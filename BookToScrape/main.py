import csv
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
START_URL = BASE_URL
HEADERS = {"User-Agent": "BooksScraper/1.1 (contact: you@example.com)"}
DELAY_PAGE = 0.7   # pause entre pages liste
DELAY_PRODUCT = 0.3  # pause entre pages produit
LOG_EVERY = 10     # log toutes les 10 fiches produit

def extract_page(url):
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def parse_rating(star_tag):
    if not star_tag:
        return None
    classes = star_tag.get("class", [])
    mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    for name, val in mapping.items():
        if name in classes:
            return val
    return None

def clean_availability(text):
    if not text:
        return 0
    import re
    m = re.search(r"(\d+)", text.strip())
    return int(m.group(1)) if m else 0

def parse_price(text):
    if not text:
        return None
    return float(text.strip().lstrip("Â£"))

def parse_product_page(product_url):
    soup = extract_page(product_url)
    title = soup.select_one("div.product_main h1").get_text(strip=True)
    price_incl = parse_price(soup.select_one("div.product_main p.price_color").get_text())

    table = soup.select_one("table.table.table-striped")
    rows = {r.th.get_text(strip=True): r.td.get_text(strip=True) for r in table.select("tr")}
    upc = rows.get("UPC")
    price_excl = parse_price(rows.get("Price (excl. tax)", ""))
    price_incl_table = parse_price(rows.get("Price (incl. tax)", ""))
    availability = clean_availability(rows.get("Availability", ""))

    breadcrumb = soup.select("ul.breadcrumb li a")
    category = breadcrumb[2].get_text(strip=True) if len(breadcrumb) > 2 else None

    desc_header = soup.select_one("#product_description")
    description = None
    if desc_header:
        desc_p = desc_header.find_next("p")
        if desc_p:
            description = desc_p.get_text(strip=True)

    rating = parse_rating(soup.select_one("p.star-rating"))
    img_rel = soup.select_one("div.item.active img")["src"]
    image_url = urljoin(product_url, img_rel)

    return {
        "title": title,
        "category": category,
        "price_excl_tax": price_excl if price_excl is not None else price_incl_table or price_incl,
        "price_incl_tax": price_incl_table or price_incl,
        "availability": availability,
        "rating": rating,
        "upc": upc,
        "description": description,
        "product_url": product_url,
        "image_url": image_url,
    }

def parse_list_page(list_url):
    soup = extract_page(list_url)
    cards = soup.select("article.product_pod h3 a")
    product_urls = [urljoin(list_url, a.get("href")) for a in cards]
    next_link = soup.select_one("li.next > a")
    next_url = urljoin(list_url, next_link.get("href")) if next_link else None
    return product_urls, next_url

def crawl_all_books(start_url):
    all_rows = []
    list_url = start_url
    page_idx = 0
    total_products = 0

    while list_url:
        page_idx += 1
        product_urls, next_url = parse_list_page(list_url)

        # LOG: page liste
        print(f"[Books][List Page {page_idx}] {list_url} -> {len(product_urls)} produits (total avant: {total_products})")

        for i, purl in enumerate(product_urls, start=1):
            row = parse_product_page(purl)
            all_rows.append(row)
            total_products += 1

        # LOG: next URL
        print(f"  Next URL: {next_url}")
        list_url = next_url
        time.sleep(DELAY_PAGE)

    print(f"[Books] TOTAL produits: {total_products}")
    return all_rows

def load_to_csv(rows, filename="books.csv"):
    fieldnames = [
        "title", "category", "price_excl_tax", "price_incl_tax",
        "availability", "rating", "upc", "description",
        "product_url", "image_url"
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

def main():
    rows = crawl_all_books(START_URL)
    load_to_csv(rows, "books.csv")
    print(f"✅ Terminé ! {len(rows)} livres exportés dans books.csv")

if __name__ == "__main__":
    main()
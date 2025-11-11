import csv
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com"
START_URL = f"{BASE_URL}/"
HEADERS = {"User-Agent": "QuotesScraper/1.1 (contact: you@example.com)"}
DELAY_PAGE = 0.4  # petite pause entre pages

def extract_page(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def transform_quote_block(block):
    text = block.find(class_="text").get_text(strip=True)
    author = block.find(class_="author").get_text(strip=True)
    tags = [t.get_text(strip=True) for t in block.select(".tags a.tag")]
    return {"quote": text, "author": author, "tags": "|".join(tags)}

def extract_all_quotes(start_url):
    url = start_url
    all_rows = []
    page_idx = 0

    while True:
        page_idx += 1
        soup = extract_page(url)
        blocks = soup.select(".quote")
        page_rows = [transform_quote_block(b) for b in blocks]
        all_rows.extend(page_rows)

        # LOGS
        print(f"[Quotes][Page {page_idx}] {url} -> {len(page_rows)} quotes (total: {len(all_rows)})")

        next_link = soup.select_one("li.next > a")
        next_url = BASE_URL + next_link.get("href") if next_link else None
        print(f"  Next URL: {next_url}")
        if not next_url:
            break
        url = next_url
        time.sleep(DELAY_PAGE)

    return all_rows

def load_to_csv(rows, filename="quotes.csv"):
    fieldnames = ["quote", "author", "tags"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

def main():
    data = extract_all_quotes(START_URL)
    load_to_csv(data, "quotes.csv")
    print(f"✅ Terminé ! {len(data)} citations exportées dans quotes.csv")

if __name__ == "__main__":
    main()
import csv
import time
from typing import List, Dict, Optional
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# --------- Réglages ---------
START_URL = "https://www.scrapethissite.com/pages/forms/?page_num=1&per_page=100"
HEADERS = {"User-Agent": "ScrapeThisSiteHockey/1.1 (contact: you@example.com)"}
DELAY_PAGE = 0.3  # pause entre pages (politesse)
OUTPUT_CSV = "hockey_teams.csv"


# --------- HTTP util ---------
def get_soup(url: str) -> BeautifulSoup:
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")


# --------- Helpers conversions ---------
def to_int(x) -> Optional[int]:
    try:
        return int(str(x).replace(",", "").strip())
    except Exception:
        return None


def to_float(x) -> Optional[float]:
    try:
        return float(str(x).replace("%", "").strip())
    except Exception:
        return None


# --------- Extraction d'une page liste ---------
def extract_rows_from_page(soup: BeautifulSoup, source_url: str) -> List[Dict[str, object]]:
    """
    Récupère les lignes de stats (Team, Year, Wins, Losses, OT Losses, Win%, GF, GA, +/-)
    depuis la page courante.
    """
    # Trouver le tableau principal (thead avec 'Team' et 'Year')
    table = None
    for t in soup.find_all("table"):
        thead = t.find("thead")
        if not thead:
            continue
        head_text = " ".join(th.get_text(" ", strip=True).lower() for th in thead.find_all("th"))
        if "team" in head_text and "year" in head_text:
            table = t
            break

    rows: List[Dict[str, object]] = []
    trs = table.select("tbody tr") if table else soup.select("tr")

    for tr in trs:
        tds = tr.find_all("td")
        # On attend au moins 8 colonnes (Team, Year, Wins, Losses, Win%, GF, GA, +/-)
        if len(tds) < 8:
            continue

        # Colonne Team (essaie d'attraper un éventuel lien)
        team_cell = tds[0]
        team_a = team_cell.find("a")
        team_name = team_cell.get_text(strip=True)
        team_detail_url = urljoin(source_url, team_a["href"]) if team_a and team_a.get("href") else None

        vals = [td.get_text(strip=True) for td in tds]

        # Ordre observé le plus courant :
        # Team | Year | Wins | Losses | OT Losses | Win % | GF | GA | +/-
        data = {
            "team": team_name,
            "year": to_int(vals[1]) if len(vals) > 1 else None,
            "wins": to_int(vals[2]) if len(vals) > 2 else None,
            "losses": to_int(vals[3]) if len(vals) > 3 else None,
            "ot_losses": to_int(vals[4]) if len(vals) > 4 and "%" not in vals[4] else None,
            "win_percent": to_float(vals[-4]) if len(vals) >= 4 else None,
            "goals_for": to_int(vals[-3]) if len(vals) >= 3 else None,
            "goals_against": to_int(vals[-2]) if len(vals) >= 2 else None,
            "goal_diff": to_int(vals[-1]) if len(vals) >= 1 else None,
            "detail_url": team_detail_url,
            "source_list_url": source_url,
        }

        if data["team"] and data["year"]:
            rows.append(data)

    return rows


# --------- Détection robuste du lien "Next" ---------
def find_next_page_url(soup: BeautifulSoup, current_url: str) -> Optional[str]:
    """
    Essaie plusieurs sélecteurs pour détecter l'URL de la page suivante.
    """
    # Cas 1 : <li class="next"><a href="?page_num=2">»</a></li>
    nxt = soup.select_one("li.next a")
    if nxt and nxt.get("href"):
        return urljoin(current_url, nxt["href"])

    # Cas 2 : rel="next"
    nxt = soup.select_one('a[rel="next"]')
    if nxt and nxt.get("href"):
        return urljoin(current_url, nxt["href"])

    # Cas 3 : pagination générique (» ou Next)
    for a in soup.select("ul.pagination a"):
        txt = a.get_text(strip=True)
        if txt in ("Next", "»", ">>"):
            href = a.get("href")
            if href:
                return urljoin(current_url, href)

    return None


# --------- Crawl complet ---------
def crawl_all(start_url: str) -> List[Dict[str, object]]:
    url = start_url
    all_rows: List[Dict[str, object]] = []
    page_idx = 0

    while url:
        page_idx += 1
        soup = get_soup(url)

        page_rows = extract_rows_from_page(soup, url)
        all_rows.extend(page_rows)

        # Logs utiles pour vérifier que la pagination fonctionne
        print(f"[Page {page_idx}] {url} -> {len(page_rows)} lignes")

        next_url = find_next_page_url(soup, url)
        print(f" Next URL: {next_url}")
        url = next_url

        time.sleep(DELAY_PAGE)

    return all_rows


# --------- Export CSV ---------
def export_csv(rows: List[Dict[str, object]], filename: str) -> None:
    cols = ["team", "year", "wins", "losses", "ot_losses", "win_percent",
            "goals_for", "goals_against", "goal_diff", "detail_url", "source_list_url"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


# --------- Main ---------
if __name__ == "__main__":
    data = crawl_all(START_URL)
    export_csv(data, OUTPUT_CSV)
    print(f"✅ Exporté {len(data)} lignes dans {OUTPUT_CSV}")
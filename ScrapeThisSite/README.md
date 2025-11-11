# ScrapeThisSite – Hockey (Full Crawl + Détails)

Ce projet extrait **toutes les lignes** de la section *Hockey Teams – Forms, Searching & Pagination* et
**suit les liens de détail** s'ils existent, afin de récupérer **un maximum d’informations**.

## 🎯 Objectifs

### Éducatif

- Pratiquer un **ETL complet** (Requests + BeautifulSoup + CSV).
- Gérer **toute la pagination** via le lien “Next”.
- Enrichir les résultats en **suivant les liens** (pages de détail).
- Exporter un CSV **complet**, réunissant toutes les colonnes rencontrées.

### Fonctionnel

- Extraire : `team, year, wins, losses, ot_losses, win_percent, goals_for, goals_against, goal_diff`
- Suivre les liens de détail (si présents) et ajouter des champs comme `detail_heading`, `detail_note`, etc.
- Générer un fichier **`hockey_full.csv`** (UTF-8), compatible Excel / Google Sheets / pandas.

## 🛠 Installation

```bash
pip install requests beautifulsoup4

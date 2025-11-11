# Quotes to Scrape – Scraper Python (Requests + BeautifulSoup + CSV)

## 🎯 Objectifs

### Côté éducatif

- **Mettre en pratique un pipeline ETL** simple :  
  **Extract** (HTTP + parsing HTML) → **Transform** (nettoyage minimal) → **Load** (CSV).
- **Apprendre BeautifulSoup** : sélecteurs CSS, `find`, `select`, récupération de texte.
- **Adopter de bonnes pratiques** : `User-Agent`, `time.sleep`, gestion d’erreurs (`raise_for_status`), encodage UTF-8.

### Côté fonctionnel

- **Extraire automatiquement** les citations, auteurs et tags depuis `http://quotes.toscrape.com`.
- **Suivre la pagination** jusqu’à la dernière page (bouton “Next”).
- **Générer un fichier `quotes.csv`** propre, lisible par Excel / Google Sheets / pandas.

---

## 📦 Prérequis

- Python **3.9+** recommandé
- Dépendances :
  - `requests`
  - `beautifulsoup4`

Installez-les :

pip install requests beautifulsoup4

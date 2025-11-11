# Books to Scrape – Scraper Python (Requests + BeautifulSoup + CSV)

## 🎯 Objectifs

### Côté éducatif

- Mettre en pratique un **pipeline ETL** :
  - **Extract** : parcours des pages listes + pages produit
  - **Transform** : normalisation (prix, stock, rating, URLs absolues)
  - **Load** : export **CSV** propre (UTF-8, en-têtes)
- Approfondir **BeautifulSoup** : sélecteurs CSS, parsing de tableaux, fil d’Ariane, images
- Appliquer des **bonnes pratiques de scraping** : `User-Agent`, `sleep`, gestion d’erreurs

### Côté fonctionnel

- Extraire **tous les livres** de `https://books.toscrape.com`
- Pour chaque livre : **titre, catégorie, prix HT/TTC, disponibilité, rating, UPC, description, URL produit, URL image**
- Générer un **fichier `books.csv`** compatible Excel / Google Sheets / pandas

---

## 📦 Prérequis

- Python **3.9+** recommandé
- Dépendances :
  - `requests`
  - `beautifulsoup4`

Installation :

```bash
pip install requests beautifulsoup4

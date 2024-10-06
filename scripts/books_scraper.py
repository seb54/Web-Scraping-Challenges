import requests
from bs4 import BeautifulSoup
import time
import random
import json
import os
from typing import Optional

# URL de base du site Books to Scrape
BASE_URL = "https://books.toscrape.com/"

# Liste des User-Agents pour simuler différentes configurations de navigateur
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1"
]

def make_request(url: str, retries: int = 5) -> Optional[requests.Response]:
    """Effectue une requête HTTP robuste avec gestion des erreurs et rotation des User-Agents."""
    retry_count = 0

    while retry_count < retries:
        headers = {
            "User-Agent": random.choice(USER_AGENTS)
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Erreur lors de la requête : {e}. Tentative {retry_count + 1}/{retries}")
            retry_count += 1
            time.sleep(random.uniform(1, 3))

    print(f"Échec de la récupération de l'URL après {retries} tentatives : {url}")
    return None

def scrape_category_with_pagination(category_url: str) -> dict:
    """Scrape les livres dans une catégorie en prenant en compte la pagination."""
    total_books = 0
    total_price = 0.0

    while True:
        response = make_request(category_url)
        if response is None:
            print(f"Impossible de scraper l'URL : {category_url}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
        
        for book in books:
            price_str = book.find('p', class_='price_color').text[1:]
            try:
                price = float(price_str)
                total_books += 1
                total_price += price
            except ValueError:
                print(f"Erreur de conversion du prix : {price_str}")

        next_page = soup.find('li', class_='next')
        if next_page:
            next_url = next_page.find('a')['href']
            category_url = category_url.rsplit('/', 1)[0] + '/' + next_url
            sleep_time = random.uniform(1, 3)
            print(f"Attente de {sleep_time:.2f} secondes avant de scraper la page suivante...")
            time.sleep(sleep_time)
        else:
            break

    return {
        "nombre_de_livres": total_books,
        "prix_moyen": round(total_price / total_books, 2) if total_books > 0 else 0.0
    }

def scrape_categories():
    """Récupère le nombre de livres et le prix moyen par catégorie."""
    response = make_request(BASE_URL)
    if response is None:
        print("Impossible de scraper la page principale.")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    categories = soup.find('ul', class_='nav nav-list').find_all('a')
    
    for category in categories[1:]:
        category_name = category.text.strip()
        category_url = BASE_URL + category['href']
        print(f"Scraping catégorie : {category_name}")
        category_data = scrape_category_with_pagination(category_url)
        results.append({
            "catégorie": category_name,
            "nombre_de_livres": category_data["nombre_de_livres"],
            "prix_moyen": category_data["prix_moyen"]
        })
        print(f"Catégorie: {category_name} | Nombre de livres: {category_data['nombre_de_livres']} | Prix moyen: {category_data['prix_moyen']} £")

    export_to_json(results)

def export_to_json(data: list):
    """Exporte les données dans un fichier JSON à l'emplacement ../data/books_scrape.json."""
    json_path = os.path.join('..', 'data', 'books_scrape.json')
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Les résultats ont été exportés vers {json_path}")

def main():
    print("Scraping des catégories...")
    scrape_categories()

if __name__ == "__main__":
    main()
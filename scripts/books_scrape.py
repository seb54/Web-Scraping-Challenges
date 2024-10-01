import requests
from bs4 import BeautifulSoup
import time
import random
import json
import os

# URL de base du site Books to Scrape
BASE_URL = "https://books.toscrape.com/"

# Liste des User-Agents pour simuler différentes configurations de navigateur
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1"
]

# Fonction pour faire une requête HTTP robuste avec gestion des erreurs et rotation des User-Agents
def make_request(url):
    max_retries = 5  # Nombre maximum de tentatives en cas d'erreur
    retry_count = 0

    while retry_count < max_retries:
        headers = {
            "User-Agent": random.choice(USER_AGENTS)
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)  # Timeout ajouté
            response.raise_for_status()  # Vérifie que le statut est 200 (succès)
            return response
        except requests.exceptions.HTTPError as http_err:
            print(f"Erreur HTTP: {http_err}. Tentative {retry_count + 1}/{max_retries}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Erreur de connexion: {conn_err}. Tentative {retry_count + 1}/{max_retries}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Délai d'attente dépassé: {timeout_err}. Tentative {retry_count + 1}/{max_retries}")
        except requests.exceptions.RequestException as req_err:
            print(f"Erreur de requête: {req_err}. Tentative {retry_count + 1}/{max_retries}")

        retry_count += 1
        time.sleep(random.uniform(1, 3))  # Attendre entre 1 et 3 secondes avant de réessayer

    print(f"Échec de la récupération de l'URL après {max_retries} tentatives : {url}")
    return None  # Retourner None si toutes les tentatives échouent

# Fonction pour scraper les livres dans une catégorie en prenant en compte la pagination
def scrape_category_with_pagination(category_url):
    total_books = 0  # Nombre total de livres dans la catégorie
    total_price = 0.0  # Prix total des livres dans la catégorie

    while True:
        response = make_request(category_url)
        if response is None:  # Si la requête échoue, on arrête
            print(f"Impossible de scraper l'URL : {category_url}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        books = soup.find_all('article', class_='product_pod')
        for book in books:
            price_str = book.find('p', class_='price_color').text[1:]  # Enlever le symbole de livre
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

            sleep_time = random.uniform(1, 3)  # Délai aléatoire entre 1 et 3 secondes
            print(f"Attente de {sleep_time:.2f} secondes avant de scraper la page suivante...")
            time.sleep(sleep_time)

        else:
            break  # Sortir de la boucle quand il n'y a plus de page suivante

    if total_books > 0:
        average_price = total_price / total_books
    else:
        average_price = 0.0

    return total_books, average_price

# Fonction pour récupérer le nombre de livres et prix moyen par catégorie
def scrape_categories():
    response = make_request(BASE_URL)
    if response is None:
        print("Impossible de scraper la page principale.")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    results = []  # Liste pour stocker les résultats des catégories

    categories = soup.find('ul', class_='nav nav-list').find_all('a')
    for category in categories[1:]:  # On saute le premier lien "Books" qui est général
        category_name = category.text.strip()
        category_url = BASE_URL + category['href']

        print(f"Scraping catégorie : {category_name}")
        total_books, average_price = scrape_category_with_pagination(category_url)

        # Ajouter les résultats de la catégorie dans la liste
        results.append({
            "catégorie": category_name,
            "nombre_de_livres": total_books,
            "prix_moyen": round(average_price, 2)
        })

        print(f"Catégorie: {category_name} | Nombre de livres: {total_books} | Prix moyen: {average_price:.2f} £")

    # Exporter les résultats dans un fichier JSON
    export_to_json(results)

def export_to_json(data):
    """
    Exporte les données dans un fichier JSON à l'emplacement ../data/books_scrape.json
    """
    # Définir le chemin du fichier JSON
    json_path = os.path.join('..', 'data', 'books_scrape.json')

    # Créer le dossier data s'il n'existe pas
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    # Écriture des données dans le fichier JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Les résultats ont été exportés vers {json_path}")

# Appel des fonctions pour exécuter le scraping
print("Scraping des catégories...")
scrape_categories()

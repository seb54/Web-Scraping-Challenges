import random
import time
import requests
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from typing import Optional

# Liste des User-Agents pour rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
]

def get_random_headers() -> dict:
    """Retourne un en-tête User-Agent aléatoire."""
    return {"User-Agent": random.choice(USER_AGENTS)}

def type_like_human(element, text: str):
    """Simule une frappe humaine sur un élément Web."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

def navigate_pagination(driver, page_count: int) -> int:
    """Clique sur le bouton 'Next' tant qu'il est présent, pour naviguer à travers la pagination."""
    action = ActionChains(driver)
    
    while True:
        try:
            next_button = driver.find_elements(By.CSS_SELECTOR, "li.next > a")
            if next_button:
                next_button = next_button[0]
                action.move_to_element(next_button).perform()
                time.sleep(random.uniform(2, 5))
                next_button.click()
                time.sleep(random.uniform(2, 4))
                page_count += 1
                print(f"Navigué vers : {driver.current_url} (Page {page_count})")
            else:
                print("Fin de la pagination : Pas de bouton 'Next' trouvé.")
                break
        except Exception as e:
            print("Erreur inattendue :", str(e))
            break
    
    return page_count

def save_page_count_to_json(page_count: int):
    """Sauvegarde le nombre total de pages dans un fichier JSON."""
    data = {"total_pages": page_count}
    file_path = os.path.join('..', 'data', 'bot_connect_count_pages.json')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Données sauvegardées dans {file_path}")

def configure_driver() -> webdriver.Chrome:
    """Configure le navigateur Chrome avec un profil utilisateur et retourne le driver configuré."""
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=C:\\Users\\sebas\\AppData\\Local\\Google\\Chrome\\User Data")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login(driver, username_text: str, password_text: str):
    """Effectue la connexion sur le site donné en simulant une saisie humaine."""
    driver.get("https://quotes.toscrape.com/login")
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    action = ActionChains(driver)
    action.move_to_element(username).perform()
    type_like_human(username, username_text)
    action.move_to_element(password).perform()
    type_like_human(password, password_text)
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    action.move_to_element(login_button).click().perform()
    time.sleep(random.uniform(2, 4))

def main():
    driver = configure_driver()
    try:
        login(driver, "Homer Simpson", "Dooh!")
        page_count = 1
        page_count = navigate_pagination(driver, page_count)
        save_page_count_to_json(page_count)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
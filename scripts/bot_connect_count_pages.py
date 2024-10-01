import random
import time
import requests
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Liste des User-Agents pour rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
]

# Fonction pour récupérer un en-tête User-Agent aléatoire
def get_random_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}

# Fonction pour taper comme un humain
def type_like_human(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))  # Délai aléatoire entre chaque touche


# Fonction pour cliquer sur le bouton "Next" tant qu'il est présent
def navigate_pagination(driver, page_count):
    action = ActionChains(driver)
    
    while True:
        try:
            # Vérifie la présence du bouton 'Next'
            next_button = driver.find_elements(By.CSS_SELECTOR, "li.next > a")  # Utilise find_elements pour éviter une exception

            if next_button:  # Si le bouton "Next" est présent
                next_button = next_button[0]  # Récupère l'élément
                # Simule un déplacement du curseur vers le bouton "Next"
                action.move_to_element(next_button).perform()
                
                # Ajoute un délai aléatoire avant de cliquer sur le bouton
                time.sleep(random.uniform(2, 5))
                
                # Clique sur le bouton "Next"
                next_button.click()
                
                # Ajoute un autre délai après avoir cliqué, pour simuler la navigation naturelle
                time.sleep(random.uniform(2, 4))
                
                # Affiche l'URL de la page courante après avoir changé de page
                page_count += 1
                print(f"Navigué vers : {driver.current_url} (Page {page_count})")
                
            else:
                # Si le bouton "Next" n'est pas trouvé, on arrête la boucle
                print("Fin de la pagination : Pas de bouton 'Next' trouvé.")
                break

        except Exception as e:
            # Si une autre erreur survient, on sort de la boucle
            print("Erreur inattendue : ", str(e))
            break
    
    return page_count

# Fonction pour sauvegarder les données dans un fichier JSON
def save_page_count_to_json(page_count):
    data = {"total_pages": page_count}
    
    # Définir le chemin du fichier dans ../data/
    file_path = os.path.join('..', 'data', 'bot_connect_count_pages.json')
    
    # S'assurer que le répertoire existe
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Écrire les données dans le fichier JSON
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Données sauvegardées dans {file_path}")

# Configuration du navigateur avec profil utilisateur
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=C:\\Users\\sebas\\AppData\\Local\\Google\\Chrome\\User Data")  # Remplace par le chemin réel du profil
driver = webdriver.Chrome(options=chrome_options)

# Ouvrir la page de login
driver.get("https://quotes.toscrape.com/login")

# Simuler la saisie humaine pour le login
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")

# Simuler les mouvements de souris vers les champs avant la saisie
action = ActionChains(driver)
action.move_to_element(username).perform()
type_like_human(username, "Homer Simpson")

action.move_to_element(password).perform()
type_like_human(password, "Dooh!")

# Cliquer sur le bouton de connexion
login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
action.move_to_element(login_button).click().perform()

# Attendre quelques secondes que la page se charge
time.sleep(random.uniform(2, 4))

# Initialisation du compteur de pages
page_count = 1  # La première page est déjà ouverte

# Boucle de scraping avec gestion de la pagination
page_count = navigate_pagination(driver, page_count)

# Sauvegarder le nombre total de pages dans un fichier JSON
save_page_count_to_json(page_count)

# Fermer le navigateur une fois terminé
driver.quit()

import random
import time
import requests
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
def navigate_pagination(driver):
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
                print(f"Navigué vers : {driver.current_url}")
                
            else:
                # Si le bouton "Next" n'est pas trouvé, on arrête la boucle
                print("Fin de la pagination : Pas de bouton 'Next' trouvé.")
                break

        except Exception as e:
            # Si une autre erreur survient, on sort de la boucle
            print("Erreur inattendue : ", str(e))
            break

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
type_like_human(username, "your_username")

action.move_to_element(password).perform()
type_like_human(password, "your_password")

# Cliquer sur le bouton de connexion
login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
action.move_to_element(login_button).click().perform()

# Attendre quelques secondes que la page se charge
time.sleep(random.uniform(2, 4))


# Boucle de scraping avec gestion de la pagination
while True:
    # Traiter le contenu de la page ici
    print(f"Scraping la page: {driver.current_url}")
    navigate_pagination(driver)
    
    # Condition d'arrêt : vérifie s'il n'y a plus de bouton "Next"
    if not driver.find_elements(By.LINK_TEXT, "Next"):
        print("Pagination terminée.")
        break

# Fermer le navigateur une fois terminé
driver.quit()

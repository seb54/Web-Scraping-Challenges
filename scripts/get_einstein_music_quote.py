import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurer Chrome pour afficher la fenêtre (sans headless) et options supplémentaires
chrome_options = Options()

# Chemin vers ton WebDriver
service = Service(executable_path="..\\drivers\\chromedriver.exe")

# Initialiser le driver avec les options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Ouvrir la page avec Selenium
driver.get("https://quotes.toscrape.com/search.aspx")

# Pause supplémentaire pour donner le temps au site de charger
time.sleep(5)  # Pause de 5 secondes, ajuste selon la vitesse du chargement

# Attendre que l'élément avec l'ID "author" soit visible
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "author")))

# Sélectionner Albert Einstein comme auteur
author_select = Select(driver.find_element(By.ID, "author"))
author_select.select_by_visible_text("Albert Einstein")

# Sélectionner 'music' comme tag
tag_select = Select(driver.find_element(By.ID, "tag"))
tag_select.select_by_visible_text("music")

# Exécuter le JavaScript pour soumettre le formulaire via __doPostBack
driver.execute_script("__doPostBack();")

# Attendre que les résultats apparaissent (maximum 10 secondes)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "results"))
)

# Récupérer la citation dans la div "results"
quote = driver.find_element(By.CLASS_NAME, "content").text

print("Citation d'Albert Einstein sur la musique:", quote)

# Fermer le driver
driver.quit()

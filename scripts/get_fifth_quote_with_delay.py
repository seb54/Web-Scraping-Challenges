from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurer l'option pour que le navigateur n'affiche pas de fenêtre (headless)
chrome_options = Options()
chrome_options.add_argument("--headless")

# Chemin vers ton WebDriver
service = Service(executable_path="..\\drivers\\chromedriver.exe")

# Initialiser le driver avec les options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Ouvrir la page avec Selenium
driver.get("https://quotes.toscrape.com/js-delayed/page/5/")

# Attendre que les citations apparaissent avec un délai maximum de 10 secondes
try:
    # Attente explicite pour que les éléments soient présents
    quotes = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
    )
    
    # Vérifier s'il y a au moins 5 citations
    if len(quotes) >= 5:
        fifth_quote = quotes[4].find_element(By.CLASS_NAME, "text").text
        print("Cinquième citation:", fifth_quote)
    else:
        print("Il n'y a pas assez de citations sur la page.")
finally:
    # Fermer le driver
    driver.quit()

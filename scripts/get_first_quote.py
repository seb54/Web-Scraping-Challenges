from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configurer l'option pour que le navigateur n'affiche pas de fenêtre (headless)
chrome_options = Options()
chrome_options.add_argument("--headless")

# Chemin vers ton WebDriver
service = Service(executable_path="..\\drivers\\chromedriver.exe")

# Initialiser le driver avec les options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Ouvrir la page avec Selenium
driver.get("https://quotes.toscrape.com/js/page/10/")

# Extraire la première citation
try:
    first_quote = driver.find_element(By.CLASS_NAME, "quote")
    quote_text = first_quote.find_element(By.CLASS_NAME, "text").text
    print("Première citation:", quote_text)
finally:
    # Fermer le driver
    driver.quit()

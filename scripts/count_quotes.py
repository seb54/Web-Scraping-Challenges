from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Lancer le navigateur avec Selenium (assurez-vous que le driver est dans le PATH)
driver = webdriver.Chrome()

# Aller à l'URL
driver.get("https://quotes.toscrape.com/scroll")

# Fonction pour faire défiler jusqu'à ce que la page ne scrolle plus
def scroll_until_no_more_quotes(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroller jusqu'en bas de la page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Attendre que les nouvelles citations soient chargées
        time.sleep(2)  # Ajuster le délai si nécessaire

        # Calculer la nouvelle hauteur de la page
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Si la hauteur n'a pas changé, on est à la fin de la page
        if new_height == last_height:
            break
        
        last_height = new_height

# Appel de la fonction pour scroller jusqu'à la fin
scroll_until_no_more_quotes(driver)

# Récupérer toutes les div ayant la classe "quote"
quotes = driver.find_elements(By.CLASS_NAME, "quote")

# Filtrer et compter uniquement les citations qui ont un <span class="text">
valid_quotes = []
for quote in quotes:
    span_text = quote.find_elements(By.CLASS_NAME, "text")
    if span_text:
        valid_quotes.append(quote)

# Afficher le nombre de citations valides
print(f"Nombre de citations valides trouvées : {len(valid_quotes)}")

# Fermer le navigateur
driver.quit()

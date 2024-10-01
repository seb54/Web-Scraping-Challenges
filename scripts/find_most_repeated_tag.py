from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from collections import Counter
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
driver.get("https://quotes.toscrape.com/tableful/")

# Attendre que les tags soient présents sur la page
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//td/a")))


# Récupérer toutes les cellules <td> qui contiennent des tags
tags_elements = driver.find_elements(By.XPATH, "//td[contains(text(), 'Tags:')]/a")

# Extraire les textes des liens (les noms des tags)
tags = [tag.text for tag in tags_elements]

# Compter les occurrences de chaque tag
tag_counts = Counter(tags)

# Trouver le tag le plus répétitif
most_common_tag = tag_counts.most_common(1)[0]  # Renvoie le tag le plus fréquent

print("Tag le plus répétitif:", most_common_tag[0])
print("Nombre d'occurrences:", most_common_tag[1])

# Fermer le driver
driver.quit()

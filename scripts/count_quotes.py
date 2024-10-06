from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def configure_driver() -> webdriver.Chrome:
    """Configure le navigateur Chrome et retourne le driver configuré."""
    driver = webdriver.Chrome()
    return driver

def scroll_until_no_more_quotes(driver):
    """Fait défiler la page jusqu'à ce qu'il n'y ait plus de nouvelles citations à charger."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Ajuster le délai si nécessaire
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_valid_quotes(driver) -> list:
    """Récupère toutes les citations valides ayant un <span class='text'>."""
    quotes = driver.find_elements(By.CLASS_NAME, "quote")
    valid_quotes = [quote for quote in quotes if quote.find_elements(By.CLASS_NAME, "text")]
    return valid_quotes

def main():
    driver = configure_driver()
    try:
        driver.get("https://quotes.toscrape.com/scroll")
        scroll_until_no_more_quotes(driver)
        valid_quotes = get_valid_quotes(driver)
        print(f"Nombre de citations valides trouvées : {len(valid_quotes)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
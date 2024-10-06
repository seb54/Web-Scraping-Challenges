from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def configure_driver(executable_path: str) -> webdriver.Chrome:
    """Configure le navigateur Chrome en mode headless et retourne le driver configuré."""
    chrome_options = Options()
    service = Service(executable_path=executable_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def wait_for_quotes(driver, timeout: int = 20):
    """Attend que toutes les citations soient présentes sur la page avec un délai plus long."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
    )

def get_fifth_quote(quotes: list) -> str:
    """Récupère la cinquième citation si elle est présente."""
    if len(quotes) >= 5:
        return quotes[4].find_element(By.CLASS_NAME, "text").text
    else:
        return "Il n'y a pas assez de citations sur la page."

def main():
    driver = configure_driver("..\\drivers\\chromedriver.exe")
    try:
        driver.get("https://quotes.toscrape.com/js-delayed/page/5/")
        time.sleep(5)  # Pause pour s'assurer que la page est entièrement chargée
        quotes = wait_for_quotes(driver)
        fifth_quote = get_fifth_quote(quotes)
        print("Cinquième citation:", fifth_quote)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
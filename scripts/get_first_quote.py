from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def configure_driver(executable_path: str) -> webdriver.Chrome:
    """Configure le navigateur Chrome en mode headless et retourne le driver configuré."""
    chrome_options = Options()
    service = Service(executable_path=executable_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def wait_for_first_quote(driver, timeout: int = 10):
    """Attend que la première citation soit présente sur la page."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, "quote"))
    )

def get_first_quote(driver) -> str:
    """Récupère la première citation présente sur la page."""
    first_quote = driver.find_element(By.CLASS_NAME, "quote")
    quote_text = first_quote.find_element(By.CLASS_NAME, "text").text
    return quote_text

def main():
    driver = configure_driver("..\\drivers\\chromedriver.exe")
    try:
        driver.get("https://quotes.toscrape.com/js/page/10/")
        wait_for_first_quote(driver)
        quote_text = get_first_quote(driver)
        print("Première citation:", quote_text)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
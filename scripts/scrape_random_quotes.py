import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

def initialize_driver():
    """
    Initialise le WebDriver Chrome.
    """
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        return driver
    except WebDriverException as e:
        print(f"Erreur lors de l'initialisation du WebDriver : {e}")
        return None

def get_random_quote(driver, url):
    """
    Charge la page de citation et extrait la citation et l'auteur.
    Args:
        driver (webdriver.Chrome): L'instance de WebDriver.
        url (str): URL de la page à charger.

    Returns:
        tuple: La citation et l'auteur sous la forme (quote_text, author_text).
    """
    try:
        driver.get(url)
        quote_element = driver.find_element(By.CLASS_NAME, "text")
        author_element = driver.find_element(By.CLASS_NAME, "author")
        return quote_element.text, author_element.text
    except NoSuchElementException as e:
        print(f"Erreur lors de l'extraction de la citation : {e}")
        return None, None

def scrape_quotes(url, total_quotes=100):
    """
    Scrape des citations uniques jusqu'à atteindre le nombre souhaité.
    Args:
        url (str): URL de la page à scraper.
        total_quotes (int): Nombre de citations uniques à obtenir.
    """
    driver = initialize_driver()
    if not driver:
        return

    quotes_dict = {}
    start_time = time.time()

    while len(quotes_dict) < total_quotes:
        quote_text, author_text = get_random_quote(driver, url)
        if quote_text and author_text:
            quote_key = f"{quote_text} - {author_text}"
            if quote_key not in quotes_dict:
                quotes_dict[quote_key] = {
                    "quote": quote_text,
                    "author": author_text
                }
                print(f"Nouvelle citation trouvée ({len(quotes_dict)}/{total_quotes}) : {quote_key}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Temps nécessaire pour scraper les {total_quotes} citations uniques : {elapsed_time:.2f} secondes")

    driver.quit()

def main():
    """
    Point d'entrée principal du script.
    """
    url = "https://quotes.toscrape.com/random"
    total_quotes = 100
    scrape_quotes(url, total_quotes)

if __name__ == "__main__":
    main()
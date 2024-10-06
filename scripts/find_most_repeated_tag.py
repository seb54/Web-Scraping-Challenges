from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter

def configure_driver(executable_path: str) -> webdriver.Chrome:
    """Configure le navigateur Chrome avec un profil headless et retourne le driver configuré."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    service = Service(executable_path=executable_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def wait_for_tags(driver, timeout: int = 10):
    """Attend que les tags soient présents sur la page."""
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//td/a")))

def get_tags(driver) -> list:
    """Récupère tous les tags présents sur la page."""
    tags_elements = driver.find_elements(By.XPATH, "//td[contains(text(), 'Tags:')]/a")
    tags = [tag.text for tag in tags_elements]
    return tags

def get_most_common_tag(tags: list) -> tuple:
    """Trouve le tag le plus répétitif et son nombre d'occurrences."""
    tag_counts = Counter(tags)
    most_common_tag = tag_counts.most_common(1)[0]
    return most_common_tag

def main():
    driver = configure_driver("..\\drivers\\chromedriver.exe")
    try:
        driver.get("https://quotes.toscrape.com/tableful/")
        wait_for_tags(driver)
        tags = get_tags(driver)
        most_common_tag = get_most_common_tag(tags)
        print("Tag le plus répétitif:", most_common_tag[0])
        print("Nombre d'occurrences:", most_common_tag[1])
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
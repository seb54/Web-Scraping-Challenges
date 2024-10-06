import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def configure_driver(executable_path: str) -> webdriver.Chrome:
    """Configure le navigateur Chrome et retourne le driver configuré."""
    chrome_options = Options()
    service = Service(executable_path=executable_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def wait_for_element(driver, by: By, value: str, timeout: int = 30):
    """Attend qu'un élément soit visible sur la page."""
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def select_author_and_tag(driver, author: str, tag: str):
    """Sélectionne l'auteur et le tag dans les menus déroulants."""
    author_select = Select(driver.find_element(By.ID, "author"))
    author_select.select_by_visible_text(author)
    tag_select = Select(driver.find_element(By.ID, "tag"))
    tag_select.select_by_visible_text(tag)

def submit_form_with_javascript(driver):
    """Soumet le formulaire via l'appel JavaScript __doPostBack."""
    driver.execute_script("__doPostBack();")

def get_quote(driver) -> str:
    """Récupère la citation présente dans la div "results"."""
    wait_for_element(driver, By.CLASS_NAME, "results", timeout=10)
    quote = driver.find_element(By.CLASS_NAME, "content").text
    return quote

def main():
    driver = configure_driver("..\\drivers\\chromedriver.exe")
    try:
        driver.get("https://quotes.toscrape.com/search.aspx")
        time.sleep(5)  # Pause pour donner le temps au site de charger
        wait_for_element(driver, By.ID, "author")
        select_author_and_tag(driver, "Albert Einstein", "music")
        submit_form_with_javascript(driver)
        quote = get_quote(driver)
        print("Citation d'Albert Einstein sur la musique:", quote)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
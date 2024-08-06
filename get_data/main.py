import noideacore
import pagecrawler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
from bs4 import BeautifulSoup

training = "https://lichess.org/training"
analyse = ""

def get_training_fen():
    service = ChromeService()
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(training)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    time.sleep(5)
    source = driver.page_source
    print(source)
    button = driver.find_element(By.CLASS_NAME, 'view_solution')
    button.click()
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    fen = str(soup.find(title="Spiele mit dem Computer"))
    print(fen)
    fen = fen[fen.find('href="/analysis/')+len('href="/analysis/'):]
    fen = fen[:fen.find('?')].replace('_', ' ')
    driver.quit()
    return fen


if __name__ == "__main__":
    print(get_training_fen())


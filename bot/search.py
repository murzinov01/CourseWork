from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from parsers.habr_parser import HabrParser

DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def find_articles_by_str(text: str = ""):
    habr_parser = HabrParser(DRIVER)
    articles = habr_parser.search(text)

    print(articles)
    return articles

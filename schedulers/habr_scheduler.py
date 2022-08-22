import time
from datetime import datetime as dt

import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import config
from parsers.habr_parser import HabrParser


def habr_scheduler():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    print("Scheduler started at ", dt.now())

    habr_parser = HabrParser(driver)
    habr_parser.update(days_n=config.UPDATE_FOR_DAYS_NUM)


def main():
    schedule.every(config.RUN_EVERY_HOURS_NUM).hours.do(habr_scheduler)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()

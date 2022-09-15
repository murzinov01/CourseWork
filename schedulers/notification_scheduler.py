import json
import time
from dataclasses import asdict
from datetime import datetime as dt

import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import config
from bot.database import HabrDB
from parsers.habr_parser import HabrParser
import pika


def notification_schedule(every_minutes: int):
    habr_db = HabrDB()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    print("Notification Scheduler started at ", dt.now())

    habr_parser = HabrParser(driver)
    newest_articles = habr_parser.find_newest_articles(for_minutes=every_minutes)
    for article in newest_articles:
        entry = {
            "chat_ids": habr_db.find_users_subscribed(article),
            "article_to_send": json.dumps(asdict(article), ensure_ascii=False)
        }

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=config.RABBIT_HOST, port=config.RABBIT_PORT
            )
        )
        channel = connection.channel()
        channel.exchange_declare(exchange="notifications", exchange_type="fanout")
        channel.basic_publish(
            exchange="notifications",
            routing_key="",
            body=json.dumps(entry, ensure_ascii=False).encode()
        )
        connection.close()


def main():
    schedule.every(config.PARSE_FOR_NOTIFY_PERIOD).minutes.do(
        notification_schedule, every_minutes=config.PARSE_FOR_NOTIFY_PERIOD
    )
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception:
            continue


if __name__ == "__main__":
    main()

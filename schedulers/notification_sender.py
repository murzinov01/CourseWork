import json

from pymongo import MongoClient
import requests
import pika

import config
from bot.messages import Messages
from bot.templates import construct_article_from_template

CLIENT = MongoClient(config.MONGO_URL)
NOTIFICATION_QUEUE = CLIENT[config.DATABASE][config.NOTIFICATIONS_QUEUE_COLL]


def notification_sender(ch, method, properties, body: bytes):
    notification = json.loads(body)
    if notification:
        user_ids = notification.get("user_ids")
        article = notification.get("article_to_send")
        if user_ids is not None and article is not None:
            article = json.loads(article)
            article = construct_article_from_template(article)
            for user_id in user_ids:
                if user_id:
                    requests.post(
                        config.SEND_MESSAGE_URL,
                        json={
                            "chat_id": user_id,
                            "text": Messages.NOTIFY + article,
                            # "disable_notification": True,
                            "parse_mode": "HTML",
                        },
                    )


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST, port=config.RABBIT_PORT))
    channel = connection.channel()

    channel.exchange_declare(exchange="notifications", exchange_type="fanout")

    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange="notifications", queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=notification_sender, auto_ack=True)

    channel.start_consuming()


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception:
            continue

import logging

from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
)
from telegram.ext.filters import TEXT, COMMAND, Regex

import config
from bot.handlers import button_handler, find_by_string, find_by_theme, message_handler
from bot.short_commands import find_articles, start, _help, subscribe, unsubscribe, show_subscribes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


def main():
    application = ApplicationBuilder().token(config.TOKEN).build()

    messages_handler = MessageHandler(TEXT & (~COMMAND), message_handler)
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", _help)
    find_articles_handler = CommandHandler("find_articles", find_articles)
    subscribe_handler = CommandHandler("subscribe", subscribe)
    unsubscribe_handler = CommandHandler("unsubscribe", unsubscribe)
    show_subscribes_handler = CommandHandler("show_subscribes", show_subscribes)
    find_by_theme_handler = MessageHandler(Regex(r"Поиск по фильтрам"), find_by_theme)
    find_by_string_handler = MessageHandler(Regex(r"Обычный поиск"), find_by_string)

    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(find_articles_handler)
    application.add_handler(subscribe_handler)
    application.add_handler(unsubscribe_handler)
    application.add_handler(show_subscribes_handler)
    application.add_handler(find_by_theme_handler)
    application.add_handler(find_by_string_handler)
    application.add_handler(messages_handler)

    application.run_polling()


if __name__ == "__main__":
    main()

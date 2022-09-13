import json
from dataclasses import asdict

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from webdriver_manager.chrome import ChromeDriverManager

import config
from parsers.habr_parser import HabrParser

from bot.database import HabrDB, RedisDB
from bot.keyboards import generate_articles_keyboard, KeyboardButtons
from bot.messages import get_wait_msg, Messages

from hashlib import md5

from bot.templates import construct_article_from_template

DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


async def find_articles_by_str(
    update, context: ContextTypes.DEFAULT_TYPE, user_msg: str = "", page: int = 1
) -> list[dict]:
    # Calc query id
    redis_db = RedisDB()
    query_key = f"{user_msg}_{page}"
    query_id = md5(query_key.encode(encoding="utf-8")).hexdigest()
    articles = await redis_db.get(query_id)

    if not articles:  # if not query in cash
        await context.bot.send_message(chat_id=update.effective_chat.id, text=get_wait_msg())
        habr_parser = HabrParser(DRIVER)
        articles = habr_parser.search(user_msg, page=page)
        articles = list(map(asdict, articles))
        await redis_db.set(query_id, json.dumps(articles, ensure_ascii=False))
    else:
        articles = json.loads(articles)

    return articles


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text.lower()
    user_id = update.message.from_user["id"]
    habr_db = HabrDB()
    habr_page = 1

    articles = await find_articles_by_str(update, context, user_msg, page=habr_page)

    if articles:
        titles_on_page = [article["title"] for article in articles]
        await habr_db.update_user(
            user_id,
            {
                "search_query": user_msg,
                "current_page": 0,
                "habr_page": habr_page,
                "titles_on_page": titles_on_page,
                "articles_on_page": articles,
            },
        )

        articles_keyboard = generate_articles_keyboard(articles, 0, config.ARTICLES_PER_PAGE)
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=Messages.FIND_RESULT, reply_markup=articles_keyboard
        )

        return await habr_db.update_user(user_id, {"action": "choose_article"})
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=Messages.CAN_NOT_FIND,
        )


async def show_article(update: Update, context: ContextTypes.DEFAULT_TYPE):
    title = update.message.text
    user_id = update.message.from_user["id"]
    habr_db = HabrDB()
    if article := await habr_db.find_article_by_title(user_id, title):
        article = construct_article_from_template(article)
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=article, parse_mode="HTML")


async def paginate_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    user_id = update.message.from_user["id"]
    habr_db = HabrDB()

    user_entry = await habr_db.find_user(
        user_id, {"articles_on_page": 1, "titles_on_page": 1, "habr_page": 1, "current_page": 1, "search_query": 1}
    )
    titles_on_page = user_entry.get("titles_on_page", [])
    articles_on_page = user_entry.get("articles_on_page", [])
    current_page = user_entry.get("current_page", 0)
    habr_page = user_entry.get("habr_page", 0)
    search_query = user_entry.get("search_query", "")
    titles_num = len(titles_on_page)
    update_fields = {}

    if user_msg == KeyboardButtons.LEFT:
        page = current_page - 1
    else:
        page = current_page + 1

    max_page = titles_num // config.ARTICLES_PER_PAGE
    if titles_num % config.ARTICLES_PER_PAGE != 0:
        max_page + 1

    if 0 <= page <= max_page:
        current_page = page
        left = current_page * config.ARTICLES_PER_PAGE
        right = (current_page + 1) * config.ARTICLES_PER_PAGE
        articles_keyboard = generate_articles_keyboard(articles_on_page, left, right)
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=Messages.FIND_RESULT, reply_markup=articles_keyboard
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=Messages.WAIT_PLEASE,
            reply_markup=ReplyKeyboardRemove(),
        )
        current_page = 0 if page > max_page else max_page
        habr_page = habr_page + 1 if page > max_page else habr_page - 1

        if habr_page < 1:
            habr_page = 1
            current_page = 0
        left = current_page * config.ARTICLES_PER_PAGE
        right = (current_page + 1) * config.ARTICLES_PER_PAGE
        articles_on_page = await find_articles_by_str(update, context, search_query, page=habr_page)
        titles_on_page = [article["title"] for article in articles_on_page]

        update_fields = {
            "articles_on_page": articles_on_page,
            "titles_on_page": titles_on_page,
        }

        articles_keyboard = generate_articles_keyboard(articles_on_page, left, right)
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=Messages.FIND_RESULT, reply_markup=articles_keyboard
        )

    update_fields["current_page"] = current_page
    update_fields["habr_page"] = habr_page

    await habr_db.update_user(user_id, update_fields)

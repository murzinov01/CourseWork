from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import HABR_THEMES_RU
from bot.database import HabrDB
from bot.keyboards import FINDER_KEYBOARD, SUBSCRIBE_KEYBOARD, UNSUBSCRIBE_KEYBOARD
from bot.messages import Messages


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_chat.first_name
    await context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.START.format(user_name))


async def _help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.HELP)


async def find_articles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=Messages.HOW_SEARCH,
        reply_markup=FINDER_KEYBOARD,
    )


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=Messages.HOW_NOTIFY,
        reply_markup=SUBSCRIBE_KEYBOARD,
    )


async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=Messages.UNSUBSCRIBE,
        reply_markup=UNSUBSCRIBE_KEYBOARD,
    )


def create_pretty_list(strings: list[str]) -> str:
    result = ""
    for string in strings:
        result += f"• {string}\n"
    return result


async def show_subscribes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    habr_db = HabrDB()

    answer = ""
    user_id = update.effective_chat.id
    user_entry = await habr_db.find_user(
        user_id, projection={"subscribe_on_theme": 1, "subscribe_on_author": 1, "subscribe_on_tag": 1}
    )

    subscribe_on_theme = user_entry.get("subscribe_on_theme", [])
    subscribe_on_author = user_entry.get("subscribe_on_author", [])
    subscribe_on_tag = user_entry.get("subscribe_on_tag", [])

    if any((subscribe_on_theme, subscribe_on_author, subscribe_on_tag)):
        answer += Messages.FOUND_SUBSCRIPTIONS

    # Check subscribes by theme
    if subscribe_on_theme:
        themes = [theme_ru for theme in subscribe_on_theme if (theme_ru := HABR_THEMES_RU.get(theme)) is not None]
        themes_pretty_list = create_pretty_list(themes)
        answer += Messages.SUBSCRIBED_ON_THEMES + themes_pretty_list

    # Check subscribes by author
    if subscribe_on_author:
        authors_pretty_list = create_pretty_list(subscribe_on_author)
        answer += "\n" + Messages.SUBSCRIBED_ON_AUTHORS + authors_pretty_list

    # Check subscribes by tag
    if subscribe_on_tag:
        tags_pretty_list = create_pretty_list(subscribe_on_tag)
        answer += "\n" + Messages.SUBSCRIBED_ON_THEMES.format(tags_pretty_list)

    if not answer:
        answer = Messages.NOT_FOUND_SUBSCRIPTIONS

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=answer,
        parse_mode="HTML"
    )

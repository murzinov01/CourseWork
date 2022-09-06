import logging

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
)
from telegram.ext.filters import TEXT, COMMAND, Regex

from bot.database import HabrDB
from bot.keyboards import APPROVE_KEYBOARD, FINDER_KEYBOARD, ShortCommands, KeyboardButtons
from bot.messages import Messages, is_say_hello, get_hello_msg
from bot.search import show_menu, show_article, paginate_page
import config

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_chat.first_name
    await context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.START.format(user_name))


async def _help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.HELP)


async def find_articles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Давай выберем, как будем искать",
        reply_markup=FINDER_KEYBOARD,
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    user_id = update.message.from_user["id"]
    user_name = update.effective_chat.first_name
    habr_db = HabrDB()
    logging.info(f"| {user_id} | {user_name} | {user_msg}|")

    if said_hello := is_say_hello(user_msg):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=get_hello_msg(user_name))

    if user_info := await habr_db.find_user(user_id):
        action = user_info["action"]
        if action:
            if action == "find_by_string":
                return await show_menu(update, context)
            elif action == "choose_article":
                titles_on_page = await habr_db.find_titles_on_page(user_id)
                if user_msg == KeyboardButtons.CLOSE:
                    await habr_db.update_user(user_id, {"action": None})
                    return await context.bot.send_message(
                        chat_id=update.effective_chat.id, text="Заканчиваю поиск", reply_markup=ReplyKeyboardRemove()
                    )
                elif user_msg in titles_on_page:
                    return await show_article(update, context)
                elif user_msg in (KeyboardButtons.LEFT, KeyboardButtons.RIGHT):
                    return await paginate_page(update, context)

    if "иск" in user_msg or "най" in user_msg or "ище" in user_msg:
        answer = Messages.FIND
        reply_markup = APPROVE_KEYBOARD
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer, reply_markup=reply_markup)
    elif "уведом" in user_msg:
        answer = Messages.NOTIFICATION
        reply_markup = APPROVE_KEYBOARD
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer, reply_markup=reply_markup)
    else:
        if not said_hello:
            answer = Messages.DEFAULT
            reply_markup = None
            await context.bot.send_message(chat_id=update.effective_chat.id, text=answer, reply_markup=reply_markup)


async def yes_no_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == ShortCommands.YES:
        await find_articles(update, context)
    elif query.data == ShortCommands.NO:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.MISUNDERSTAND_SEARCH)


async def find_by_theme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Сорри, Бро, я пока так не умею( ", reply_markup=ReplyKeyboardRemove()
    )


async def find_by_string(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user["id"]
    await HabrDB().update_user(user_id, {"action": "find_by_string"})

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=Messages.SIMPLE_SEARCH, reply_markup=ReplyKeyboardRemove()
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(config.TOKEN).build()

    messages_handler = MessageHandler(TEXT & (~COMMAND), message_handler)
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", _help)
    find_articles_handler = CommandHandler("find_articles", find_articles)
    find_by_theme_handler = MessageHandler(Regex(r"Поиск по фильтрам"), find_by_theme)
    find_by_string_handler = MessageHandler(Regex(r"Обычный поиск"), find_by_string)

    application.add_handler(CallbackQueryHandler(yes_no_button))
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(find_articles_handler)
    application.add_handler(find_by_theme_handler)
    application.add_handler(find_by_string_handler)
    application.add_handler(messages_handler)

    application.run_polling()

from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards import FINDER_KEYBOARD, SUBSCRIBE_FINDER
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
        reply_markup=SUBSCRIBE_FINDER,
    )

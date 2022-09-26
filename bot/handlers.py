import logging

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from bot.constants import SUPPORTED_HABR_THEMES, HABR_THEMES_RU
from bot.database import HabrDB
from bot.keyboards import (
    ShortCommands,
    KeyboardButtons,
    SubscribeOptions,
    CHOOSE_THEME_KEYBOARD,
    APPROVE_NOTIFY_KEYBOARD,
    APPROVE_SEARCH_KEYBOARD,
    APPROVE_SUBS_LIST_KEYBOARD,
    APPROVE_HELP_KEYBOARD,
    APPROVE_DELETE_KEYBOARD,
    create_choose_theme_unsubscribed_keyboard,
    create_choose_author_unsubscribed_keyboard,
    create_choose_tag_subscribed_keyboard,
    create_choose_tag_unsubscribed_keyboard,
)
from bot.messages import Messages, is_say_hello, get_hello_msg
from bot.search import show_menu, show_article, paginate_page
from bot.short_commands import find_articles, subscribe, show_subscriptions, _help


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    user_id = update.effective_chat.id
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
                        chat_id=update.effective_chat.id, text=Messages.END_SEARCH, reply_markup=ReplyKeyboardRemove()
                    )
                elif user_msg in titles_on_page:
                    return await show_article(update, context)
                elif user_msg in (KeyboardButtons.LEFT, KeyboardButtons.RIGHT):
                    return await paginate_page(update, context)
            elif action == "specify_author":
                await habr_db.subscribe_on_author(user_id, author=user_msg)
                await habr_db.update_user(user_id, {"action": None})
                return await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=Messages.SUBSCRIBED_AUTHOR.format(user_msg),
                    parse_mode="HTML",
                )
            elif action == "specify_tag":
                await habr_db.subscribe_on_tag(user_id, tag=user_msg)
                await habr_db.update_user(user_id, {"action": None})
                return await context.bot.send_message(
                    chat_id=update.effective_chat.id, text=Messages.SUBSCRIBED_TAG.format(user_msg), parse_mode="HTML"
                )

    user_msg = user_msg.lower()
    if "иск" in user_msg or "най" in user_msg or "ище" in user_msg:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=Messages.FIND, reply_markup=APPROVE_SEARCH_KEYBOARD
        )
    elif "спис" in user_msg and ("уведом" in user_msg or "подпис" in user_msg or "оповещ" in user_msg):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=Messages.SUBSCRIPTIONS_LIST, reply_markup=APPROVE_SUBS_LIST_KEYBOARD
        )
    elif "уведом" in user_msg or "подпис" in user_msg or "оповещ" in user_msg:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=Messages.NOTIFICATION, reply_markup=APPROVE_NOTIFY_KEYBOARD
        )
    elif "помо" in user_msg or "help" in user_msg or "хэлп" in user_msg:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=Messages.NEED_HELP, reply_markup=APPROVE_HELP_KEYBOARD
        )
    else:
        if not said_hello:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.DEFAULT, reply_markup=None)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = update.effective_chat.id
    habr_db = HabrDB()
    await query.answer()
    if q_data := query.data:
        # Yes/No buttons
        if q_data == ShortCommands.SEARCH_YES:
            # await find_articles(update, context)
            await find_by_string(update, context)
        elif q_data == ShortCommands.NOTIFY_YES:
            await subscribe(update, context)
        elif q_data == ShortCommands.SUBS_LIST_YES:
            await show_subscriptions(update, context)
        elif q_data == ShortCommands.HELP_YES:
            await _help(update, context)
        elif q_data == ShortCommands.DELETE_YES:
            await habr_db.delete_all_subscriptions(user_id)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.ALL_DELETED)
        elif q_data == ShortCommands.NO:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.MISUNDERSTAND_SEARCH)

        # Notification parameter buttons
        elif q_data == SubscribeOptions.TAG:
            await habr_db.update_user(user_id, {"action": "specify_tag"})
            tags_num = 30
            tags = await habr_db.find_most_popular_tags(tags_num)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=Messages.SPECIFY_TAG.format(tags_num),
                reply_markup=create_choose_tag_subscribed_keyboard(tags),
                parse_mode="HTML",
            )
        elif q_data == SubscribeOptions.UN_TAG:
            user_entry = await habr_db.find_user(user_id, projection={"subscribe_on_tag": 1})
            user_tags = user_entry.get("subscribe_on_tag", [])
            if user_tags:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=Messages.CHOOSE_TAG,
                    reply_markup=create_choose_tag_unsubscribed_keyboard(user_tags),
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=Messages.NOT_FOUND_TAG_SUBSCRIPTIONS,
                )
        elif q_data == SubscribeOptions.AUTHOR:
            await habr_db.update_user(user_id, {"action": "specify_author"})
            await context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.SPECIFY_AUTHOR)
        elif q_data == SubscribeOptions.UN_AUTHOR:
            user_entry = await habr_db.find_user(user_id, projection={"subscribe_on_author": 1})
            user_authors = user_entry.get("subscribe_on_author", [])
            if user_authors:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=Messages.CHOOSE_AUTHOR,
                    reply_markup=create_choose_author_unsubscribed_keyboard(user_authors),
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=Messages.NOT_FOUND_AUTHOR_SUBSCRIPTIONS,
                )
        elif q_data == SubscribeOptions.THEME:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=Messages.CHOOSE_THEME, reply_markup=CHOOSE_THEME_KEYBOARD
            )
        elif q_data == SubscribeOptions.UN_THEME:
            user_entry = await habr_db.find_user(user_id, projection={"subscribe_on_theme": 1})
            user_themes = user_entry.get("subscribe_on_theme", [])
            if user_themes:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=Messages.CHOOSE_THEME,
                    reply_markup=create_choose_theme_unsubscribed_keyboard(user_themes),
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=Messages.NOT_FOUND_THEME_SUBSCRIPTIONS,
                )
        elif q_data == SubscribeOptions.ALL:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=Messages.IS_SURE_TO_DELETE,
                reply_markup=APPROVE_DELETE_KEYBOARD,
                parse_mode="HTML",
            )

        # HabrThemes buttons
        elif q_data in SUPPORTED_HABR_THEMES:
            await HabrDB().subscribe_on_theme(user_id, q_data)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=Messages.SUBSCRIBED_THEME.format(HABR_THEMES_RU.get(q_data)),
                parse_mode="HTML",
            )
        elif (q_data_stripped := q_data.lstrip("_")) in SUPPORTED_HABR_THEMES:
            await HabrDB().unsubscribe_on_theme(user_id, q_data_stripped)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=Messages.UNSUBSCRIBED_THEME.format(HABR_THEMES_RU.get(q_data_stripped)),
                parse_mode="HTML",
            )

        # HabrAuthors buttons
        elif "author_" in q_data:
            author = q_data.replace("author_", "")
            await HabrDB().unsubscribe_on_author(user_id, author)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=Messages.UNSUBSCRIBED_AUTHOR.format(author),
                parse_mode="HTML",
            )

        # HabrTags buttons
        elif "_tag" in q_data:
            await habr_db.update_user(user_id, {"action": None})
            tag = q_data.replace("_tag", "")
            await HabrDB().subscribe_on_tag(user_id, tag)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=Messages.SUBSCRIBED_TAG.format(tag),
                parse_mode="HTML",
            )
        elif "tag_" in q_data:
            tag = q_data.replace("tag_", "")
            await HabrDB().unsubscribe_on_tag(user_id, tag)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=Messages.UNSUBSCRIBED_TAG.format(tag),
                parse_mode="HTML",
            )


async def find_by_theme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=Messages.I_CAN_NOT_DO_THIS, reply_markup=ReplyKeyboardRemove()
    )


async def find_by_string(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    await HabrDB().update_user(user_id, {"action": "find_by_string"})

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=Messages.SIMPLE_SEARCH, reply_markup=ReplyKeyboardRemove()
    )

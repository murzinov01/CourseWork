from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class ShortCommands:
    YES = "yes"
    NO = "no"


class SubscribeOptions:
    TAG = "tag"
    AUTHOR = "author"
    THEME = "theme"


class KeyboardButtons:
    CLOSE = "❌"
    LEFT = "◀"
    RIGHT = "▶"


APPROVE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Да", callback_data=ShortCommands.YES),
            InlineKeyboardButton("Нет", callback_data=ShortCommands.NO),
        ]
    ],
)

FINDER_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Поиск по фильтрам"),
            KeyboardButton(text="Обычный поиск"),
        ]
    ],
    resize_keyboard=True,
)


SUBSCRIBE_FINDER = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Тэг", callback_data=SubscribeOptions.TAG),
            InlineKeyboardButton(text="Автор", callback_data=SubscribeOptions.AUTHOR),
            InlineKeyboardButton(text="Тема", callback_data=SubscribeOptions.THEME),
        ]
    ]
)


def generate_articles_keyboard(articles: list, left: int, right: int) -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=article["title"])] for article in articles[left:right]]
    keyboard.append(
        [
            KeyboardButton(text=KeyboardButtons.LEFT),
            KeyboardButton(text=KeyboardButtons.CLOSE),
            KeyboardButton(text=KeyboardButtons.RIGHT),
        ]
    )
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )

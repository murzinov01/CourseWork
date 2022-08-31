from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class ShortCommands:
    YES = "yes"
    NO = "no"


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

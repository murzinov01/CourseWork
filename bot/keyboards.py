from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from bot.constants import ShortCommands, SubscribeOptions, HabrThemes, HABR_THEMES_RU, KeyboardButtons

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


SUBSCRIBE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Тэг", callback_data=SubscribeOptions.TAG),
            InlineKeyboardButton(text="Автор", callback_data=SubscribeOptions.AUTHOR),
            InlineKeyboardButton(text="Тема", callback_data=SubscribeOptions.THEME),
        ]
    ]
)

UNSUBSCRIBE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Тэг", callback_data=SubscribeOptions.UN_TAG),
            InlineKeyboardButton(text="Автор", callback_data=SubscribeOptions.UN_AUTHOR),
            InlineKeyboardButton(text="Тема", callback_data=SubscribeOptions.UN_THEME),
        ],
        [
            InlineKeyboardButton(text="Убрать все оповещения", callback_data=SubscribeOptions.ALL),
        ],
    ]
)

CHOOSE_THEME_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=HABR_THEMES_RU.get(HabrThemes.DEVELOP), callback_data=HabrThemes.DEVELOP),
            InlineKeyboardButton(text=HABR_THEMES_RU.get(HabrThemes.ADMIN), callback_data=HabrThemes.ADMIN),
        ],
        [
            InlineKeyboardButton(text=HABR_THEMES_RU.get(HabrThemes.DESIGN), callback_data=HabrThemes.DESIGN),
            InlineKeyboardButton(text=HABR_THEMES_RU.get(HabrThemes.MANAGEMENT), callback_data=HabrThemes.MANAGEMENT),
        ],
        [
            InlineKeyboardButton(text=HABR_THEMES_RU.get(HabrThemes.MARKETING), callback_data=HabrThemes.MARKETING),
            InlineKeyboardButton(text=HABR_THEMES_RU.get(HabrThemes.POPSCI), callback_data=HabrThemes.POPSCI),
        ],
    ]
)

CHOOSE_THEME_UNSUBSCRIBED_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=HABR_THEMES_RU.get(HabrThemes.DEVELOP), callback_data=HabrThemes.DEVELOP_UNSUBSCRIBED
            ),
            InlineKeyboardButton(
                text=HABR_THEMES_RU.get(HabrThemes.ADMIN), callback_data=HabrThemes.ADMIN_UNSUBSCRIBED
            ),
        ],
        [
            InlineKeyboardButton(
                text=HABR_THEMES_RU.get(HabrThemes.DESIGN), callback_data=HabrThemes.DESIGN_UNSUBSCRIBED
            ),
            InlineKeyboardButton(
                text=HABR_THEMES_RU.get(HabrThemes.MANAGEMENT), callback_data=HabrThemes.MANAGEMENT_UNSUBSCRIBED
            ),
        ],
        [
            InlineKeyboardButton(
                text=HABR_THEMES_RU.get(HabrThemes.MARKETING), callback_data=HabrThemes.MARKETING_UNSUBSCRIBED
            ),
            InlineKeyboardButton(
                text=HABR_THEMES_RU.get(HabrThemes.POPSCI), callback_data=HabrThemes.POPSCI_UNSUBSCRIBED
            ),
        ],
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
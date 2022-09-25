from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from bot.constants import ShortCommands, SubscribeOptions, HabrThemes, HABR_THEMES_RU, KeyboardButtons


def generate_yes_no_keyboard(yes_key: str, no_key: str = ShortCommands.NO) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Да", callback_data=yes_key),
                InlineKeyboardButton("Нет", callback_data=no_key),
            ]
        ],
    )


APPROVE_SEARCH_KEYBOARD = generate_yes_no_keyboard(yes_key=ShortCommands.SEARCH_YES)
APPROVE_NOTIFY_KEYBOARD = generate_yes_no_keyboard(yes_key=ShortCommands.NOTIFY_YES)
APPROVE_SUBS_LIST_KEYBOARD = generate_yes_no_keyboard(yes_key=ShortCommands.SUBS_LIST_YES)
APPROVE_HELP_KEYBOARD = generate_yes_no_keyboard(yes_key=ShortCommands.HELP_YES)
APPROVE_DELETE_KEYBOARD = generate_yes_no_keyboard(yes_key=ShortCommands.DELETE_YES)


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


def create_choose_theme_unsubscribed_keyboard(themes: list[str]):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=HABR_THEMES_RU.get(theme), callback_data="_" + theme)
            ] for theme in themes
        ]
    )


def create_choose_author_unsubscribed_keyboard(authors: list[str]):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=author, callback_data="author_" + author)
            ] for author in authors
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

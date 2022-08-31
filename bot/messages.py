import random


class Messages:
    START = (
        "Привет, {}!\n"
        "Я помогу тебе находить любые статьи на хабре 🔍, \nлибо получать уведомления о появлении новых 🔔!\n"
        "Напиши /help, чтобы узнать о всех моих возможностях! 😊"
    )
    HELP = (
        "Вот, что я умею:\n"
        "● /start - Начни со мной диалог!\n"
        "● /help - Когда нужна будет помощь!\n"
        "● /find_articles - Поиск по статьям на Хабре 🔍\n"
    )
    DEFAULT = "Упс! Кажется, я тебя не правильно понял, попробуй сформулировать по-другому!"
    FIND = "Ты хочешь найти статьи на хабре?"
    NOTIFICATION = (
        "Ты хочешь получать уведомления о выходе новых статей определенных автор или на выбранные тобой темы?"
    )
    SIMPLE_SEARCH = "Напиши то, что хочешь найти 🔍"
    MISUNDERSTAND_SEARCH = "Ууупсс, мой косяк. Кажется я тебя не так понял. Давай попробуем ещё раз)"


GREETINGS = {
    'привет', 'доброе утро', 'здравствуйте', 'hello', 'hello,', 'hi',
    'добрый вечер', 'ассаламу алейкум', 'ассаляму алейкум', 'вечер',
    'вечер добрый', 'всем привет', 'день добрый', 'доброе утро', 'добрый день'
}

BOT_GREETINGS = [
    "Привет, {}, чем я могу помочь?",
    "Привет, {}! Я твой помощник для поиска по хабру! Чем я могу помочь?",
    "Привет, {}! Я самый лучший бот-искатель! Что отыщем в этот раз?",
    "Я так долго тебя ждал, {}. Давай уже отыщем что-нибудь!",
]

WAIT_MESSAGES = [
    "Хммм, такое я ещё не искал, подожди секундочку ⌛",
    "Ух ты! Такое я ещё не видал... Уже ищу 🤔"
    "Я конечно быстро ищу, но я не флеш. 🙃 Подожди немного, пожалуйста!"
]


def is_say_hello(user_msg: str) -> bool:
    user_msg = user_msg.lower()
    for greeting in GREETINGS:
        if greeting in user_msg:
            return True
    return False


def get_hello_msg(user_name: str) -> str:
    return BOT_GREETINGS[random.randint(0, len(BOT_GREETINGS) - 1)].format(user_name)


def get_wait_msg() -> str:
    return WAIT_MESSAGES[random.randint(0, len(WAIT_MESSAGES) - 1)]

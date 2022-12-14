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
        "● /subscribe - Оформить подписку на получение новых статей на хабре 🔔\n"
        "● /unsubscribe - Отключи подписку на получение новых статей на хабре 🔕\n"
        "● /show_subscriptions - Посмотри список своих актуальных подписок 📋\n"
    )
    DEFAULT = "Упс! Кажется, я тебя не правильно понял, попробуй сформулировать по-другому!"
    FIND = "Ты хочешь найти статьи на хабре?"
    NOTIFICATION = "Ты хочешь быть вкурсе самых свежих статей и новостей Хабра?"
    SIMPLE_SEARCH = "Напиши то, что хочешь найти 🔍"
    MISUNDERSTAND_SEARCH = "Ууупсс, мой косяк. Кажется я тебя не так понял. Давай попробуем ещё раз)"
    I_CAN_NOT_DO_THIS = "Сорри, Бро, я пока так не умею("
    END_SEARCH = "Заканчиваю поиск"
    HOW_SEARCH = "Давай выберем, как будем искать"
    HOW_NOTIFY = "Давай выберем, по какому параметру я буду оповещать тебя."
    CAN_NOT_FIND = "Кажется, я ничего не смог найти, попробуй переформулировать по-другому"
    WAIT_PLEASE = "Подожди-ка, мне нужно ещё поискать"
    FIND_RESULT = "Вот, что я нашёл"
    CHOOSE_THEME = "А теперь выбери тему"
    CHOOSE_AUTHOR = "А теперь выбери автора"
    CHOOSE_TAG = "А теперь выбери тэг"
    SUBSCRIBED_THEME = (
        'Подписка на тему "<b>{}</b>" оформлена. Я буду оповещать тебя, когда будут появляться новые статьи! 😉'
    )
    UNSUBSCRIBED_THEME = (
        'Подписка на тему "<b>{}</b>" отключена. Теперь я не буду присылать тебе оповещения о статьях на эту тему 👌'
    )
    SUBSCRIBED_AUTHOR = (
        'Подписка на автора "<b>{}</b>" оформлена. Я буду оповещать тебя, когда будут появляться новые статьи! 😉'
    )
    UNSUBSCRIBED_AUTHOR = (
        'Подписка на автора "<b>{}</b>" отключена. Теперь я не буду присылать тебе оповещения о статьях этого автора 👌'
    )
    SUBSCRIBED_TAG = (
        'Подписка по тэгу "<b>{}</b>" оформлена. Я буду оповещать тебя, когда будут появляться новые статьи! 😉'
    )
    UNSUBSCRIBED_TAG = (
        'Подписка по тэгу "<b>{}</b>" отключена. Теперь я не буду присылать тебе оповещения о статьях по этому тэгу 👌'
    )
    UNSUBSCRIBE = "Выбери по какому параметру мне выключить оповещения."
    NOTIFY = "Привет! Кажется я нашёл что-то новенькое для тебя!\n"
    SUBSCRIBED_ON_THEMES = "<b>Темы:</b>\n"
    SUBSCRIBED_ON_AUTHORS = "<b>Авторы:</b>\n"
    SUBSCRIBED_ON_TAGS = "<b>Тэги:</b>\n"
    FOUND_SUBSCRIPTIONS = "Вот список твоих подписок:\n"
    NOT_FOUND_SUBSCRIPTIONS = (
        "Кажется, ты ещё не подписался ни на одну рассылку ☹\nПодпишись и читай самые свежие статьи Хабра первым! 😏"
    )
    NOT_FOUND_THEME_SUBSCRIPTIONS = (
        "Кажется, ты ещё не подписался на рассылку по теме ☹\nПодпишись и читай самые свежие статьи Хабра первым! 😏"
    )
    NOT_FOUND_AUTHOR_SUBSCRIPTIONS = (
        "Кажется, ты не подписан ни на одного автора ☹\nПодпишись и читай самые свежие статьи Хабра первым! 😏"
    )
    NOT_FOUND_TAG_SUBSCRIPTIONS = "Кажется, ты не подписан на получение статей ни по одному тэгу ☹\nПодпишись и читай самые свежие статьи Хабра первым! 😏"
    SUBSCRIPTIONS_LIST = "Ты хочешь получить список твоих пидписок?"
    NEED_HELP = "Кажется тебе нужна помощь? Расскзать, что я умею?"
    IS_SURE_TO_DELETE = (
        "Ты уверен, что хочешь отписаться от рассылки новых статей <b>по всем параметрам</b> (авторы, темы, тэги?)"
    )
    ALL_DELETED = "Теперь список твоих подписок пуст!"
    SPECIFY_AUTHOR = "Напиши имя автора, новости которого ты хочешь получать от меня!"
    SPECIFY_TAG = "Я нашел <b>{}</b> самых популярных тэгов 😊.\nТы можешь <b>выбрать тэг</b> из списка, либо <b>написать свой</b>."


GREETINGS = {
    "привет",
    "доброе утро",
    "здравствуйте",
    "hello",
    "hello,",
    "hi",
    "добрый вечер",
    "ассаламу алейкум",
    "ассаляму алейкум",
    "вечер",
    "вечер добрый",
    "всем привет",
    "день добрый",
    "доброе утро",
    "добрый день",
}

BOT_GREETINGS = [
    "Привет, {}, чем я могу помочь?",
    "Привет, {}! Я твой помощник для поиска по хабру! Чем я могу помочь?",
    "Привет, {}! Со мной ты будешь вкурсе всех самых новых статей Хабра!",
]

WAIT_MESSAGES = [
    "Хммм, такое я ещё не искал, подожди секундочку ⌛",
    "Ух ты! Такое я ещё не видал... Уже ищу 🤔" "Я конечно быстро ищу, но я не флеш. 🙃 Подожди немного, пожалуйста!",
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

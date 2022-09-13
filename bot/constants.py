class ShortCommands:
    YES = "yes"
    NO = "no"


class SubscribeOptions:
    TAG = "tag"
    AUTHOR = "author"
    THEME = "theme"

    UN_TAG = "un_tag"
    UN_AUTHOR = "un_author"
    UN_THEME = "un_theme"
    ALL = "all"


class KeyboardButtons:
    CLOSE = "❌"
    LEFT = "◀"
    RIGHT = "▶"


class HabrThemes:
    DEVELOP = "develop"
    DESIGN = "design"
    ADMIN = "admin"
    MANAGEMENT = "management"
    MARKETING = "marketing"
    POPSCI = "popsci"

    DEVELOP_UNSUBSCRIBED = "_develop"
    DESIGN_UNSUBSCRIBED = "_design"
    ADMIN_UNSUBSCRIBED = "_admin"
    MANAGEMENT_UNSUBSCRIBED = "_management"
    MARKETING_UNSUBSCRIBED = "_marketing"
    POPSCI_UNSUBSCRIBED = "_popsci"


HABR_THEMES_RU = {
    HabrThemes.DEVELOP: "Разработка",
    HabrThemes.DESIGN: "Дизайн",
    HabrThemes.ADMIN: "Администрование",
    HabrThemes.MANAGEMENT: "Менеджмент",
    HabrThemes.MARKETING: "Маркетинг",
    HabrThemes.POPSCI: "Научпоп",
}

SUPPORTED_HABR_THEMES = set(key for key in HABR_THEMES_RU.keys())

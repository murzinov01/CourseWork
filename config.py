HABR_URL = "https://habr.com/ru/flows/design"

# Mongo
MONGO_URL = "mongodb://docker:mongopw@localhost:49153"
DATABASE = "Articles"
HABR_ARTICLES_COLL = "HabrArticles"
USERS_COLL = "Users"
TAGS_COLL = "Tags"

# Redis
REDIS_HOST = "localhost"
REDIS_PORT = "49154"
REDIS_PASSWORD = "redispw"
REDIS_DEFAULT_TTL = 86400

# RabbitMQ
RABBIT_HOST = "localhost"
RABBIT_PORT = "49156"
RABBIT_PASSWORD = "guest"


# Schedulers
PARSE_PERIOD = 12  # Запускать шедулер каждые 12 часов
PARS_LAST_DAY = 1  # Искать записи за последний день


# Bot settings
TOKEN = "5511032264:AAGUB8xAw4UOJdt9ZA1GyTGhbzPsne3irWA"
ARTICLES_PER_PAGE = 3
SEND_MESSAGE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# Notifications
PARSE_FOR_NOTIFY_PERIOD = 10  # Минуты
NOTIFICATIONS_QUEUE_COLL = "NotificationsQueue"

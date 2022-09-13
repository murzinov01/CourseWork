HABR_URL = "https://habr.com/ru/flows/design"

# Mongo
MONGO_URL = "mongodb://docker:mongopw@localhost:49153"
DATABASE = "Articles"
HABR_ARTICLES_COLL = "HabrArticles"
USERS_COLL = "Users"

# Redis
REDIS_HOST = "localhost"
REDIS_PORT = "49154"
REDIS_PASSWORD = "redispw"
REDIS_DEFAULT_TTL = 86400


# Schedulers
RUN_EVERY_HOURS_NUM = 12  # Запускать шедулер каждые 12 часов
UPDATE_FOR_DAYS_NUM = 1  # Искать записи за последний день


# Bot settings
TOKEN = "5511032264:AAGUB8xAw4UOJdt9ZA1GyTGhbzPsne3irWA"
ARTICLES_PER_PAGE = 3

import asyncio
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from aredis import StrictRedis

import config
from parsers.habr_selenium_parser import Article
from pymongo import MongoClient


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class HabrDB(metaclass=Singleton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        event_loop = asyncio.get_event_loop()
        client = AsyncIOMotorClient(
            config.MONGO_URL,
            io_loop=event_loop,
        )
        habr_db = client[config.DATABASE]
        self.users_collection = habr_db[config.USERS_COLL]
        self.tags_collection = habr_db[config.TAGS_COLL]

    async def find_user(self, user_id: object, projection=None):
        return await self.users_collection.find_one({"id": user_id}, projection=projection)

    async def update_user(self, user_id: object, data: dict):
        return await self.users_collection.update_one({"id": user_id}, {"$set": data}, upsert=True)

    async def subscribe_on_theme(self, user_id: object, theme: str):
        return await self.users_collection.update_one({"id": user_id}, {"$addToSet": {"subscribe_on_theme": theme}})

    async def unsubscribe_on_theme(self, user_id: object, theme: str):
        return await self.users_collection.update_one(
            {"id": user_id}, {"$pull": {"subscribe_on_theme": {"$in": [theme]}}}
        )

    async def subscribe_on_author(self, user_id: object, author: str):
        return await self.users_collection.update_one({"id": user_id}, {"$addToSet": {"subscribe_on_author": author}})

    async def unsubscribe_on_author(self, user_id: object, author: str):
        return await self.users_collection.update_one(
            {"id": user_id}, {"$pull": {"subscribe_on_author": {"$in": [author]}}}
        )

    async def subscribe_on_tag(self, user_id: object, tag: str):
        return await self.users_collection.update_one({"id": user_id}, {"$addToSet": {"subscribe_on_tag": tag}})

    async def unsubscribe_on_tag(self, user_id: object, tag: str):
        return await self.users_collection.update_one({"id": user_id}, {"$pull": {"subscribe_on_tag": {"$in": [tag]}}})

    async def delete_all_subscriptions(self, user_id: object):
        return await self.users_collection.update_one(
            {"id": user_id}, {"$set": {"subscribe_on_theme": [], "subscribe_on_author": [], "subscribe_on_tag": []}}
        )

    async def find_article_by_title(self, user_id: object, title: str) -> Optional[dict]:
        entry = await self.users_collection.find_one(
            {"id": user_id}, projection={"_id": 0, "articles_on_page": {"$elemMatch": {"title": title}}}
        )
        return entry["articles_on_page"][0] if entry else None

    async def find_titles_on_page(self, user_id: object) -> Optional[list]:
        entry = await self.users_collection.find_one({"id": user_id}, projection={"_id": 0, "titles_on_page": 1})
        return entry.get("titles_on_page", []) if entry else None

    async def find_current_page(self, user_id: object) -> Optional[int]:
        entry = await self.users_collection.find_one({"id": user_id}, projection={"_id": 0, "current_page": 1})
        return entry.get("current_page", 0) if entry else None

    async def find_habr_page(self, user_id: object) -> Optional[int]:
        entry = await self.users_collection.find_one({"id": user_id}, projection={"_id": 0, "habr_page": 1})
        return entry.get("habr_page", 0) if entry else None

    async def find_most_popular_tags(self, tags_num: int = None) -> list[str]:
        tags = []
        async for entry in self.tags_collection.find({}, limit=tags_num):
            tags.append(entry.get("tag"))
        return tags

    @staticmethod
    def find_users_subscribed(article: Article) -> list[object]:
        client = MongoClient(config.MONGO_URL)
        db = client[config.DATABASE]
        users = db[config.USERS_COLL]
        theme = article.theme
        author = article.author
        tags = [tag.get("tag") for tag in article.tags]

        # find users with subscription by theme
        user_ids = set()
        for user in users.find({"subscribe_on_theme": {"$in": [theme]}}, projection={"id": 1}):
            user_ids.add(user.get("id"))
        for user in users.find({"subscribe_on_author": {"$in": [author]}}, projection={"id": 1}):
            user_ids.add(user.get("id"))
        for user in users.find({"subscribe_on_tag": {"$in": tags}}, projection={"id": 1}):
            user_ids.add(user.get("id"))
        return list(user_ids)


class RedisDB(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.client = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, password=config.REDIS_PASSWORD)

    async def set(self, key, value, ttl=config.REDIS_DEFAULT_TTL):
        await self.client.set(key, value, ex=ttl)

    async def get(self, key):
        return await self.client.get(key)

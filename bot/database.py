import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from aredis import StrictRedis
import config


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

    async def find_user(self, user_id):
        return await self.users_collection.find_one({"id": user_id})

    async def update_user(self, user_id, data: dict):
        return await self.users_collection.update_one({"id": user_id}, {"$set": data}, upsert=True)


class RedisDB(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.client = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, password=config.REDIS_PASSWORD)

    async def set(self, key, value, ttl=config.REDIS_DEFAULT_TTL):
        await self.client.set(key, value, ex=ttl)

    async def get(self, key):
        return await self.client.get(key)


loop = asyncio.get_event_loop()
loop.run_until_complete(RedisDB().set("foo", "bar"))

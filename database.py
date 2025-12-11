from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings


client = AsyncIOMotorClient(settings.mongo_uri)
master_db = client[settings.master_db_name]


async def get_master_db():
    return master_db


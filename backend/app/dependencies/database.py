import os
from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


@lru_cache()  # Caches the result of the function to prevent redundant connections.
def get_mongo_client() -> AsyncIOMotorClient:
    """
    Returns an AsyncIOMotorClient instance.
    The function is cached using lru_cache to prevent redundant connections.
    """
    return AsyncIOMotorClient(os.getenv("MONGODB_URI"))


async def get_database() -> AsyncIOMotorDatabase:
    """
    Returns the AsyncIOMotorDatabase object from the MongoDB client.
    """
    client = get_mongo_client()
    return client[os.getenv("MONGO_DB_NAME")]

from motor.motor_asyncio import AsyncIOMotorClient
import os


def get_db_async():
    client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
    try:
        yield client[os.getenv("MONGODB_DBNAME")]
    finally:
        client.close()

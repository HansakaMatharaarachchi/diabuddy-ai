import os

from app.db.mongodb import MongoDB
from dotenv import load_dotenv

load_dotenv("../.env")

# Initialize MongoDB connection
mongo_instance = MongoDB(
    uri=os.getenv("MONGODB_URI"), db_name=os.getenv("MONGODB_DBNAME")
)


# Dependency function to get MongoDB instance
def get_mongo():
    """Get MongoDB instance.

    Returns:
        _type_: MongoDB instance.
    """
    return mongo_instance

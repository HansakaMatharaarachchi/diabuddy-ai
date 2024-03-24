import os

from app.db.mongodb import MongoDB

# Initialize MongoDB connection
mongo_instance = MongoDB(
    uri=os.getenv("MONGODB_URI"), db_name=os.getenv("MONGODB_DBNAME")
)


def get_db():
    """Get MongoDB instance.

    Returns:
        _type_: MongoDB instance.
    """
    return mongo_instance

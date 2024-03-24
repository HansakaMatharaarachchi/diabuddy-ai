import logging

from pymongo import MongoClient
from pymongo.errors import PyMongoError

logger = logging.getLogger(__name__)


class MongoDB:
    def __init__(self, uri: str, db_name: str):
        """Initialize MongoDB instance with given connection uri.

        Args:
            uri (str): mongoDB uri.
            db_name (str): Database name.
        """
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]

            self.user_collection = self.db.get_collection("users")
            self.chat_message_history_collection = self.db.get_collection(
                "chat_message_history"
            )
        except PyMongoError as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            raise

    def get_chat_message_collection(self):
        """Get chat message collection.

        Returns:
            _type_: Collection object.
        """
        return self.chat_message_history_collection

    def get_user_collection(self):
        """Get user collection.

        Returns:
            _type_: Collection object.
        """
        return self.user_collection

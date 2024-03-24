import logging
from typing import List, Optional

from app.models.chat import ChatMessage
from app.models.user import User
from langchain_core.messages import messages_from_dict
from langchain_core.messages.base import message_to_dict
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

    def add_user(self, user: User) -> bool:
        """Add user to the database.

        Args:
            user (User): User object.

        Returns:
            bool: True if user is added successfully, False otherwise.
        """
        try:
            self.user_collection.insert_one(user.dict())
            return True
        except PyMongoError as e:
            logger.error(f"Error adding user: {e}")
            return False

    def get_user(self, id: str) -> Optional[User]:
        """Get user from the database.

        Args:
            id (str): User id.

        Returns:
            Optional[User]: User object if found, None otherwise.
        """
        try:
            user_data = self.user_collection.find_one({"id": id})
            return User(**user_data) if user_data else None
        except PyMongoError as e:
            logger.error(f"Error getting user: {e}")
            return None

    def add_chat_message(self, user_id: str, message: ChatMessage) -> bool:
        """Add chat message to the database.

        Args:
            user_id (str): User id.
            message (ChatMessage): Chat message object.

        Returns:
            bool: True if chat message is added successfully, False otherwise.
        """
        try:
            self.chat_message_history_collection.update_one(
                {"user_id": user_id},
                {"$push": {"messages": message_to_dict(message)}},
                upsert=True,
            )
            return True
        except PyMongoError as e:
            logger.error(f"Error adding chat message: {e}")
            return False

    def get_chat_message_history(self, user_id: str) -> List[ChatMessage]:
        """Get chat message history of the user.

        Args:
            user_id (str): User id.

        Returns:
            List[ChatMessage]: List of chat messages.
        """
        try:
            user = self.chat_message_history_collection.find_one({"user_id": user_id})
            return messages_from_dict(user.get("messages", [])) if user else []
        except PyMongoError as e:
            logger.error(f"Error getting chat message history: {e}")
            return []

    def clear_chat_message_history(self, user_id: str) -> bool:
        """Clear chat message history of the user.

        Args:
            user_id (str): User id.

        Returns:
            bool: True if chat message history is cleared successfully, False otherwise.
        """
        try:
            self.chat_message_history_collection.update_one(
                {"user_id": user_id}, {"$set": {"messages": []}}, upsert=True
            )
            return True
        except PyMongoError as e:
            logger.error(f"Error clearing chat message history: {e}")
            return False

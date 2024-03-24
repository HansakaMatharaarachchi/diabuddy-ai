import logging
from typing import List

from app.db.mongodb import MongoDB
from app.models.chat import ChatMessage
from langchain_core.messages import messages_from_dict
from langchain_core.messages.base import message_to_dict

logger = logging.getLogger(__name__)


class ChatHistoryService:
    def __init__(self, db: MongoDB):
        """Initialize ChatHistoryService.

        Args:
            db (MongoDB): MongoDB instance.
        """
        self.message_collection = db.get_chat_message_collection()

    def add_message(self, user_id: str, message: ChatMessage) -> bool:
        """Add chat message to the user.

        Args:
            user_id (str): User id.
            message (ChatMessage): Chat message object.

        Returns:
            bool: True if chat message is added successfully, False otherwise.
        """
        try:
            self.message_collection.update_one(
                {"user_id": user_id},
                {"$push": {"messages": message_to_dict(message)}},
                upsert=True,
            )
            return True
        except Exception as e:
            logger.error(f"Error adding chat message: {e}")
            return False

    def get_message_history(self, user_id: str) -> List[ChatMessage]:
        """Get chat message history of the user.

        Args:
            user_id (str): User id.

        Returns:
            List[ChatMessage]: List of chat messages.
        """
        try:
            user = self.message_collection.find_one({"user_id": user_id})
            return messages_from_dict(user.get("messages", [])) if user else []
        except Exception as e:
            logger.error(f"Error getting chat message history: {e}")
            return []

    def clear_message_history(self, user_id: str) -> bool:
        """Clear chat message history of the user.

        Args:
            user_id (str): User id.

        Returns:
            bool: True if chat message history is cleared successfully, False otherwise.
        """
        try:
            self.message_collection.update_one(
                {"user_id": user_id}, {"$set": {"messages": []}}, upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Error clearing chat message history: {e}")
            return False

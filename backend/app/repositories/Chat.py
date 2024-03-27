from typing import List

from app.dependencies.database import get_database
from app.models.chat import ChatMessage
from fastapi import Depends
from langchain_core.messages import messages_from_dict
from langchain_core.messages.base import message_to_dict
from motor.motor_asyncio import AsyncIOMotorDatabase


class ChatRepository:

    def __init__(self, db: AsyncIOMotorDatabase = Depends(get_database)):
        """Initialize chat repository.

        Args:
            db (MongoDB): MongoDB instance.
        """
        self.db = db
        self.message_collection = self.db["chat_message_history_collection"]

    async def add_message(self, user_id: str, message: ChatMessage) -> ChatMessage:
        """Add chat message to the user.

        Args:
            user_id (str): ID of the user.
            message (ChatMessage): Chat message.

        Raises:
            Exception: Failed to add message to the user.

        Returns:
            ChatMessage: Chat message.
        """
        result = await self.message_collection.update_one(
            {"user_id": user_id},
            {"$push": {"messages": message_to_dict(message)}},
            upsert=True,
        )

        if not result.acknowledged:
            raise Exception("Failed to add message to the user")

        return message

    async def get_messages_by_user_id(self, user_id: str) -> List[ChatMessage] | None:
        """Get chat messages of the user.

        Args:
            user_id (str): ID of the user.

        Returns:
            List[ChatMessage] | None: List of chat messages or None if user has no messages.
        """
        user_messages = await self.message_collection.find_one({"user_id": user_id})

        if not user_messages:
            return None

        return messages_from_dict(user_messages.get("messages", []))

    async def delete_chats_by_user_id(self, user_id: str):
        """Delete chat messages of the user.

        Args:
            user_id (str): ID of the user.
        """
        await self.message_collection.delete_one({"user_id": user_id})

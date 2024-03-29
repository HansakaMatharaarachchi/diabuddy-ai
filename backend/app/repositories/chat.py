from typing import List

from app.dependencies.database import get_database
from fastapi import Depends
from langchain_core.messages import messages_from_dict
from langchain_core.messages.base import BaseMessage, message_to_dict
from motor.motor_asyncio import AsyncIOMotorDatabase


class ChatRepository:
    def __init__(self, db: AsyncIOMotorDatabase = Depends(get_database)):
        """Initialize chat repository.

        Args:
            db (MongoDB): MongoDB instance.
        """
        self.db = db
        self.message_collection = self.db["chat_message_history_collection"]

    async def add_messages(
        self, user_id: str, messages: List[BaseMessage]
    ) -> List[BaseMessage]:
        """Add chat messages to the user.

        Args:
            user_id (str): ID of the user.
            messages (List[BaseMessage]): List of chat messages.

        Raises:
            Exception: Failed to add messages to the user.

        Returns:
            List[BaseMessage]: List of chat messages.
        """
        result = await self.message_collection.update_one(
            {"user_id": user_id},
            {
                "$push": {
                    "messages": {
                        "$each": [message_to_dict(message) for message in messages],
                    }
                }
            },
            upsert=True,
        )

        if not result.acknowledged:
            raise Exception("Failed to add messages to the user")

        return messages

    async def get_messages_by_user_id(self, user_id: str) -> List[BaseMessage] | None:
        """Get chat messages of the user.

        Args:
            user_id (str): ID of the user.

        Returns:
            List[BaseMessage] | None: List of chat messages or None if user has no messages.
        """
        user_messages = await self.message_collection.find_one({"user_id": user_id})

        if not user_messages:
            return None

        return messages_from_dict(user_messages.get("messages", []))

    async def delete_messages_by_user_id(self, user_id: str):
        """Delete chat messages of the user.

        Args:
            user_id (str): ID of the user.
        """
        await self.message_collection.delete_one({"user_id": user_id})

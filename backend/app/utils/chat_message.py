from typing import List

from app.database.database import MongoDB
from app.models.chat import ChatMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage


class MongoDBUserChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, user_id: str, db: MongoDB):
        self.user_id = user_id
        self.db = db

        db.chat_message_history_collection.create_index("user_id", unique=True)

    @property
    def messages(self) -> List[BaseMessage]:
        """Retrieve messages of the user from MongoDB"""
        return self.db.get_chat_message_history(self.user_id)

    def add_message(self, message: BaseMessage) -> None:
        """Append the message to the messages in MongoDB"""
        self.db.add_chat_message(self.user_id, base_message_to_chat_message(message))

    def clear(self) -> None:
        """Clear user chat history from MongoDB"""
        self.db.clear_chat_message_history(self.user_id)


def base_message_to_chat_message(base_message: BaseMessage) -> ChatMessage:
    """Convert BaseMessage to ChatMessage.

    Args:
        base_message (BaseMessage): Base message to convert.

    Returns:
        ChatMessage: Converted ChatMessage.
    """
    return ChatMessage(**base_message.dict())

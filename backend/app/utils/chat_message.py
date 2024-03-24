from typing import List

from app.models.chat import ChatMessage
from app.services.chat_service import ChatService
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage


class MongoDBUserChatMessageHistory(BaseChatMessageHistory):

    def __init__(self, user_id: str, chat_service: ChatService):
        """Initialize the MongoDBUserChatMessageHistory.

        Args:
            user_id (str): User ID.
            chat_history_service (ChatHistoryService): Chat history service.
        """
        self.user_id = user_id
        self.chat_service = chat_service

    @property
    def messages(self) -> List[BaseMessage]:
        """Get the messages.

        Returns:
            List[BaseMessage]: List of messages.
        """
        return self.chat_service.get_messages(self.user_id)

    def add_message(self, message: BaseMessage) -> None:
        """Add a message.

        Args:
            message (BaseMessage): Message to add.
        """
        self.chat_service.add_message(
            self.user_id, base_message_to_chat_message(message)
        )

    def clear(self) -> None:
        """Clear the messages."""
        self.chat_service.clear_messages(self.user_id)


def base_message_to_chat_message(base_message: BaseMessage) -> ChatMessage:
    """Convert BaseMessage to ChatMessage.

    Args:
        base_message (BaseMessage): Base message to convert.

    Returns:
        ChatMessage: Converted ChatMessage.
    """
    return ChatMessage(**base_message.dict())

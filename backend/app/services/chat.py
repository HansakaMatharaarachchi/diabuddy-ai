from app.models.chat import ChatMessage
from app.repositories.Chat import ChatRepository
from fastapi import Depends


class ChatService:
    def __init__(self, chat_repo: ChatRepository = Depends(ChatRepository)):
        """Initialize chat service.

        Args:
            chat_repo (ChatRepository): Chat repository instance.
        """
        self.chat_repo = chat_repo

    async def add_message(self, user_id: str, message: ChatMessage) -> ChatMessage:
        """Add chat message to the user.

        Args:
            user_id (str): ID of the user.
            message (ChatMessage): Chat message.

        Returns:
            ChatMessage: Chat message.
        """
        return await self.chat_repo.add_message(user_id, message)

    async def get_messages(self, user_id: str) -> list[ChatMessage] | None:
        """Get chat messages of the user.

        Args:
            user_id (str): ID of the user.

        Returns:
            List[ChatMessage] | None: List of chat messages or None if user has no messages.
        """
        return await self.chat_repo.get_messages_by_user_id(user_id)

    async def delete_messages(self, user_id: str):
        """Delete chat messages of the user.

        Args:
            user_id (str): ID of the user.
        """
        await self.chat_repo.delete_chats_by_user_id(user_id)

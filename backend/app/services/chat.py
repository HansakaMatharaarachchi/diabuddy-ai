from typing import AsyncGenerator

from app.chains.agentic import agent_executor
from app.exceptions.common import NotFoundException
from app.repositories.chat import ChatRepository
from app.repositories.user import UserRepository
from fastapi import Depends
from langchain_core.messages.base import BaseMessage


class ChatService:
    def __init__(
        self,
        chat_repo: ChatRepository = Depends(ChatRepository),
        user_repo: UserRepository = Depends(UserRepository),
    ):
        """Initialize chat service.

        Args:
            chat_repo (ChatRepository): Chat repository instance.
        """
        self.chat_repo = chat_repo
        self.user_repo = user_repo
        self.rag_agent_executor = agent_executor

    async def stream_ai_response(
        self, user_id: str, query: str
    ) -> AsyncGenerator[str, None]:
        """Streams AI response for given query for a user.

        Args:
            user_id (str): ID of the user.
            query (str): Query to send to AI.

        Returns:
            AsyncGenerator[str, None]: AI response stream.

        Yields:
            Iterator[AsyncGenerator[str, None]]: AI response.
        """

        user = self.user_repo.get_user_by_id(user_id)

        if not user:
            raise NotFoundException("User not found")

        user_data = user.dict(
            include={"nickname", "age", "gender", "diabetes_type", "preferred_language"}
        )

        # Get chat history.
        user_data["chat_history"] = await self.get_messages(user_id) or []

        # Stream AI message chunks.
        async for chunk in self.rag_agent_executor.astream(
            {"input": query, **user_data}
        ):
            ai_response = chunk.get("output")

            if ai_response != None:
                yield ai_response

    async def add_messages(
        self, user_id: str, messages: list[BaseMessage]
    ) -> list[BaseMessage]:
        """Add chat messages for the user.

        Args:
            user_id (str): ID of the user.
            messages (List[BaseMessage]): List of chat messages.

        Returns:
            List[BaseMessage]: List of chat messages.
        """
        return await self.chat_repo.add_messages(user_id, messages)

    async def get_messages(self, user_id: str) -> list[BaseMessage] | None:
        """Get chat messages of the user.

        Args:
            user_id (str): ID of the user.

        Returns:
            List[BaseMessage] | None: List of chat messages or None if user has no messages.
        """
        return await self.chat_repo.get_messages_by_user_id(user_id)

    async def delete_messages(self, user_id: str):
        """Delete chat messages of the user.

        Args:
            user_id (str): ID of the user.
        """
        await self.chat_repo.delete_messages_by_user_id(user_id)

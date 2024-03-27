from typing import Optional

from app.models.user import User
from app.repositories.Chat import ChatRepository
from app.repositories.User import UserRepository
from app.schemas.user import UpdateUser
from fastapi import Depends


class UserService:
    def __init__(
        self,
        user_repo: UserRepository = Depends(UserRepository),
        chat_repo: ChatRepository = Depends(ChatRepository),
    ):
        """Initialize user service

        Args:
            user_repo (UserRepository): The user repository instance
            chat_repo (ChatRepository): The chat repository instance
        """
        self.user_repo = user_repo
        self.chat_repo = chat_repo

    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user

        Args:
            user_id (str): The user_id

        Returns:
            Optional[User]: The user profile or None if the user was not found
        """
        return self.user_repo.get_user_by_id(user_id)

    def update_user(self, user_id: str, data: UpdateUser) -> User | None:
        """Update a user

        Args:
            user_id (str): The user_id
            data (UpdateUser): The data to update

        Returns:
            User | None: The updated user profile or None if the user was not found.
        """
        return self.user_repo.update_user_by_id(user_id, data)

    async def delete_user(self, user_id: str) -> None:
        """Delete a user

        Args:
            user_id (str): The user_id
        """
        try:
            async with await self.chat_repo.db.client.start_session() as session:
                async with session.start_transaction():
                    await self.chat_repo.delete_chats_by_user_id(user_id)
                    self.user_repo.delete_user_by_id(user_id)
                    await session.commit_transaction()
        except Exception as e:
            await session.abort_transaction()
            raise e

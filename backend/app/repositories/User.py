from typing import Optional

from app.dependencies.auth import get_user_manager
from app.models.user import User
from app.schemas.user import UpdateUser
from auth0 import Auth0Error
from auth0.management import Users
from fastapi import Depends


# Exception to raise when user is not found.
class UserNotFound(Exception):
    def __init__(
        self,
        message="User not found",
    ):
        self.message = message
        super().__init__(self.message)


class UserRepository:
    def __init__(self, users: Users = Depends(get_user_manager)):
        """Initialize user repository

        Args:
            users (Users): The User manager instance
        """
        self.users = users

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user

        Args:
            user_id (str): The user_id

        Returns:
            Optional[User]: The user profile or None if the user was not found
        """
        try:
            # Get the user data from Auth0 metadata field.
            user_data = self.users.get(user_id, fields=["user_metadata"]).get(
                "user_metadata", {}
            )
            return User(
                id=user_id,
                **user_data,
            )
        except Auth0Error as ae:
            if ae.status_code == 404:
                return None
            raise ae

    def update_user_by_id(self, user_id: str, data: UpdateUser) -> User | None:
        """Update a user

        Args:
            user_id (str): The user_id
            data (UpdateUser): The data to update

        Returns:
            User | None: The updated user profile or None if the user was not found.
        """
        try:
            user_data = self.users.get(user_id, fields=["user_metadata"]).get(
                "user_metadata", {}
            )

            user_data.update(data.dict(exclude_unset=True))

            self.users.update(
                user_data.get("user_id", user_id),
                {"user_metadata": user_data},
            )
            return self.get_user_by_id(user_id)
        except Auth0Error as ae:
            if ae.status_code == 404:
                raise UserNotFound()
            raise ae

    def delete_user_by_id(self, user_id: str) -> None:
        """Delete a user

        Args:
            user_id (str): The user_id
        """
        try:
            self.users.delete(user_id)
        except Auth0Error as ae:
            if ae.status_code == 404:
                raise UserNotFound()
            raise ae

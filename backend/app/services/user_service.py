import logging
from typing import Optional

from app.models.user import UserProfile
from app.schemas.user import UpdateUserProfile
from auth0 import Auth0Error
from auth0.management import Users
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class IncompleteProfileDetailsException(Exception):
    """Exception raised when user profile is Incomplete."""

    pass


class UserService:
    def __init__(self, users: Users):
        """Initialize user service

        Args:
            users (Users): The User manager instance
        """
        self.users = users

    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get a user's profile

        Args:
            user_id (str): The user_id

        Returns:
            Optional[UserProfile]: The user profile or
            None if the users profile details are not complete
        """
        try:
            user_data = self.users.get(user_id, fields=["user_id", "user_metadata"])
            return UserProfile(
                id=user_data.get("user_id", user_id),
                **user_data.get("user_metadata", {}),
            )
        except Auth0Error as ae:
            if ae.status_code == 404:
                logger.error(f"User not found: {ae}")
                return None
            raise ae
        except ValidationError as ve:
            logger.error(f"User profile details are incomplete: {ve}")
            raise IncompleteProfileDetailsException(
                "User profile details are incomplete"
            )

    def update_user_profile(
        self, user_id: str, data: UpdateUserProfile
    ) -> UserProfile | None:
        """Update a user's profile

        Args:
            user_id (str): The user_id
            data (UpdateUserProfile): The user profile data

        Raises:
            ae: Auth0Error

        Returns:
            UserProfile | None: The updated user profile or None if the user was not found
        """
        try:
            user_data = self.users.get(user_id, fields=["user_id", "user_metadata"])

            user_metadata = user_data.get("user_metadata", {})
            user_metadata.update(data.dict(exclude_unset=True))

            self.users.update(
                user_data.get("user_id", user_id),
                {"user_metadata": user_metadata},
            )

            return UserProfile(id=user_id, **user_metadata)
        except Auth0Error as ae:
            if ae.status_code == 404:
                logger.error(f"User not found: {ae}")
                return None
            raise ae

    def delete_user(self, user_id: str) -> bool:
        """Delete a user

        Args:
            user_id (str): The user_id

        Returns:
            bool: True if the delete was successful, False otherwise.
        """
        try:
            self.users.delete(user_id)
            return True
        except Exception as e:
            logger.error(f"Failed to delete user: {e}")
            return False

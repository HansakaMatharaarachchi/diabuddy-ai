import logging
from typing import Optional

from app.db.mongodb import MongoDB
from app.models.user import User

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: MongoDB):
        """Initialize UserService.

        Args:
            db (MongoDB): MongoDB instance.
        """
        self.user_collection = db.get_user_collection()


def add_user(self, user: User) -> bool:
    """Add user.

    Args:
        user (User): User object.

    Returns:
        bool: True if user is added successfully, False otherwise.
    """
    try:
        self.user_collection.insert_one(user.dict())
        return True
    except Exception as e:
        logger.error(f"Error adding user: {e}")
        return False


def get_user(self, id: str) -> Optional[User]:
    """Get user by id.

    Args:
        id (str): User id.

    Returns:
        Optional[User]: User object if found, None otherwise.
    """
    try:
        user_data = self.user_collection.find_one({"id": id})
        return User(**user_data) if user_data else None
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        return None

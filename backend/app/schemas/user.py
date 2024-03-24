from typing import Optional
from app.models.user import User


class UserCreate(User):
    _id: Optional[str]

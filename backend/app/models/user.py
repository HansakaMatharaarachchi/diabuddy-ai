from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field, root_validator


class Gender(StrEnum):
    MALE = "Male"
    FEMALE = "Female"


class DiabetesType(StrEnum):
    TYPE_1 = "Type 1"
    TYPE_2 = "Type 2"


class Language(StrEnum):
    ENGLISH = "English"


class UserBase(BaseModel):
    nickname: Optional[str]
    age: Optional[int] = Field(None, ge=18, le=100)
    gender: Optional[Gender]
    diabetes_type: Optional[DiabetesType]
    preferred_language: Optional[Language]


class User(UserBase):
    id: str
    is_profile_completed: bool = False

    @root_validator
    def calculate_profile_completed(cls, values):
        # Check if all fields are not None.
        is_profile_completed = all(
            values.get(field) is not None for field in cls.__fields__.keys()
        )
        return {**values, "is_profile_completed": is_profile_completed}

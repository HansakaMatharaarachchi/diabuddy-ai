from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class DiabetesType(str, Enum):
    TYPE_1 = "type 1"
    TYPE_2 = "type 2"


class Language(str, Enum):
    ENGLISH = "english"


class UserProfileBase(BaseModel):
    nickname: str
    age: int
    gender: Gender
    diabetes_type: DiabetesType
    preferred_language: Language


class UserProfile(UserProfileBase):
    id: str

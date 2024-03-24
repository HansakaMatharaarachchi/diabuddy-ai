from enum import Enum

from pydantic import BaseModel, Field


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"


class DiabetesType(str, Enum):
    TYPE_1 = "Type 1"
    TYPE_2 = "Type 2"


class Language(str, Enum):
    ENGLISH = "en"


class User(BaseModel):
    _id: str = Field(alias="id")
    sub: str  # Auth0 user ID
    nickname: str
    age: int = Field(..., gt=18)
    gender: Gender
    diabetes_type: DiabetesType
    preferred_language: Language

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(alias="_id")
    sub: str  # Auth0 user ID
    nickname: str
    age: int
    gender: str
    diabetes_type: str
    preferred_language: str

from openai import BaseModel


class ChatQuery(BaseModel):
    query: str

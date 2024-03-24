from uuid import uuid4
from datetime import datetime
from langchain_core.messages import BaseMessage
from pydantic import BaseModel


class ChatMessage(BaseMessage):
    """ChatMessage class to store a chat message.

    Args:
        BaseMessage (_type_): Base message class.
    """

    def __init__(self, content, **kwargs):
        super().__init__(content, **kwargs)

        self.message_id = str(uuid4())
        self.timestamp = datetime.now()


class ChatHistory(BaseModel):
    user_id: str
    messages: list[ChatMessage]

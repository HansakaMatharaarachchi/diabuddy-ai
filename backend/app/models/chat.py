from datetime import datetime
from uuid import uuid4

from langchain_core.messages import BaseMessage
from pydantic import Field


class ChatMessage(BaseMessage):
    """ChatMessage class to store a chat message.

    Args:
        BaseMessage (_type_): Base message class.
    """

    message_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)

    def __init__(self, content, **kwargs):
        # Extract existing ID and timestamp if present.
        existing_id = kwargs.pop("message_id", None)
        existing_timestamp = kwargs.pop("timestamp", None)

        super().__init__(content, **kwargs)

        # Set the message_id and timestamp
        self.message_id = existing_id or self.message_id
        self.timestamp = existing_timestamp or self.timestamp

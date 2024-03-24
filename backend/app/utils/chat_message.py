import logging
from typing import List

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from pymongo import MongoClient, errors
from app.models.chat import ChatMessage

logger = logging.getLogger(__name__)

DEFAULT_DBNAME = "app"
DEFAULT_COLLECTION_NAME = "chat_message_history"


class MongoDBUserChatMessageHistory(BaseChatMessageHistory):
    """Chat message history that stores user's chat history in MongoDB.

    Args:
        connection_string: connection string to connect to MongoDB
        user_id: id of the user that need to store the messages.
        database_name: name of the database to use
        collection_name: name of the collection to use
    """

    def __init__(
        self,
        connection_string: str,
        user_id: str,
        database_name: str = DEFAULT_DBNAME,
        collection_name: str = DEFAULT_COLLECTION_NAME,
    ):
        self.connection_string = connection_string
        self.user_id = user_id
        self.database_name = database_name
        self.collection_name = collection_name

        try:
            self.client: MongoClient = MongoClient(connection_string)
        except errors.ConnectionFailure as error:
            logger.error(error)

        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self.collection.create_index("user_id", unique=True)

    @property
    def messages(self) -> List[BaseMessage]:
        """Retrieve messages of the user from MongoDB"""

        try:
            user = self.collection.find_one({"user_id": self.user_id})
            if user:
                return messages_from_dict(user.get("messages", []))
            else:
                return []
        except errors.OperationFailure as error:
            logger.error(error)

    def add_message(self, message: BaseMessage) -> None:
        """Append the message to the messages in MongoDB"""
        try:
            self.collection.update_one(
                {"user_id": self.user_id},
                {
                    "$push": {
                        "messages": message_to_dict(
                            base_message_to_chat_message(message)
                        )
                    }
                },
                upsert=True,
            )
        except errors.WriteError as err:
            logger.error(err)

    def clear(self) -> None:
        """Clear user chat history from MongoDB"""
        try:
            self.collection.update_one(
                {"user_id": self.user_id}, {"$set": {"messages": []}}
            )
        except errors.WriteError as err:
            logger.error(err)


def base_message_to_chat_message(base_message: BaseMessage) -> ChatMessage:
    """Convert BaseMessage to ChatMessage.

    Args:
        base_message (BaseMessage): Base message to convert.

    Returns:
        ChatMessage: Converted ChatMessage.
    """
    return ChatMessage(**base_message.dict())

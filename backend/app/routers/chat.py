from app.dependencies.auth import get_token_verifier
from app.dependencies.database import get_db
from app.models.chat import ChatMessage
from app.services.chat_service import ChatService
from fastapi import APIRouter, HTTPException, Security

router = APIRouter()

token_verifier = get_token_verifier()
database = get_db()

chat_service = ChatService(database)


@router.get("/history", response_model=list[ChatMessage])
def get_chat_history(
    user_id: str = Security(token_verifier.verify),
) -> list[ChatMessage]:
    """Get chat message history of the user.

    Args:
        user_id (str): user id. Defaults to Security(token_verifier.verify).

    Raises:
        HTTPException: Error getting chat message history.

    Returns:
        list[ChatMessage]: List of chat messages.
    """
    try:
        return chat_service.get_messages(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/", response_model=bool)
def clear_chat_history(user_id: str = Security(token_verifier.verify)) -> bool:
    """Clear chat message history of the user.

    Args:
        user_id (str): user id. Defaults to Security(token_verifier.verify).

    Raises:
        HTTPException: Error clearing chat message history.

    Returns:
        bool: True if chat message history is cleared successfully, False otherwise.
    """
    try:
        return chat_service.clear_messages(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

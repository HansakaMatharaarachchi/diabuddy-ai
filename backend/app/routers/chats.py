from app.dependencies.auth import get_token_verifier
from app.models.chat import ChatMessage
from app.services.chat import ChatService
from fastapi import APIRouter, Depends, HTTPException, Security

router = APIRouter()

token_verifier = get_token_verifier()


@router.get("/me/chat", response_model=list[ChatMessage])
async def get_chat_history_for_authenticated_user(
    authenticated_user_id: str = Security(token_verifier.verify),
    chat_service: ChatService = Depends(ChatService),
) -> list[ChatMessage]:
    """Get chat history for the authenticated user.

    Returns:
        list[ChatMessage]: List of chat messages.
    """
    try:
        return await chat_service.get_messages(authenticated_user_id) or []
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch chat history.")


@router.delete("/me/chat", response_model=bool)
async def delete_chat_history_of_authenticated_user(
    authenticated_user_id: str = Security(token_verifier.verify),
    chat_service: ChatService = Depends(ChatService),
) -> bool:
    """Delete chat history of the authenticated user.

    Returns:
        bool: True if chat history is deleted successfully.
    """
    try:
        await chat_service.delete_messages(authenticated_user_id)
        return True
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete chat history.")

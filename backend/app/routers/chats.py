from typing import cast

from app.dependencies.auth import get_token_verifier
from app.models.chat import ChatMessage
from app.schemas.chat import ChatQuery
from app.services.chat import ChatService
from app.utils.sse import format_sse_event
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import StreamingResponse

router = APIRouter()

token_verifier = get_token_verifier()


@router.post("/me/chat/stream", response_class=StreamingResponse)
def stream_chat(
    query: ChatQuery,
    authenticated_user_id: str = Security(token_verifier.verify),
    chat_service: ChatService = Depends(ChatService),
):
    """Streams a chat session between a user and the AI using Server-Sent Events (SSE)."""

    async def event_stream():
        try:
            user_message = ChatMessage(content=query.query, type="human")
            ai_message = ChatMessage(content="Thinking...", type="ai")

            # Stream the user message.
            yield format_sse_event("user_message", user_message.dict())
            # Stream the AI response started event.
            yield format_sse_event("ai_response_start", ai_message.dict())

            # Reset the AI response content.
            ai_message.content = ""

            async for chunk in chat_service.stream_ai_response(
                authenticated_user_id, query.query
            ):
                # Update the AI response content.
                ai_message.content += chunk
                # Stream the AI response chunk.
                yield format_sse_event(
                    "ai_message_chunk",
                    {"message_id": ai_message.message_id, "chunk": chunk},
                )

            # save the user message and AI response to the chat history.
            await chat_service.add_messages(
                authenticated_user_id,
                [
                    user_message,
                    ai_message,
                ],
            )

            yield format_sse_event("ai_response_end")
        except Exception:
            yield format_sse_event(
                "error", {"message": "Failed to stream chat response."}
            )

    return StreamingResponse(event_stream(), media_type="text/event-stream")


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
        return (
            cast(
                list[ChatMessage],
                await chat_service.get_messages(authenticated_user_id),
            )
            or []
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch chat history.")


@router.delete("/me/chat", status_code=204)
async def delete_chat_history_of_authenticated_user(
    authenticated_user_id: str = Security(token_verifier.verify),
    chat_service: ChatService = Depends(ChatService),
):
    """Delete chat history of the authenticated user.

    Returns:
        bool: True if chat history is deleted successfully.
    """
    try:
        await chat_service.delete_messages(authenticated_user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete chat history.")

from app.dependencies.auth import get_auth
from app.dependencies.database import get_db
from app.services.chat_service import ChatService
from fastapi import APIRouter

router = APIRouter()

auth = get_auth()
chat_service = ChatService(get_db())

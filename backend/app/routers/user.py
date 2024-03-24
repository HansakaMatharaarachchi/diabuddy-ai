from app.dependencies.auth import get_auth
from app.dependencies.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user_service import UserService
from fastapi import APIRouter, Security

router = APIRouter()

auth = get_auth()
user_service = UserService(get_db())


@router.post("/", response_model=User)
def create_user(
    user: UserCreate,
    auth_result: str = Security(auth.verify),
):
    return user_service.add_user(user)


# @router.get("/{user_id}", response_model=User)
# def get_user(user_id: str, user_service: UserService = Depends(get_user_service)):
#     return user_service.get_user(user_id)


# @router.delete("/{user_id}")
# def delete_user(user_id: str, user_service: UserService = Depends(get_user_service)):
#     user_service.delete_user(user_id)

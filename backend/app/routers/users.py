from app.dependencies.auth import get_token_verifier
from app.exceptions.common import NotFoundException
from app.models.user import User
from app.schemas.user import UpdateUser
from app.services.user import UserService
from fastapi import APIRouter, Depends, HTTPException, Security

token_verifier = get_token_verifier()

router = APIRouter()


@router.get("/me", response_model=User)
def get_authenticated_user(
    authenticated_user_id: str = Security(token_verifier.verify),
    user_service: UserService = Depends(UserService),
):
    """Get the authenticated user"""
    try:
        user = user_service.get_user(authenticated_user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(status_code=500, detail="Error getting user")


@router.patch("/me", response_model=User)
def update_authenticated_user(
    data: UpdateUser,
    authenticated_user_id: str = Security(token_verifier.verify),
    user_service: UserService = Depends(UserService),
):
    """Update the authenticated user"""
    try:
        user_profile = user_service.update_user(authenticated_user_id, data)

        if not user_profile:
            raise NotFoundException("User not found")

        return user_profile
    except NotFoundException as nfe:
        raise HTTPException(status_code=404, detail=nfe.message)
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(status_code=500, detail="Error updating user")


@router.delete("/me", status_code=204)
async def delete_authenticated_user(
    authenticated_user_id: str = Security(token_verifier.verify),
    user_service: UserService = Depends(UserService),
):
    """Delete the authenticated user"""
    try:
        await user_service.delete_user(authenticated_user_id)
    except Exception:
        raise HTTPException(status_code=500, detail="Error deleting user")

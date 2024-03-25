from app.dependencies.auth import get_token_verifier, get_user_manager
from app.models.user import UserProfile
from app.schemas.user import UpdateUserProfile
from app.services.user_service import IncompleteProfileDetailsException, UserService
from fastapi import APIRouter, HTTPException, Security

router = APIRouter()


token_verifier = get_token_verifier()
user_manager = get_user_manager()

user_service = UserService(user_manager)


@router.get("/profile", response_model=UserProfile)
def get_profile(user_id: str = Security(token_verifier.verify)):
    """Get user profile.

    Args:
        user_id (str): user id. Defaults to Security(token_verifier.verify).

    Raises:
        HTTPException: User profile not found.
        HTTPException: Incomplete profile details.
        HTTPException: Error getting user profile.

    Returns:
        UserProfile: User profile.
    """
    try:
        user_profile = user_service.get_user_profile(user_id)

        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")

        return user_profile
    except IncompleteProfileDetailsException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/profile", response_model=UserProfile)
def update_profile(
    data: UpdateUserProfile,
    user_id: str = Security(token_verifier.verify),
):
    """Update user profile.

    Args:
        data (UpdateUserProfile): User profile data.
        user_id (str): user id. Defaults to Security(token_verifier.verify).

    Raises:
        HTTPException: User profile not found.
        HTTPException: Error updating user profile.

    Returns:
        UserProfile: Updated user profile.
    """
    try:
        user_profile = user_service.update_user_profile(user_id, data)

        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")

        return user_profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/", response_model=bool)
def delete_user(user_id: str = Security(token_verifier.verify)):
    """Delete user.

    Args:
        user_id (str): user id. Defaults to Security(token_verifier.verify).

    Returns:
        bool: True if user is deleted successfully, False otherwise.
    """
    return user_service.delete_user(user_id)

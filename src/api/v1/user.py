from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.user import UserInDBBase, UserUpdateInfo
from src.schemas.log import LogSchema
from src.services import log_service
from src.models import User
from src.api.deps import get_current_user
from src.core.config import settings
from src.services import user_service

router = APIRouter()


@router.get(
    "/me", response_model=UserInDBBase, status_code=200, description="Get user profile"
)
async def user_details(user: User = Depends(get_current_user)):
    return user


@router.get("/me/history", response_model=List[LogSchema])
async def user_history(
    user: User = Depends(get_current_user), skip: int = 0, limit: int = 10
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request."
        )
    logs = await log_service.get_logs_by_user(user.id, skip=skip, limit=limit)
    # Add the saved path prefix to each log.
    for log in logs:
        log.picture_path = f"{settings.SAVE_PATH}/{log.picture_path}"

    return logs


@router.put(
    "/me",
    response_model=UserInDBBase,
    status_code=200,
    description="Change user's name or last name",
)
async def user_details(
    user_info: UserUpdateInfo, user: User = Depends(get_current_user)
):
    user = await user_service.change_info(user, user_info)
    return user

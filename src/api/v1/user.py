from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.user import UserInDBBase
from src.schemas.log import LogSchema
from src.services import log_service
from src.models import User
from src.api.deps import get_current_user
from src.core.config import settings

router = APIRouter()


@router.get('/me', response_model=UserInDBBase, status_code=200, description="Get user profile")
async def user_details(user: User = Depends(get_current_user)):
    return user


@router.get('/me/history', response_model=List[LogSchema])
async def user_history(user: User = Depends(get_current_user), skip: int = 0, limit: int = 10):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request.")
    logs = await log_service.get_logs_by_user(user.id, skip=skip, limit=limit)
    # Add the saved path prefix to each log.
    for log in logs:
        log.picture_path = f'{settings.SAVE_PATH}/{log.picture_path}'
        
    return logs

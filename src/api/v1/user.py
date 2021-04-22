from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from src.services import user_service, log_service
from src.models import User

router = APIRouter()


@router.get('/me')
async def user_details():
    raise NotImplementedError()


@router.get('/me/history')
async def user_history(authorize: AuthJWT = Depends(), skip: int = 0, limit: int = 10):
    user: User = await user_service.get_by_email(authorize.get_jwt_subject())
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request.")
    logs = await log_service.get_logs_by_user(user.id, skip=skip, limit=limit)
    return logs

from pathlib import Path

from src.core.config import settings
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi_jwt_auth import AuthJWT
from src.services import log_service, user_service

router = APIRouter()


@router.get('/{img_name}')
async def get_img(img_name, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user = await user_service.get_by_email(authorize.get_jwt_subject())
    img = await log_service.get_log_by_img(img_name)

    if img.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    path = Path(settings.SAVE_PATH) / img_name
    return FileResponse(f'{path}')

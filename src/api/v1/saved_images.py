from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi_jwt_auth import AuthJWT

from src.services import user_service, log_service

router = APIRouter()


@router.get('/{img_name}')
async def get_img(img_name, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user = await user_service.get_by_email(authorize.get_jwt_subject())
    img = await log_service.get_log_by_img(img_name)

    if img.user_id == user.id:
        return FileResponse(f'saved/{img_name}')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

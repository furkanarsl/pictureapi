from pathlib import Path
from src.api.deps import get_current_user

from src.core.config import settings
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from src.services import log_service, user_service
from src.models import User

router = APIRouter()


@router.get("/{img_name}", response_class=FileResponse)
async def get_img(img_name, user: User = Depends(get_current_user)):
    img = await log_service.get_log_by_img(img_name)

    if not img:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found."
        )
    if img.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    path = Path(settings.SAVE_PATH) / img_name
    return FileResponse(f"{path}")

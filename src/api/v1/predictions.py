import pathlib

from datetime import datetime
from hashlib import md5

import aiofiles
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from src.models.user import User
from src.services import log_service
from src.core.config import settings
from src.api.deps import get_current_user
from src.schemas.prediction import Result
import httpx

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png"]
router = APIRouter()


@router.post("/", response_model=Result, status_code=200)
async def predict_img(
    file: UploadFile = File(...), user: User = Depends(get_current_user)
):
    try:
        file_name, file_extension = file.filename.split(".")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid file."
        )

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File type not allowed."
        )

    img_name = md5(str(file_name + str(datetime.now())).encode("utf-8")).hexdigest()

    save_path = pathlib.Path(settings.SAVE_PATH) / (
        str(img_name) + "." + file_extension
    )

    async with aiofiles.open(save_path, "wb") as out_file:
        while content := await file.read(8388608):
            await out_file.write(content)

    files = {"file": open(save_path, "rb")}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://host.docker.internal:8000/", files=files, timeout=1000000
        )
    res = response.json()

    await log_service.create(user.id, res["result"], (img_name + "." + file_extension))
    return {"result": res["result"]}

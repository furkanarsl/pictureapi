from fastapi import APIRouter, UploadFile, File, Form, Body, HTTPException, status, Depends
import aiofiles
from fastapi_jwt_auth import AuthJWT

from src.schemas.prediction import PredictionParameters, PredictionResult
import pathlib
from src.services.result_log import log_service
from src.services.user import user_service
from src.core.config import settings

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png"]
router = APIRouter()


@router.post("/upload")
async def file_upload(file: UploadFile = File(...)):
    try:
        file_name, file_extension = file.filename.split(".")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid file.")
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File type not allowed.")
    save_path = pathlib.Path(settings.SAVE_PATH) / (file_name + "." + file_extension)
    async with aiofiles.open(save_path, 'wb') as out_file:
        while content := await file.read(16777216):  # 16MB
            await out_file.write(content)
    return {"Result": "OK"}


@router.post("/", response_model=PredictionResult)
async def predict(body: PredictionParameters, authorize: AuthJWT = Depends()):
    # Do prediction.
    authorize.jwt_required()
    user = await user_service.get_by_email(authorize.get_jwt_subject())
    await log_service.create(user.id, "car", "/saved/photo.jpg")
    return {"results": [{"name": "car", "ranking": "0.9"}, {"name": "truck", "ranking": "0.7"}]}

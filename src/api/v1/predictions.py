from fastapi import APIRouter, UploadFile, File, Form, Body, HTTPException, status, Depends
import aiofiles
from fastapi_jwt_auth import AuthJWT

from src.schemas.prediction import PredictionParameters, PredictionResult
import pathlib
from src.services.result_log import log_service
from src.services.user import user_service
from src.core.config import settings
from src.core.prediction import predict, load_img
from datetime import datetime
from hashlib import md5

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png"]
router = APIRouter()


@router.post("/")
async def predict_img(file: UploadFile = File(...), authorize: AuthJWT = Depends()):
    # Do prediction.
    authorize.jwt_required()
    user = await user_service.get_by_email(authorize.get_jwt_subject())
    try:
        file_name, file_extension = file.filename.split(".")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid file.")
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File type not allowed.")
    img_name = md5(str(file_name + str(datetime.now())).encode('utf-8')).hexdigest()
    save_path = pathlib.Path(settings.SAVE_PATH) / (str(img_name) + "." + file_extension)

    async with aiofiles.open(save_path, 'wb') as out_file:
        while content := await file.read(8388608):  # 16MB
            await out_file.write(content)

    img = load_img(f'{save_path}')
    _, result = predict(img)

    await log_service.create(user.id, result, save_path)
    return {"result": result}

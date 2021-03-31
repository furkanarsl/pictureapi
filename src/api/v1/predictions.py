from fastapi import APIRouter, UploadFile, File, Form, Body, HTTPException, status
import aiofiles
from src.schemas.prediction import PredictionParameters, PredictionResult

ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png"]
router = APIRouter()


@router.post("/upload")
async def file_upload(file: UploadFile = File(...), file_hash: str = Form(...)):
    file_extension = file.filename.split(".")[1]
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File type not allowed.")
    save_path = file_hash + "." + file_extension
    async with aiofiles.open(save_path, 'wb') as out_file:
        while content := await file.read(4096):
            await out_file.write(content)
    return {"Result": "OK"}


@router.post("/", response_model=PredictionResult)
async def predict(body: PredictionParameters):
    # Do prediction.
    return {"results": [{"name": "car", "ranking": "0.9"}, {"name": "truck", "ranking": "0.7"}]}

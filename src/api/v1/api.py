from fastapi import APIRouter

from src.api.v1 import auth, predictions, user, saved_images

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(
    predictions.router, prefix="/prediction", tags=["Predictions"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(
    saved_images.router, prefix="/saved", tags=["Images"])

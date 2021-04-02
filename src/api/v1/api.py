from fastapi import APIRouter

from src.api.v1 import auth, predictions

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(predictions.router, prefix="/prediction", tags=["Predictions"])

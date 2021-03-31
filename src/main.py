from fastapi import FastAPI, WebSocket, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from src.api.v1.api import api_router
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from src.core.config import settings

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)


@AuthJWT.load_config
def get_config():
    return settings


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

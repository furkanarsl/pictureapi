import aiofiles
from fastapi import FastAPI, WebSocket, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from src.api.v1.api import api_router
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from src.core.config import settings
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)

register_tortoise(
    app,
    db_url=settings.SQLALCHEMY_DATABASE_URI,
    modules={"models": ["src.models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)


@app.websocket_route("/ws")
async def websock(websocket: WebSocket):
    await websocket.accept()
    while data := await websocket.receive_bytes():
        async with aiofiles.open('output.png', "+wb") as out_file:
            await out_file.write(data)
    await websocket.send_text("recieved")


@app.get("/")
def hello():
    return "Hello World!"


@AuthJWT.load_config
def get_config():
    return settings


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

import jwt
from src.core.jw_exception import jwt_exception_handler
from fastapi import FastAPI


from src.api.v1.api import api_router
from src.core.config import settings
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)
app.add_exception_handler(jwt.PyJWTError, jwt_exception_handler)

register_tortoise(
    app,
    db_url=settings.SQLALCHEMY_DATABASE_URI,
    modules={"models": ["src.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

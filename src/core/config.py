import secrets
from datetime import timedelta
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    authjwt_secret_key: str = "56691a33a3124999f6a896e2812d9d9f7f5eabc33c1cc56b" # TODO move to .env
    authjwt_access_token_expires: timedelta = timedelta(minutes=2)
    authjwt_refresh_token_expires: timedelta = timedelta(days=30)
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = 'postgres://furkana:0071@localhost:5432/postgres' # TODO move to .env


settings = Settings()

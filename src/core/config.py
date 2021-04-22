from datetime import timedelta
from typing import Union

from pydantic import BaseSettings, PostgresDsn, DirectoryPath


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    authjwt_secret_key: str
    authjwt_access_token_expires: Union[timedelta, int]
    authjwt_refresh_token_expires: Union[timedelta, int]
    SQLALCHEMY_DATABASE_URI: PostgresDsn  # TODO move to .env
    SAVE_PATH: DirectoryPath = 'saved'

settings = Settings()

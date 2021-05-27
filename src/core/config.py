from pydantic import BaseSettings, PostgresDsn, DirectoryPath


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 180  # DEFAULT 3 HOURS
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200  # DEFAULT 30 DAYS
    SQLALCHEMY_DATABASE_URI: PostgresDsn
    SAVE_PATH: DirectoryPath = "saved"
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_TLS = True
    REDIS_URL: str = "redis"
    REDIS_PORT: int = 6379
    API_URL: str = "http://192.168.193.31"
    PREDICTION_URL: str


settings = Settings()

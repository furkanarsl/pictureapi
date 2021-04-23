from datetime import datetime, timedelta
from typing import Literal
from passlib.context import CryptContext
import jwt
from uuid import uuid4
from src.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_token(subject, expire: timedelta = None, type: Literal["access", "refresh"] = "access") -> str:
    issued_at = datetime.utcnow()
    if expire:
        expire = issued_at + timedelta(minutes=expire)
    else:
        expire = issued_at + \
            timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    data = {"sub": subject,
            "iat": issued_at,
            "nbf": issued_at,
            "jti": str(uuid4()),
            "exp": expire,
            "type": type}

    encoded_jwt = jwt.encode(
        data, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def generate_access_token(subject) -> str:
    expr = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    return generate_token(subject=subject, type="access", expire=expr)


def generate_refresh_token(subject) -> str:
    expr = settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
    return generate_token(subject=subject, type='refresh', expire=expr)

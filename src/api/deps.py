import jwt
from fastapi import Depends, HTTPException, status
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2PasswordBearer
from src.core import security
from src.core.config import settings
from src.models import User
from src.schemas.token import Token, TokenPayload
from src.services import user_service
from starlette.status import (HTTP_401_UNAUTHORIZED,
                              HTTP_422_UNPROCESSABLE_ENTITY)

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login/")


async def access_token_required(token: str = Depends(reusable_oauth2)) -> Token:
    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[security.ALGORITHM]
    )
    token_data = TokenPayload(**payload)
    if token_data.is_active == "False":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only verifed users are allowed.",
        )

    if token_data.type != "access":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only access tokens are allowed.",
        )
    return token


async def access_token_required_non_verified(
    token: str = Depends(reusable_oauth2),
) -> Token:
    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[security.ALGORITHM]
    )
    token_data = TokenPayload(**payload)

    if token_data.type != "access":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only access tokens are allowed.",
        )
    return token


async def refresh_token_required(token: str = Depends(reusable_oauth2)):
    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[security.ALGORITHM]
    )
    token_data = TokenPayload(**payload)
    if token_data.type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only refresh tokens are allowed.",
        )
    return token_data


async def get_current_user(token: str = Depends(access_token_required)) -> User:
    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[security.ALGORITHM]
    )

    token_data = TokenPayload(**payload)
    user = await user_service.get_by_email(token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

from fastapi.openapi.models import OAuthFlows
import jwt

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from src.models import User
from src.core.config import settings
from src.core import security
from src.services import user_service
from src.schemas.token import Token, TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/"
)


async def get_current_user(token: str = Depends(reusable_oauth2)) -> User:
    payload = jwt.decode(
        token, settings.authjwt_secret_key, algorithms=[security.ALGORITHM]
    )

    token_data = TokenPayload(**payload)
    user = await user_service.get_by_email(token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def access_token_required(token: str = Depends(reusable_oauth2)) -> Token:
    payload = jwt.decode(
        token, settings.authjwt_secret_key, algorithms=[security.ALGORITHM]
    )
    token_data = TokenPayload(**payload)

    if token_data.type == "access":
        return token
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Only access tokens are allowed.")


async def refresh_token_required(token: str = Depends(reusable_oauth2)):
    payload = jwt.decode(
        token, settings.authjwt_secret_key, algorithms=[security.ALGORITHM]
    )
    token_data = TokenPayload(**payload)
    if token_data.type == "refresh":
        return token
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Only refresh tokens are allowed.")

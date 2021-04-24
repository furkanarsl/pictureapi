from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from src.models.user import User
from src.schemas.token import LoginToken, Token
from src.api.deps import get_current_user, refresh_token_required, access_token_required

from src.core.security import generate_access_token, generate_refresh_token

from src.schemas.user import UserCreate, UserInDBBase

from src.services.user import user_service

router = APIRouter()



@router.post(
    "/login",
    response_model=LoginToken,
    status_code=200,
    description="Endpoint for users to login.",
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if not await user_service.authenticate(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong username or password",
        )
    tokens = {
        "access_token": generate_access_token(subject=username),
        "refresh_token": generate_refresh_token(subject=username),
    }
    response = LoginToken(**tokens)
    return response
    s4Vu4r96WPv


@router.get("/refresh", response_model=Token, status_code=200)
async def refresh(
    token: Token = Depends(refresh_token_required),
    user: User = Depends(get_current_user),
):
    access_token = generate_access_token(subject=user.email)
    return Token(access_token=access_token)


@router.get("/verify-token")
async def verify(token: Token = Depends(access_token_required)):
    return JSONResponse(content=({"Result": "Ok"}), status_code=200)


@router.post("/register", response_model=UserInDBBase, status_code=201)
async def register(user_in: UserCreate):
    user = await user_service.get_by_email(user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists."
        )
    user = await user_service.create(user_in)
    return user

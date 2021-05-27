from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_406_NOT_ACCEPTABLE,
)
from src.core.verification import (
    send_email_verificaton_token,
    send_password_reset_token,
)
from src.models.user import User
from src.schemas.token import (
    LoginToken,
    ResetPasswordRequest,
    Token,
    TokenPayload,
    VerifyEmail,
    ResetPassword,
    ChangePassword,
)
from src.api.deps import get_current_user, refresh_token_required, access_token_required
from src.core.security import generate_access_token, generate_refresh_token
from src.core.db.session import redis_email, redis_pw
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
    user = await user_service.authenticate(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong username or password",
        )
    tokens = {
        "access_token": generate_access_token(
            subject=username, is_active=user.is_active
        ),
        "refresh_token": generate_refresh_token(subject=username),
    }
    response = LoginToken(**tokens)
    return response


@router.get("/refresh", response_model=Token, status_code=200)
async def refresh(token: TokenPayload = Depends(refresh_token_required)):
    access_token = generate_access_token(subject=token.sub, is_active=token.is_active)
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
    send_email_verificaton_token(to=user_in.email)
    return user


@router.post("/verify_email", response_model=Token)
async def verify_email(code: VerifyEmail):
    r = redis_email.get(code.code)
    if not r:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid verificaiton code.",
        )
    user = await user_service.verify_user(r)
    print(user)
    if user:
        redis_email.delete(code.code)

    access_token = generate_access_token(subject=user.email, is_active=user.is_active)
    return Token(access_token=access_token)


@router.post("/change_password")
async def change_password(
    new_pass: ChangePassword, user: User = Depends(get_current_user)
):
    await user_service.change_pass(user, new_pass=new_pass.new_password)
    return JSONResponse(content=({"Result": "Ok"}), status_code=200)


@router.post("/reset_password")
async def reset_password(obj: ResetPassword):
    user_email = redis_pw.get(obj.code)
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid verificaiton code.",
        )
    user = await user_service.get_by_email(user_email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exists.",
        )
    await user_service.change_pass(user, new_pass=obj.new_password)
    redis_pw.delete(obj.code)
    return JSONResponse(content=({"Result": "Ok"}), status_code=200)


@router.post("/request_password_reset")
async def reset_password_token(obj: ResetPasswordRequest):
    user = user_service.get_by_email(obj.email)
    if user:
        send_password_reset_token(to=obj.email)
    return JSONResponse(
        content=({"Result": "Email sent."}),
        status_code=200,
    )

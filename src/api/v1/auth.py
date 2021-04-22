from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from src.schemas.user import UserCreate, UserBase
from fastapi_jwt_auth import AuthJWT
from src.services.user import user_service

router = APIRouter()


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                authorize: AuthJWT = Depends()):
    username = form_data.username
    password = form_data.password
    if not await user_service.authenticate(username, password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong username or password")
    access_token = authorize.create_access_token(subject=username)
    refresh_token = authorize.create_refresh_token(subject=username)
    return JSONResponse({"access_token": access_token, "refresh_token": refresh_token}, status_code=status.HTTP_200_OK)


@router.get("/refresh")
async def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()
    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.get("/verify-token")
async def verify(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return {"Result": "OK"}


@router.post("/register", response_model=UserBase)
async def register(user_in: UserCreate):
    user = await user_service.get_by_email(user_in.email)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists.")
    user = await user_service.create(user_in)
    return user

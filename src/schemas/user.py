from os import name
from typing import Optional
from pydantic import BaseModel, EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator
from src.models import User


class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = False
    name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):

    email: EmailStr
    password: str
    name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: str


class UserUpdateInfo(BaseModel):
    name: Optional[str]
    last_name: Optional[str]


User_Pydantic = pydantic_model_creator(User, name="User")

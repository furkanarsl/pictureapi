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


# Properties to receive via API on creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    last_name: Optional[str] = None


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
# class User(UserInDBBase):
#     pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


User_Pydantic = pydantic_model_creator(User, name="User")

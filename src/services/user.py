from typing import Optional

from src.models.user import User
from src.schemas.user import UserCreate
from src.core.security import get_password_hash, verify_password


class UserService:
    async def get_by_email(self, email: str) -> Optional[User]:
        user = await User.filter(email=email).first()
        return user

    async def create(self, obj_in: UserCreate) -> User:
        # db_obj = User(email=obj_in.email, hashed_password=get_password_hash(obj_in.password),
        #               full_name=obj_in.full_name,
        #               is_superuser=False,
        #               )
        # user = User(email=obj_in.email, hashed_password=get_password_hash(obj_in.password))
        obj_in = obj_in.dict(exclude_unset=True)
        password = obj_in.pop("password")
        user = await User.create(
            **obj_in,
            hashed_password=get_password_hash(password),
            is_active=False,
            is_superuser=False
        )
        return user

    async def change_pass(self, user: User, new_pass: str):
        user.hashed_password = get_password_hash(new_pass)
        await user.save()
        return user

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    async def verify_user(self, email: str):
        user = await self.get_by_email(email=email)
        if not user:
            return None
        user.is_active = True
        await user.save()
        return user


user_service = UserService()

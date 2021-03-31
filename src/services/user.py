from typing import Optional

from src.models.user import User, UserIn_Pydantic
from src.core.security import get_password_hash, verify_password


class UserService:
    async def get_by_email(self, email: str) -> Optional[User]:
        user = await User.filter(email=email).first()
        return user

    async def create(self, obj_in: UserIn_Pydantic) -> User:
        # db_obj = User(email=obj_in.email, hashed_password=get_password_hash(obj_in.password),
        #               full_name=obj_in.full_name,
        #               is_superuser=False,
        #               )
        # user = User(email=obj_in.email, hashed_password=get_password_hash(obj_in.password))
        user = await User.create(**obj_in.dict(exclude_unset=True)
                                 )
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


user_service = UserService()

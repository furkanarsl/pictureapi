from sqlalchemy import Boolean, Column, Integer, String
from src.core.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

from sqlalchemy import Column, String, Enum

from app.utils import RoleEnum
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    name = Column(String(255), nullable=False)
    email = Column(String(55), nullable=False, unique=True)
    password = Column(String, nullable=False)  # hashed password
    role = Column(Enum(RoleEnum, name="user_roles"), default=RoleEnum.user)

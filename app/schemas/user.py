from uuid import UUID

from datetime import datetime
from pydantic import BaseModel, field_validator, EmailStr, Field

from app.utils import RoleEnum, hash_password


class BaseUser(BaseModel):
    name: str
    email: EmailStr


class CreateUser(BaseUser):
    password: str

    @field_validator('password')
    def validate_password(cls, v: str):
        return hash_password(v)


class CreateUserManagement(CreateUser):
    role: RoleEnum


class ResponseUser(BaseUser):
    id: UUID
    role: RoleEnum


class ResponseUserManagement(ResponseUser):
    created_at: datetime


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class ResponseToken(BaseModel):
    access_token: str


class UpdateUser(BaseModel):
    name: str
    current_password: str | None = Field(default=None)
    new_password: str | None = Field(default=None)


class UpdateUserManagement(CreateUser):
    name: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    password: str | None = Field(default=None)
    role: RoleEnum | None = Field(default=None)

    @field_validator('password')
    def validate_password(cls, v: str):
        return hash_password(v) if v else v

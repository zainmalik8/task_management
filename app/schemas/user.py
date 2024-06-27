from uuid import UUID

from pydantic import BaseModel, field_validator, EmailStr

from app.utils import RoleEnum, hash_password


class BaseUser(BaseModel):
    name: str
    email: EmailStr


class CreateUser(BaseUser):
    password: str
    role: RoleEnum

    @field_validator('password')
    def validate_dates(cls, v: str):
        return hash_password(v)


class ResponseUser(BaseUser):
    id: UUID
    role: RoleEnum


class LoginUser(BaseUser):
    email: EmailStr
    password: str


class ResponseToken(BaseModel):
    access_token: str

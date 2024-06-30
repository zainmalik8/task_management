from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

from pydantic import BaseModel, Field, BeforeValidator


class BaseProject(BaseModel):
    name: str


class CreateProject(BaseProject):
    ...


def user_validator(v: Any):
    from app.models.user import User
    if isinstance(v, User):
        return v.id
    return v


UserField = Annotated[Any, BeforeValidator(user_validator)]


class ResponseProject(BaseProject):
    id: UUID
    users: list[UserField] | None = Field(default=None)
    created_at: datetime


class AssignProject(BaseModel):
    user_id: UUID


class UserProjectsResponse(BaseProject):
    id: UUID
    created_at: datetime

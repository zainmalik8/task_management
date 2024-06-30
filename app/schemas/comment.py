from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class BaseComment(BaseModel):
    content: str
    parent_id: UUID | None = Field(default=None)


class CreateComment(BaseComment):
    ...


class ResponseComment(BaseComment):
    id: UUID
    task_id: UUID
    created_at: datetime


class UpdateComment(BaseModel):
    content: str

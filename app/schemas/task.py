from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.utils import StatusEnum


class BaseTask(BaseModel):
    title: str
    description: str | None = Field(default=None)
    parent_id: UUID | None = Field(default=None)
    assignee_id: UUID | None = Field(default=None)


class CreateTask(BaseTask):
    ...


class ResponseTask(BaseTask):
    id: UUID
    project_id: UUID
    status: StatusEnum
    created_at: datetime


class UpdateTask(BaseTask):
    title: str | None = Field(default=None)
    status: StatusEnum | None = Field(default=None)
    project_id: UUID | None = Field(default=None)


class AssignTask(BaseModel):
    assignee_id: UUID

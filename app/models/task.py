import uuid

from sqlalchemy import Column, UUID, Text, String, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.utils import StatusEnum
from .base import BaseModel


class Task(BaseModel):
    __tablename__ = "tasks"

    parent_id = Column(UUID(as_uuid=True))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    project_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    status = Column(Enum(StatusEnum, name="task_status"), default=StatusEnum.to_do)

    assignee_id = Column(UUID, ForeignKey('users.id'))  # task can be created without any assignee
    assignee = relationship("User", backref="task_assignee")

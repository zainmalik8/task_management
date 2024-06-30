from sqlalchemy import Column, UUID, Text

from .base import BaseModel


class Comment(BaseModel):
    __tablename__ = "comments"

    parent_id = Column(UUID(as_uuid=True))
    task_id = Column(UUID(as_uuid=True), nullable=False)
    content = Column(Text, nullable=False)

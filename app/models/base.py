import uuid

from sqlalchemy import Column, DateTime, func, UUID

from ..database import Base


class BaseModel(Base):
    """
    Base Model can contain fields which are common in multiple models.
    """

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __abstract__ = True

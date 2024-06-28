from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import BaseModel
from .association_tables import project_users


class Project(BaseModel):
    __tablename__ = "projects"

    name = Column(String(255), nullable=False)
    users = relationship("User", secondary=project_users, back_populates="projects")

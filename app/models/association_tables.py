from sqlalchemy import Table, Column, ForeignKey

from .base import Base

project_users = Table(
    "project_users",
    Base.metadata,
    Column('project_id', ForeignKey('projects.id')),
    Column('user_id', ForeignKey('users.id')),
)

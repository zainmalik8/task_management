from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint

from .base import Base

project_users = Table(
    "project_users",
    Base.metadata,
    Column('project_id', ForeignKey('projects.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    UniqueConstraint('project_id', 'user_id', name='uq_project_user')
)

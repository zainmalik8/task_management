from enum import Enum


class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"


class StatusEnum(str, Enum):
    to_do = "to_do"
    in_progress = "in_progress"
    completed = "completed"

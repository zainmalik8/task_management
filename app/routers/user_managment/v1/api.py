from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.logger import logger
from app.models.user import User
from app.schemas.user import CreateUserManagement, ResponseUserManagement, UpdateUserManagement
from app.utils import BadRequestException

router = APIRouter(tags=["User Management"], prefix="/admin")


@router.get("/user", response_model=list[ResponseUserManagement], status_code=200)
def get_users(db: Session = Depends(get_db)):
    try:
        return db.query(User).all()
    except Exception as error:
        logger.exception(error)
        raise BadRequestException


@router.post("/user", response_model=ResponseUserManagement, status_code=201)
def create_user(user: CreateUserManagement, db: Session = Depends(get_db)):
    try:
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as error:
        logger.exception(error)
        raise BadRequestException


@router.put("/user{user_id}", response_model=ResponseUserManagement, status_code=200)
def update_user(user_id: UUID, data: UpdateUserManagement, db: Session = Depends(get_db)):
    try:
        serialized_data = data.model_dump(exclude_defaults=True)
        if user := db.query(User).filter(User.id == user_id).first():
            [setattr(user, attribute, value) for attribute, value in serialized_data.items()]
            return user
        raise BadRequestException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid details.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException


@router.delete("/user{user_id}", status_code=204)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    try:
        if db_project := db.query(User).filter(User.id == user_id).first():
            db.delete(db_project)
            db.commit()
            return
        raise BadRequestException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid User ID.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException

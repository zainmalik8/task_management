from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.logger import logger
from app.models.user import User
from app.schemas.user import ResponseUser, UpdateUser
from app.utils import BadRequestException

router = APIRouter(tags=["Profile"])


@router.get('/profile', response_model=ResponseUser, status_code=200)
def get_profile(request: Request, db: Session = Depends(get_db)):
    try:
        if user := db.query(User).filter(User.id == request.state.user_id).first():
            return user
        raise BadRequestException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid details.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException


@router.put('/profile', response_model=ResponseUser, status_code=201)
def update_profile(data: UpdateUser, request: Request, db: Session = Depends(get_db)):
    try:
        serialized_data = data.model_dump()
        if user := db.query(User).filter(User.id == request.state.user_id).first():
            [setattr(user, attribute, value) for attribute, value in serialized_data.items()]
            db.commit()
            db.refresh(user)
            return user
        raise BadRequestException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid details.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException

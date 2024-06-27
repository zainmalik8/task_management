from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.user import User
from app.dependencies import get_db
from app.schemas.user import CreateUser, ResponseUser
from app.utils import BadRequestException
from app.logger import logger

router = APIRouter(tags=["Authentication"])


@router.post('/register', response_model=ResponseUser, status_code=201)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    try:
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as error:
        logger.exception(error)
        raise BadRequestException

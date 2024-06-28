from fastapi import APIRouter, Depends
from fastapi import status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.logger import logger
from app.models.user import User
from app.schemas.user import CreateUser, ResponseUser, LoginUser, ResponseToken
from app.settings import JwtCreds
from app.utils import verify_password, generate_access_token, BadRequestException

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


@router.post('/login', response_model=ResponseToken, status_code=200, dependencies=[])
def login_user(user_creds: LoginUser, db: Session = Depends(get_db)):
    try:
        serialized_data = user_creds.model_dump()
        if user := db.query(User).filter(User.email == serialized_data["email"]).first():
            if verify_password(serialized_data.get("password"), user.password):
                access_token = generate_access_token({"user_id": str(user.id), "user_role": user.role},
                                                     **JwtCreds.get_dict())
                return {"access_token": access_token}
            raise BadRequestException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password.")
        raise BadRequestException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email.")
    except Exception as error:
        logger.exception(error)
        raise error if isinstance(error, BadRequestException) else BadRequestException

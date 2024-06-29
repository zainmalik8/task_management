from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """

    :param password: User password
    :return: a hash
    """
    return pwd_context.hash(password)


def verify_password(raw_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(raw_password, hashed_password)


def generate_access_token(to_encode: dict, secret_key: str, algorithm: str, token_expire_time: int) -> str:
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=token_expire_time)})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)

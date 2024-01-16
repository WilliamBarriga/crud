from typing import Any, Dict, Optional
from datetime import timedelta, datetime

# FastAPI
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import ValidationException

# JWT
from jose import jwt, JWTError

# Cryptography
from passlib.context import CryptContext

# Env
from decouple import config

# Schemas
from auth.schemas.users import User, CompleteUser


SECRET_KEY = config("SECRET_KEY", cast=str)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """create the jwt for the app

    Args:
        data (Userdict): user to encode
        expires_delta: expiration time
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=240)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def generate_token(user: User) -> str:
    """generate a token for auth

    Args:
        user (User): user information
    """
    access_token_expires = timedelta(minutes=120)
    token = create_access_token(
        data=user.model_dump(mode="json"),
        expires_delta=access_token_expires,
    )
    return token

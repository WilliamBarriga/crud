# FastAPI
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import ValidationException

# JWT
from jose import jwt, JWTError

# Schemas
from auth.schemas.users import User

# Services
from auth.services.token import SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """get the current user dependency"""
    error_message = "coul not validate credentials"

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=["HS256"])
        user = User(**payload)
        if not user.email:
            raise ValidationException(error_message)

    except JWTError:
        raise ValidationException(error_message)

    return user

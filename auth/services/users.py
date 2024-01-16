# FastAPI
from fastapi.exceptions import ValidationException

# Cryptography
from passlib.context import CryptContext

# schemas
from auth.schemas.users import CompleteUser, SignupUser, User

# DB
from commons.db import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> None:
    """verify the password

    Args:
        plain_password (str): plain password
        hashed_password (str): hashed password
    """

    verify = pwd_context.verify(plain_password, hashed_password)

    if not verify:
        raise ValidationException("the password is not correct")


def authenticate_user(email: str, password: str) -> User:
    """authenticate user on login"""

    db_user = db.sp("crud_auth_user", [f"'{email}'::varchar"])
    if not db_user:
        raise ValidationException("user not found")

    user = CompleteUser(**db_user[0])
    verify_password(password, user.password.get_secret_value())
    return User(**user.model_dump())


def create_user_signup(user: SignupUser) -> User:
    """create user on signup action

    Args:
        user (SignupUser): user information
    """
    exists = db.sp("crud_validate_user_mail", [f"'{user.email}'::varchar"])[0]
    if exists["duplicated"]:
        raise ValidationException("this user already exists")

    password = user.password.get_secret_value()
    password = pwd_context.hash(password)

    db_user = db.sp(
        "crud_create_user",
        [
            f"'{user.name}'::varchar",
            f"'{user.email}'::varchar",
            f"$${password}$$::varchar",
        ],
    )[0]
    user = User(**db_user)
    return user

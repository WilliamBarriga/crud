# Fastapi
from fastapi import APIRouter, status, Body, Depends
from fastapi.responses import JSONResponse

# Schemas
from users.schemas.users import User
from users.schemas.books import LikedBooks

# Dependencies
from auth.dependecies import get_current_user

# Services
from users.services.books import get_books

from commons.db import db

router = APIRouter(dependencies=[Depends(get_current_user)], prefix="/me")


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
def me_view(user: User = Depends(get_current_user)) -> User:
    "get user data"
    return user


@router.get("/books/", status_code=status.HTTP_200_OK)
def liked_books_view(user: User = Depends(get_current_user)) -> list[LikedBooks]:
    "get user liked books"
    books = get_books(user.id)
    return books

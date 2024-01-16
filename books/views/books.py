# Fastapi
from fastapi import APIRouter, status, Body, Depends, Query
from fastapi.responses import JSONResponse

# Dependencies
from auth.dependecies import get_current_user

# Schemas
from books.schemas.categories import Category
from books.schemas.books import CreateBook, Book

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", status_code=status.HTTP_200_OK)
def get_books_view(
    q: str = Query(default=None), categories: list[int] = Query(default=None)
) -> Book:
    """"""
    return JSONResponse({})


@router.get("/{b_id}", status_code=status.HTTP_200_OK)
def get_book_view(b_id: int) -> Book:
    return JSONResponse({})


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_book_view(book: CreateBook = Body(...)) -> Book:
    return JSONResponse({})


@router.put("/{b_id}/", status_code=status.HTTP_200_OK)
def update_book_view(book: CreateBook = Body(...)) -> Book:
    return JSONResponse({})


@router.delete("/{b_id}/", status_code=status.HTTP_200_OK)
def delete_book_view(b_id: int) -> Book:
    return JSONResponse({})


@router.post("/{b_id}/like/", status_code=status.HTTP_200_OK)
def like_book_view():
    return

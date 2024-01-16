# Fastapi
from fastapi import APIRouter, status, Body, Depends, Query
from fastapi.responses import JSONResponse

# Dependencies
from auth.dependecies import get_current_user

# Schemas
from books.schemas.books import CreateBook, Book

# Services
from books.services.books import (
    create_books,
    delete_books,
    get_books,
    udpate_books,
    like_book,
)

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", status_code=status.HTTP_200_OK)
def get_books_view(
    q: str = Query(default=None), categories: list[int] = Query(default=None)
) -> list[Book]:
    "get all books"
    books = get_books(q, categories)
    return books


@router.get("/{b_id}", status_code=status.HTTP_200_OK)
def get_book_view(b_id: int) -> Book:
    "get one book"
    book = get_books(b_id=b_id)
    return book


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_book_view(book: CreateBook = Body(...)) -> Book:
    "create a new book"
    new_book = create_books(book)
    return new_book


@router.put("/{b_id}/", status_code=status.HTTP_200_OK)
def update_book_view(b_id: int, book: CreateBook = Body(...)) -> Book:
    "update a book and the categories"
    new_book = udpate_books(b_id, book)
    return new_book


@router.delete("/{b_id}/", status_code=status.HTTP_200_OK)
def delete_book_view(b_id: int) -> None:
    "delete a book"
    delete_books(b_id)
    return JSONResponse({})


@router.post("/{b_id}/like/", status_code=status.HTTP_200_OK)
def like_book_view(b_id: int, user=Depends(get_current_user)) -> None:
    "like or remove like to     a book"
    like_book(b_id, user.id)
    JSONResponse({})

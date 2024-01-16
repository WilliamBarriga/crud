from pydantic import BaseModel, Field


class Categories(BaseModel):
    id: int | None
    name: str | None


class PCategories(Categories):
    books: int | None


class Book(BaseModel):
    id: int | None
    name: str | None
    author: str | None
    categories: list[Categories] | None


class LikedBooks(BaseModel):
    principal_categories: list[PCategories] | None
    books: list[Book] | None
    total_books: int | None

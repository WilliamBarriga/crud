from pydantic import BaseModel


class Categories(BaseModel):
    id: int
    name: str


class PCategories(Categories):
    books: int


class Book(BaseModel):
    id: int
    name: str
    author: str
    categories: list[Categories]


class LikedBooks(BaseModel):
    principal_categories: list[PCategories]
    books: list[Book]
    total_books: list

from pydantic import BaseModel, Field

# Schemas
from books.schemas.categories import Category


class BaseBook(BaseModel):
    name: str
    author: str | None = Field(default=None)


class CreateBook(BaseBook):
    categories: list[int] | None = Field(default=None)


class Book(BaseBook):
    id: int
    active: bool

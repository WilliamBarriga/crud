from enum import Enum, auto
from datetime import datetime

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
    categories: list[Category]
    updated_at: datetime


class CUBook(Enum):
    create = auto()
    udpate = auto()

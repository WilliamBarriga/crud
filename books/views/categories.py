# Fastapi
from fastapi import APIRouter, status, Body, Depends, Query
from fastapi.responses import JSONResponse

# Dependencies
from auth.dependecies import get_current_user

# Schemas
from books.schemas.categories import BaseCategory, Category

# Services
from books.services.categories import get_all_categories, create_a_category, delete_a_category

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", status_code=status.HTTP_200_OK)
def get_categories_view(q: str = Query(default=None)) -> list[Category]:
    "get books categories"
    categories = get_all_categories(q)
    return categories


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_category_view(category: BaseCategory = Body(...)) -> Category:
    "create a book category"
    category = create_a_category(category)
    return category


@router.delete("/{c_id}/", status_code=status.HTTP_200_OK)
def delete_category_view(c_id: int) -> Category:
    "delete a category"
    category = delete_a_category(c_id)
    return category

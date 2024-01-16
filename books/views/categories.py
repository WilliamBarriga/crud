# Fastapi
from fastapi import APIRouter, status, Body, Depends, Query
from fastapi.responses import JSONResponse

# Dependencies
from auth.dependecies import get_current_user

# Schemas
from books.schemas.categories import BaseCategory, Category

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/", status_code=status.HTTP_200_OK)
def get_categories_view(q: str = Query(default=None)) -> Category:
    return JSONResponse({})


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_category_view(category: BaseCategory = Body(...)) -> Category:
    return JSONResponse({})


@router.delete("/{c_id}/", status_code=status.HTTP_200_OK)
def delete_category_view(c_id: int) -> Category:
    return JSONResponse({})

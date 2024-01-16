# FastAPI
from fastapi import APIRouter

# Views
from .views.books import router as books_roouter
from .views.categories import router as categories_router

router = APIRouter(prefix=("/books"))

router.include_router(books_roouter)
router.include_router(categories_router, prefix="/categories")

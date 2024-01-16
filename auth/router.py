# FastAPI
from fastapi import APIRouter

# Views
from .views.onboard import router as onboard_router

router = APIRouter()

router.include_router(onboard_router)

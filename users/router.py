# FastAPI
from fastapi import APIRouter

# Views
from .views.profile import router as profile_router

router = APIRouter()

router.include_router(profile_router)

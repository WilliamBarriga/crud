from contextlib import asynccontextmanager

# Starlette
from starlette.middleware.cors import CORSMiddleware

# FastAPI
from fastapi import FastAPI, APIRouter

# DB
from commons.db import db

# Env
from decouple import config, Csv

# Views
from auth.router import router as auth_router
from users.router import router as users_router
from books.router import router as books_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """task to execute on startup and shutodown"""
    db.create_db()
    yield
    db.close()


app = FastAPI(title="CRUD", lifespan=lifespan)

# router
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(books_router)
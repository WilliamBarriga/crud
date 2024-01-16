# Fastapi
from fastapi import APIRouter, status, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

# Env
from decouple import config

# Schemas
from auth.schemas.users import SignupUser
from auth.schemas.token import Token

# Services
from auth.services.token import generate_token
from auth.services.users import create_user_signup, authenticate_user

router = APIRouter()


@router.post("/signup/", status_code=status.HTTP_201_CREATED)
def sigup_view(user: SignupUser = Body(...)) -> JSONResponse:
    user = create_user_signup(user)
    token = generate_token(user)
    return JSONResponse({"status": "user created"})


@router.post("/login/", status_code=status.HTTP_200_OK)
def login_view(form: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = authenticate_user(form.username, form.password)
    acces_token = generate_token(user)
    return Token(access_token=acces_token, token_type="bearer")

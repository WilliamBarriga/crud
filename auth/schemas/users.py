from pydantic import BaseModel, EmailStr, Field, SecretStr


class SignupUser(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr


class User(BaseModel):
    id: int | None = Field(default=None)
    name: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)


class CompleteUser(User):
    password: SecretStr

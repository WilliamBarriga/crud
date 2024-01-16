from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int | None = Field(default=None)
    name: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)

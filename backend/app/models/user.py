from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(BaseModel):
    password: str

class User(UserBase):
    id: int
    is_active: bool | None = None
    role: str

class TokenData(BaseModel):
    username: str | None = None


    class Config:
        orm_mode = True
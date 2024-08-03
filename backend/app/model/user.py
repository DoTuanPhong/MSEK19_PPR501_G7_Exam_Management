from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(BaseModel):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    role: str

    class Config:
        orm_mode = True
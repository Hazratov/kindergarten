from pydantic import BaseModel
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    cook = "cook"
    manager = "manager"


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    role: Role

class LoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: Role
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

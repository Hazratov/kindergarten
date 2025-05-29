from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    cook = "cook"
    manager = "manager"

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    role: Role
    is_active: bool

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[Role] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

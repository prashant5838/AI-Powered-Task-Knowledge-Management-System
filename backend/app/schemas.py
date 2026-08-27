from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str]

class UserOut(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    class Config:
        orm_mode = True


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: Optional[str]
    user: Optional[UserOut]


class DocumentCreate(BaseModel):
    filename: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    assigned_to: Optional[int]

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    assigned_to: Optional[int]
    created_at: datetime
    class Config:
        orm_mode = True

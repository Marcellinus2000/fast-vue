from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    password: str
    class Config:
        orm_mode = True

class CreateUser(UserBase):
    pass

class UserResponse(BaseModel):
    email: EmailStr
    id : int
    created_at: datetime
    class Config:
        orm_mode = True
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    password: str
    class Config:
        from_attributes = True

class CreateUser(UserBase):
    pass

class UserResponse(BaseModel):
    email: EmailStr
    id : int
    created_at: datetime
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    class Config:
        from_attributes  = True

class Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        from_attributes  = True

class TokenData(BaseModel):
    id: Optional[str] = None
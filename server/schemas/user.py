from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    email: str
    password: str
    class Config:
        orm_mode = True


class CreateUser(UserBase):
    pass

class UserResponse(UserBase):
    id : int
    created_at: datetime
    class Config:
        orm_mode = True
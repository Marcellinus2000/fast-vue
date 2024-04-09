from pydantic import BaseModel
from datetime import datetime
from schemas.user import UserResponse

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    owner: UserResponse


class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(PostBase):
    id : int
    created_at: datetime
    class Config:
        from_attributes = True

class JoinPost(BaseModel):
    post: PostResponse
    votes: int

    class Config:
        from_attributes = True
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


"""User Serializer."""

class UserCreate(BaseModel):
    """Structure of User model."""
    email: EmailStr
    password: str

class UserOut(BaseModel):
    """Fields to return the user as a response."""
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True



"""user loging serializer"""
class UserLogin(BaseModel):
    email: EmailStr
    password: str


"""Token serializer"""
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


"""Post serializer"""


class PostBase(BaseModel):
    """Defining Structure of the posts model."""
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# response to user
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    post: Post
    votes: int
    class Config:
        from_attributes = True

class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., le=1)

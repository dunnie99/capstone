from pydantic import BaseModel, Field
from typing import Optional, List

# User schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str

# Movie schemas
class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: str
    owner_id: str

# Rating schemas
class RatingBase(BaseModel):
    rating: float

class RatingCreate(RatingBase):
    movie_id: str

class Rating(RatingBase):
    id: str
    user_id: str
    movie_id: str

# Comment schema
class Comment(BaseModel):
    id: str
    movie_id: str
    user_id: str
    content: str
    parent_id: Optional[str] = None  # For nested comments

    class Config:
        orm_mode = True

# Schema to create a comment
class CommentCreate(BaseModel):
    movie_id: str
    content: str
    parent_id: Optional[str] = None  # Optional parent_id for nested comments
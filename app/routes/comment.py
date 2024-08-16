from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app import crud, schemas
from app.routes.user import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Comment)
async def comment_movie(
    comment: schemas.CommentCreate, 
    user: schemas.User = Depends(get_current_user)
):
    return await crud.create_comment(comment=comment, user_id=user["id"])

@router.get("/{movie_id}", response_model=List[schemas.Comment])
async def get_comments_for_movie(movie_id: str):
    return await crud.get_comments(movie_id=movie_id)

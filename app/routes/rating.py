from typing import List
from fastapi import APIRouter, Depends
from app import crud, schemas
from app.routes.user import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Rating)
async def rate_movie(
    rating: schemas.RatingCreate, 
    user: schemas.User = Depends(get_current_user)
):
    return await crud.rate_movie(rating=rating, user_id=user["id"])

@router.get("/{movie_id}", response_model=List[schemas.Rating])
async def get_ratings(movie_id: str):
    return await crud.get_ratings(movie_id=movie_id)

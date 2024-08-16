from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app import crud, schemas
from app.routes.user import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Movie, status_code=status.HTTP_201_CREATED)
async def create_movie(
    movie: schemas.MovieCreate, 
    user: schemas.User = Depends(get_current_user)
):
    return await crud.create_movie(movie=movie, owner_id=user["id"])

@router.get("/", response_model=List[schemas.Movie])
async def read_movies(skip: int = 0, limit: int = 10):
    movies = await crud.get_movies(skip=skip, limit=limit)
    return movies

@router.get("/{movie_id}", response_model=schemas.Movie)
async def read_movie(movie_id: str):
    movie = await crud.get_movie(movie_id=movie_id)
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return movie

@router.put("/{movie_id}", response_model=schemas.Movie)
async def update_movie(
    movie_id: str, 
    movie: schemas.MovieCreate, 
    user: schemas.User = Depends(get_current_user)
):
    updated_movie = await crud.update_movie(movie_id=movie_id, movie=movie, owner_id=user["id"])
    if not updated_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found or you don't have permission to update")
    return updated_movie

@router.delete("/{movie_id}", response_model=dict)
async def delete_movie(
    movie_id: str, 
    user: schemas.User = Depends(get_current_user)
):
    success = await crud.delete_movie(movie_id=movie_id, owner_id=user["id"])
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found or you don't have permission to delete")
    return {"detail": "Movie deleted"}

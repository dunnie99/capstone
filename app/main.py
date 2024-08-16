from fastapi import FastAPI
from app.routes import user, movie, rating, comment

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Movie Listing API"}

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(movie.router, prefix="/movies", tags=["Movies"])
app.include_router(rating.router, prefix="/ratings", tags=["Ratings"])
app.include_router(comment.router, prefix="/comments", tags=["Comments"])

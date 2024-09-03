from bson import ObjectId
from app import auth
from app.databse import user_collection, movie_collection, rating_collection, comment_collection
from app.schemas import UserCreate, MovieCreate, RatingCreate, CommentCreate, Movie, Rating, Comment
from typing import List, Dict
import logging

async def create_user(user_create: UserCreate) -> Dict[str, str]:
    try:
        user = {
            "username": user_create.username,
            "hashed_password": auth.get_password_hash(user_create.password)
        }
        result = await user_collection.insert_one(user)
        user_id = result.inserted_id
        return {
            "id": str(user_id),
            "username": user_create.username
        }
    except Exception as e:
        logging.error(f"Error creating user: {str(e)}")
        raise

async def create_movie(movie: MovieCreate, token: str) -> Movie:
    try:
        # Decode token to get the user information
        token_data = auth.decode_token(token)
        if token_data is None:
            raise Exception("Invalid or expired token")
        
        user = await auth.get_user(token_data["username"])
        if user is None:
            raise Exception("User not found")
        
        movie_data = movie.dict()
        movie_data["owner_id"] = ObjectId(user["_id"])
        new_movie = await movie_collection.insert_one(movie_data)
        created_movie = await movie_collection.find_one({"_id": new_movie.inserted_id})
        return Movie(**created_movie)
    except Exception as e:
        logging.error(f"Error creating movie: {str(e)}")
        raise
    

async def get_movies(skip: int = 0, limit: int = 10) -> List[Movie]:
    try:
        cursor = movie_collection.find().skip(skip).limit(limit)
        movies = await cursor.to_list(length=limit)
        return [Movie(**movie) for movie in movies]
    except Exception as e:
        logging.error(f"Error retrieving movies: {str(e)}")
        raise

async def rate_movie(rating: RatingCreate, token: str) -> Rating:
    try:
        # Decode token to get the user information
        token_data = auth.decode_token(token)
        if token_data is None:
            raise Exception("Invalid or expired token")
        
        user = await auth.get_user(token_data["username"])
        if user is None:
            raise Exception("User not found")
        
        rating_data = rating.dict()
        rating_data["user_id"] = ObjectId(user["_id"])
        rating_data["movie_id"] = ObjectId(rating.movie_id)
        new_rating = await rating_collection.insert_one(rating_data)
        created_rating = await rating_collection.find_one({"_id": new_rating.inserted_id})
        return Rating(**created_rating)
    except Exception as e:
        logging.error(f"Error rating movie: {str(e)}")
        raise

async def create_comment(comment: CommentCreate, token: str) -> Comment:
    try:
        # Decode token to get the user information
        token_data = auth.decode_token(token)
        if token_data is None:
            raise Exception("Invalid or expired token")
        
        user = await auth.get_user(token_data["username"])
        if user is None:
            raise Exception("User not found")
        
        comment_data = comment.dict()
        comment_data["user_id"] = ObjectId(user["_id"])
        comment_data["movie_id"] = ObjectId(comment.movie_id)
        if comment_data.get("parent_id"):
            comment_data["parent_id"] = ObjectId(comment_data["parent_id"])
        new_comment = await comment_collection.insert_one(comment_data)
        created_comment = await comment_collection.find_one({"_id": new_comment.inserted_id})
        return Comment(**created_comment)
    except Exception as e:
        logging.error(f"Error creating comment: {str(e)}")
        raise
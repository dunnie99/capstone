from bson import ObjectId
from app.databse import movie_collection, rating_collection, comment_collection
from app.models import movie_helper, rating_helper, comment_helper
from app.schemas import RatingCreate, MovieCreate, CommentCreate

# Function to create a new movie
async def create_movie(movie: MovieCreate, owner_id: str):
    movie_data = movie.dict()
    movie_data["owner_id"] = ObjectId(owner_id)
    new_movie = await movie_collection.insert_one(movie_data)
    created_movie = await movie_collection.find_one({"_id": new_movie.inserted_id})
    return movie_helper(created_movie)

# Function to retrieve a movie by its ID, including associated ratings
async def get_movie(movie_id: str):
    movie = await movie_collection.find_one({"_id": ObjectId(movie_id)})
    if movie:
        # Fetch and attach ratings associated with this movie
        ratings = []
        async for rating in rating_collection.find({"movie_id": ObjectId(movie_id)}):
            ratings.append(rating_helper(rating))
        movie_data = movie_helper(movie)
        movie_data["ratings"] = ratings
        return movie_data
    return None

# Function to retrieve all ratings for a specific movie
async def get_ratings(movie_id: str):
    ratings = []
    async for rating in rating_collection.find({"movie_id": ObjectId(movie_id)}):
        ratings.append(rating_helper(rating))
    return ratings

# Function to update an existing movie
async def update_movie(movie_id: str, movie: MovieCreate, owner_id: str):
    movie_data = movie.dict()
    updated_movie = await movie_collection.update_one(
        {"_id": ObjectId(movie_id), "owner_id": ObjectId(owner_id)},
        {"$set": movie_data}
    )
    if updated_movie.modified_count:
        return await get_movie(movie_id)
    return None

# Function to delete a movie
async def delete_movie(movie_id: str, owner_id: str):
    deleted_movie = await movie_collection.delete_one(
        {"_id": ObjectId(movie_id), "owner_id": ObjectId(owner_id)}
    )
    return bool(deleted_movie.deleted_count)

# Function to create a rating for a movie
async def rate_movie(rating: RatingCreate, user_id: str):
    rating_data = rating.dict()
    rating_data["user_id"] = ObjectId(user_id)
    rating_data["movie_id"] = ObjectId(rating.movie_id)
    
    new_rating = await rating_collection.insert_one(rating_data)
    created_rating = await rating_collection.find_one({"_id": new_rating.inserted_id})
    return rating_helper(created_rating)

# Function to retrieve a list of movies, including associated ratings (optional pagination)
async def get_movies(skip: int = 0, limit: int = 10):
    movies = []
    async for movie in movie_collection.find().skip(skip).limit(limit):
        movie_data = movie_helper(movie)
        ratings = []
        async for rating in rating_collection.find({"movie_id": movie["_id"]}):
            ratings.append(rating_helper(rating))
        movie_data["ratings"] = ratings
        movies.append(movie_data)
    return movies
# Function to create a comment for a movie
async def create_comment(comment: CommentCreate, user_id: str):
    comment_data = comment.dict()
    comment_data["user_id"] = ObjectId(user_id)
    comment_data["movie_id"] = ObjectId(comment.movie_id)
    
    # If it's a nested comment, parent_id should be an ObjectId
    if comment_data.get("parent_id"):
        comment_data["parent_id"] = ObjectId(comment_data["parent_id"])
    
    new_comment = await comment_collection.insert_one(comment_data)
    created_comment = await comment_collection.find_one({"_id": new_comment.inserted_id})
    return comment_helper(created_comment)

# Function to retrieve comments for a movie
async def get_comments(movie_id: str):
    comments = []
    async for comment in comment_collection.find({"movie_id": ObjectId(movie_id)}):
        comments.append(comment_helper(comment))
    return comments
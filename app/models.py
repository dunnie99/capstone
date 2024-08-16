from bson import ObjectId

# Helper functions to convert MongoDB documents to Pydantic models
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "hashed_password": user["hashed_password"]
    }

def movie_helper(movie) -> dict:
    return {
        "id": str(movie["_id"]),
        "title": movie["title"],
        "description": movie["description"],
        "owner_id": str(movie["owner_id"])
    }

def rating_helper(rating) -> dict:
    return {
        "id": str(rating["_id"]),
        "movie_id": str(rating["movie_id"]),
        "user_id": str(rating["user_id"]),
        "rating": rating["rating"]
    }

def comment_helper(comment) -> dict:
    return {
        "id": str(comment["_id"]),
        "movie_id": str(comment["movie_id"]),
        "user_id": str(comment["user_id"]),
        "content": comment["content"],
        "parent_id": str(comment["parent_id"]) if comment.get("parent_id") else None
    }

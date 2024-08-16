from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MongoDB connection string from environment variable
MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Create a new MongoDB client and connect to the database
client = AsyncIOMotorClient(MONGO_DETAILS)

# Select the database you want to use
database = client.movie_listing_app

# Define the collections
user_collection = database.get_collection("users")
movie_collection = database.get_collection("movies")
rating_collection = database.get_collection("ratings")
comment_collection = database.get_collection("comments")

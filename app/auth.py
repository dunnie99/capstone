from datetime import datetime, timedelta
from typing import Union, Optional
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from app.databse import user_collection
from app.models import user_helper

SECRET_KEY = "hit"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Ensure 'sub' is set to a valid identifier, such as the username
    if "username" in data:
        to_encode.update({"exp": expire, "sub": data["username"]})
    else:
        raise ValueError("The 'data' dictionary must contain a 'username' field")
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Union[dict, None]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # Ensure this is correctly extracting the username
        if username is None:
            raise JWTError("Invalid token payload: 'sub' is missing or null")
        return {"username": username}
    except ExpiredSignatureError:
        print("Token has expired")
        return None
    except JWTError as e:
        print(f"Token error: {str(e)}")
        return None

async def get_user(username: str) -> Union[dict, None]:
    print(f"Searching for user with username: {username}")  # Debugging line
    user = await user_collection.find_one({"username": username})
    if user:
        return user_helper(user)
    print("User not found")  # Debugging line
    return None
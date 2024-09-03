from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from app import crud, schemas, auth

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=schemas.User)
async def register(user: schemas.UserCreate):
    db_user = await auth.get_user(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_data = await crud.create_user(user)
    return schemas.User(id=user_data['id'], username=user_data['username'])

@router.post("/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Retrieve the user from the database
    user = await auth.get_user(form_data.username)
    
    # Verify the password
    if not user or not auth.verify_password(form_data.password, user.get("hashed_password", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Create the access token
    access_token = auth.create_access_token(data={"username": user["username"]})
    
    # Decode the token for debugging purposes
    try:
        token_payload = jwt.decode(access_token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        print(f"Token generated with payload: {token_payload}")
    except JWTError as e:
        print(f"Error decoding token: {str(e)}")
    
    return {"access_token": access_token, "token_type": "bearer"}
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = auth.decode_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await auth.get_user(payload.get("sub"))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
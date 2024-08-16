from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app import crud, schemas, auth

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=schemas.User)
async def register(user: schemas.UserCreate):
    db_user = await auth.get_user(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await crud.create_user(user)

@router.post("/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth.get_user(form_data.username)
    if not user or not auth.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = auth.create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = auth.decode_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await auth.get_user(payload.get("username"))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

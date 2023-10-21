from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, ShowUser, LoginUser
from data.session import get_db

from data.models.user import User
from core.security import authenticate_user, create_access_token, get_current_user

router = APIRouter()

@router.post("/users", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    _user: User = User(**payload.model_dump())
    await _user.save(db)
    return _user


@router.post("/users/login")
async def login_user(user_input: LoginUser, db: AsyncSession = Depends(get_db)):
    _user = await authenticate_user(user_input.email, user_input.password, db)
    
    if _user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": _user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=ShowUser)
async def get_current_active_user(
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):
    return ShowUser(id=current_user.id, email=current_user.email, is_active=current_user.is_active)


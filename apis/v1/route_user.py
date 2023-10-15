from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate, ShowUser
from data.session import get_db

from data.models.user import User


router = APIRouter()

@router.post("/users", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    _user: User = User(**payload.model_dump())
    await _user.save(db)
    return _user

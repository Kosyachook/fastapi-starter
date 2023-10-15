from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from core.settings import settings
from fastapi.security import OAuth2PasswordBearer
from data.models.user import User

from data.session import get_db
from core.hashing import Hasher
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode_jwt


async def authenticate_user(email:str, password: str, db: AsyncSession):
    
    _user: User = await User.findone(db, [User.email == email])
    if not _user:
        return False
    if not Hasher.verify_password(password, _user.password):
        return False
    return _user

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    #user = get_user_by_email(email=username, db=db)
    _user: User = await User.findone(db, [User.email == username])
    if _user is None:
        raise credentials_exception
    return _user


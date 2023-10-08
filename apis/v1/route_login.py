from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.user import Token
from core.hashing import Hasher
from db.repositories.user import get_user_by_email
from core.security import create_access_token, authenticate_user

from core.settings import settings


router = APIRouter()


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


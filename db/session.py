from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.settings import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
print("Database URL is ",SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

async_engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True, execution_options={"isolation_level": "AUTOCOMMIT"})
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        #db: AsyncSession = async_session()
        yield db
    finally:
        db.close()


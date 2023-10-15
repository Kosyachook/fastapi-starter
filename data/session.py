from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.settings import settings


async_engine = create_async_engine(
    settings.REAL_DATABASE_URL, 
    future=True, 
    echo=True, 
    execution_options={"isolation_level": "AUTOCOMMIT"}
    )

AsyncSessionFactory = async_sessionmaker(async_engine, autoflush=False, expire_on_commit=False)

async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
    
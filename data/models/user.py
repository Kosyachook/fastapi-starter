from typing import Any, List
from data.base_class import Base
from sqlalchemy import Boolean, Integer, String, LargeBinary, select
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession

from core.hashing import Hasher


class User(Base):
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    _password: Mapped[str] = mapped_column(String, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    blogs = relationship("Blog", back_populates="author")
    
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password: str):
        self._password = Hasher.get_password_hash(password=password)
    
    @classmethod
    async def findone(cls, db: AsyncSession, where_conditions: list[Any]):
        query = select(cls).where(*where_conditions)
        result = await db.execute(query)
        return result.scalars().first()
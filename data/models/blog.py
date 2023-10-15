from datetime import datetime
from sqlalchemy import Integer, String, Text, Boolean, DateTime, ForeignKey, select
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from data.base_class import Base


class Blog(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    author = relationship("User", back_populates="blogs")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    
    
    @classmethod
    async def findone(cls, db: AsyncSession, id: int):
        query = select(cls).where(cls.id == id)
        result = await db.execute(query)
        instance = result.scalars().first()
        if instance is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} not found")
        else:
            return instance
        
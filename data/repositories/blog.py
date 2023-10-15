from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.blog import CreateBlog, UpdateBlog
from data.models.blog import Blog


async def list_blogs(db: AsyncSession):
    query = (select(Blog).order_by(Blog.created_at))
    result = await db.execute(query)
    instance = result.scalars().all()
    print(instance)
    print(type(instance))
    return instance


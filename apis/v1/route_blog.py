from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from data.session import get_db

from schemas.blog import CreateBlog, ShowBlog, UpdateBlog
from data.models.blog import Blog
from data.models.user import User
from data.repositories.blog import list_blogs
from core.security import get_current_user


router = APIRouter()


@router.post("/blogs", response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
async def create_blog(
    payload: CreateBlog, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):
    blog = Blog(**payload.model_dump())
    blog.author_id = current_user.id
    await blog.save(db)
    return blog


@router.get("/blog/{id}", response_model=ShowBlog)
async def get_blog(id: int, db: AsyncSession = Depends(get_db)):
    return await Blog.findone(db, id)


@router.get("/blogs", response_model=List[ShowBlog])
async def get_all_blogs(db: AsyncSession = Depends(get_db)):
    blogs = await list_blogs(db)
    return blogs


@router.patch("/blog/{id}", response_model=ShowBlog)
async def update_a_blog(
    id: int, 
    payload: UpdateBlog, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    blog = await Blog.findone(db, id)
    if blog.author_id == current_user.id:
        await blog.update(db, **payload.model_dump())
        return blog
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permissions denied")
    

@router.delete("/delete/{id}")
async def delete_a_blog(
    id:int, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):
    blog = await Blog.findone(db, id)
    
    if blog.author_id == current_user.id:
        return await Blog.delete(blog, db)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permissions denied")
    
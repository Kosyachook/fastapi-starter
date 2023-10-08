from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from db.repositories.blog import create_new_blog, retrieve_blog, list_blogs, update_blog, delete_blog
from schemas.blog import CreateBlog, ShowBlog, UpdateBlog
from db.models.user import User
from core.security import get_current_user


router = APIRouter()


@router.post("/blogs", response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
async def create_blog(blog: CreateBlog, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = create_new_blog(blog=blog, db=db, author_id=current_user.id)
    return blog


@router.get("/blog/{id}", response_model=ShowBlog)
async def get_blog(id: int, db: Session = Depends(get_db)):
    blog = await retrieve_blog(id=id, db=db)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with ID {id} does not exist.")
    return blog


@router.get("/blogs", response_model=List[ShowBlog])
async def get_all_blogs(db: Session = Depends(get_db)):
    blogs = await list_blogs(db=db)
    return blogs


@router.put("/blog/{id}", response_model=ShowBlog)
def update_a_blog(
    id: int, 
    blog: UpdateBlog, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    blog = update_blog(id=id, blog=blog, author_id=current_user.id, db=db)
    if isinstance(blog, dict):
        raise HTTPException(detail=f"Blog with id {id} does not exist")
    return blog


@router.delete("/delete/{id}")
def delete_a_blog(id:int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    message = delete_blog(id=id,author_id=current_user.id,db=db)
    if message.get("error"):
        raise HTTPException(detail=message.get("error"), status_code= status.HTTP_400_BAD_REQUEST)
    return {"msg":f"Successfully deleted blog with id {id}"}

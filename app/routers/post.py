from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from typing import List, Union

from .. import schema, models, utils, oAuth
from sqlalchemy import func

# initialize the first python file
import os

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.params import Body
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import time
from ..database import engine, get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schema.PostOut])
async def read_posts(db: Session = Depends(get_db), curr_user: int = Depends(oAuth.get_current_user), limit: int = 10, skip: int =0, search: Optional[str] = ""):


    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    # print(db.query(models.Post))
    # %20 as space
    # {{URL}}posts?limit=5&skip=1&search=lagta%20hello

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# @app.get("/posts")
# async def read_posts():
#     cursor.execute(""" SELECT * FROM posts""")
#     val = cursor.fetchall()
#     return {"posts": val}


@router.get("/{post_id}", response_model=schema.Post)
async def get_onepost(post_id: int, db: Session = Depends(get_db), curr_user: int = Depends(oAuth.get_current_user)):
    # print(post_id)
    val = db.query(models.Post).filter(models.Post.id == str(post_id)).first()
    if not val:
        raise HTTPException(status_code=404, detail="Item not found")
    return val
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(post_id)))
    # val = cursor.fetchone()
    # if not val:
    #     raise HTTPException(status_code=404, detail="Item not found")
    # return {"post": val}


@router.delete("/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db), curr_user: int = Depends(oAuth.get_current_user)):

    val = db.query(models.Post).filter(models.Post.id == str(post_id))
    newVal = val.first()
    if not newVal:
        raise HTTPException(status_code=404, detail=f"Item of Id {post_id} not found")
    
    if newVal.owner_id != curr_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this post")
    
    val.delete(synchronize_session=False)
    db.commit()
    # Return a JSON response with a custom message and status code 200
    return JSONResponse(content={"message": f"Post with ID {post_id} has been successfully deleted."},
                        status_code=status.HTTP_200_OK)
    # return JSONResponse(content = {"post deleted"},status_code=status.HTTP_204_NO_CONTENT)
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""",(str(post_id)))
    # val = cursor.fetchone()
    # conn.commit()

    # if not val:
    #     raise HTTPException(status_code=404, detail="Item not found")

    return {"detail": "Post deleted", "deleted": val}

@router.put("/{post_id}")
async def update_post(post_id:int, post: schema.PostCreate, db: Session = Depends(get_db), curr_user: int = Depends(oAuth.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == str(post_id))
    posting = post_query.first()

    if not posting:
        raise HTTPException(status_code=404, detail=f"Item of Id {post_id} not found")
    

    if posting.owner_id != curr_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this post")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()

    return JSONResponse(content={"message":"post updated"},status_code= status.HTTP_202_ACCEPTED)
    # cursor.execute(""" UPDATE posts SET title=%s, description=%s WHERE id = %s RETURNING *""",(post.title, post.description, str(post_id)))
    # val = cursor.fetchone()
    # conn.commit()
    # if not val:
    #     raise HTTPException(status_code=404, detail=f"Item of Id {post_id} not found")
    # return {"detail": "Post updated", "post": val}


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schema.Post)
async def create_post(new_post: schema.PostCreate, db: Session = Depends(get_db), curr_user: int = Depends(oAuth.get_current_user)):
   print(curr_user.email)
   newP =  models.Post(owner_id = curr_user.id, **new_post.dict())           
   db.add(newP)
   db.commit()
   db.refresh(newP)
#    print(newP)
   return newP

    # cursor.execute("""  INSERT INTO posts (title, description) VALUES (%s, %s) RETURNING * """,(new_post.title,new_post.description))
    # val = cursor.fetchone()
    # conn.commit()

    # return {"post created": val}

    
from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from typing import List, Union

from .. import schema, models, utils, oAuth


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


@router.get("/", response_model=List[schema.Post])
async def read_posts(db: Session = Depends(get_db), ):
    posts = db.query(models.Post).all()
    # print(db.query(models.Post))
    return posts

# @app.get("/posts")
# async def read_posts():
#     cursor.execute(""" SELECT * FROM posts""")
#     val = cursor.fetchall()
#     return {"posts": val}


@router.get("/{post_id}", response_model=schema.PostBase)
async def get_onepost(post_id: int, db: Session = Depends(get_db)):
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
async def delete_post(post_id: int, db: Session = Depends(get_db)):

    val = db.query(models.Post).filter(models.Post.id == str(post_id))
    if not val.first():
        raise HTTPException(status_code=404, detail=f"Item of Id {post_id} not found")
    
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
async def update_post(post_id:int, post: schema.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == str(post_id))
    posting = post_query.first()

    if not post_query.first():
        raise HTTPException(status_code=404, detail=f"Item of Id {post_id} not found")
    
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
async def create_post(new_post: schema.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oAuth.get_current_user)):
#    print(user_id)
   newP =  models.Post(**new_post.dict())           
   db.add(newP)
   db.commit()
   db.refresh(newP)
   return newP

    # cursor.execute("""  INSERT INTO posts (title, description) VALUES (%s, %s) RETURNING * """,(new_post.title,new_post.description))
    # val = cursor.fetchone()
    # conn.commit()

    # return {"post created": val}

    
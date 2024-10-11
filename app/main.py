# initialize the first python file
import os
from typing import List, Union

from fastapi import FastAPI, status, Response, HTTPException, Depends

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.params import Body
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import time

from . import models, schema
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import utils

models.Base.metadata.create_all(bind=engine)

load_dotenv()


app = FastAPI()


# while True:
#         try:
#             conn = psycopg2.connect(
#                 host=os.getenv('HOST'),
#                 database=os.getenv('DATABASE'),
#                 user= os.getenv('USERNAME'),
#                 password=os.getenv('PASSWORD')
#             )

#             cursor = conn.cursor(cursor_factory=RealDictCursor)
#             print("Database connection established")
#             break

#         except (Exception, psycopg2.Error) as error:
#             print ("Error while connecting to PostgreSQL", error)
#             time.sleep(2)
#             break



# my_post =  [{"title": "hey title 1", "description": "description 1", "id": 1},{"title": "hey title 2", "description": "description 2", "id": 2}]


@app.get("/")
async def read_root():

    return {"Hello": "World"}

@app.get("/posts", response_model=List[schema.Post])
async def read_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # print(db.query(models.Post))
    return posts

# @app.get("/posts")
# async def read_posts():
#     cursor.execute(""" SELECT * FROM posts""")
#     val = cursor.fetchall()
#     return {"posts": val}


@app.get("/posts/{post_id}", response_model=schema.PostBase)
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


@app.delete("/posts/{post_id}")
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

@app.put("/posts/{post_id}")
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


@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model=schema.Post)
async def create_post(new_post: schema.PostCreate, db: Session = Depends(get_db)):
   newP =  models.Post(**new_post.dict())           
   db.add(newP)
   db.commit()
   db.refresh(newP)
   return newP

    # cursor.execute("""  INSERT INTO posts (title, description) VALUES (%s, %s) RETURNING * """,(new_post.title,new_post.description))
    # val = cursor.fetchone()
    # conn.commit()

    # return {"post created": val}

    
@app.post("/users", status_code = status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    user_in_db = db.query(models.User).filter(models.User.email == user.email).first()
    if user_in_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password

    user_to_create = models.User(**user.dict())
    db.add(user_to_create)
    db.commit()
    db.refresh(user_to_create)

    return user_to_create

@app.get('/users/{id}', response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
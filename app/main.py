# initialize the first python file
import os
from typing import Union

from fastapi import FastAPI, status, Response, HTTPException

from pydantic import BaseModel
from fastapi.params import Body
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import time

load_dotenv()


app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class Post(BaseModel):
    title: str
    description: str
    published: bool = True


while True:
        try:
            print(os.getenv('USERNAME'))
            print(f"Password: {os.getenv('PASSWORD')}")
            conn = psycopg2.connect(
                host=os.getenv('HOST'),
                database=os.getenv('DATABASE'),
                user= os.getenv('USERNAME'),
                password=os.getenv('PASSWORD')
            )

            cursor = conn.cursor(cursor_factory=RealDictCursor)
            print("Database connection established")
            break

        except (Exception, psycopg2.Error) as error:
            print ("Error while connecting to PostgreSQL", error)
            time.sleep(2)
            break



my_post =  [{"title": "hey title 1", "description": "description 1", "id": 1},{"title": "hey title 2", "description": "description 2", "id": 2}]

@app.get("/")
async def read_root():

    return {"Hello": "World"}

@app.get("/posts")
async def read_posts():
    cursor.execute(""" SELECT * FROM posts""")
    val = cursor.fetchall()
    return {"posts": val}


@app.get("/posts/{post_id}")
async def get_onepost(post_id: int):
    print(post_id)

    cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(post_id)))
    val = cursor.fetchone()
    if not val:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"post": val}

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""",(str(post_id)))
    val = cursor.fetchone()
    conn.commit()

    return {"detail": "Post deleted", "deleted": val}

@app.put("/items/{item_id}")
async def update_item(item_id:int, item: Item):
    return {"item_name": item.name, "item_id": item_id} 

# @app.post("/createPost")
# async def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"post": f"title: {payload['title']}, description: {payload['description']}", "title": payload["title"],"description": payload["description"]}


@app.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_post(new_post: Post):
    # print(new_post)
    # val = new_post.dict()
    # val["id"] = randrange(1,1000000)
    # my_post.append(val)

    cursor.execute("""  INSERT INTO posts (title, description) VALUES (%s, %s) RETURNING * """,(new_post.title,new_post.description))
    val = cursor.fetchone()
    conn.commit()

    return {"post created": val}

    
# initialize the first python file


from typing import Union

from fastapi import FastAPI, status, Response, HTTPException

from pydantic import BaseModel
from fastapi.params import Body
from typing import Optional
from random import randrange

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class Post(BaseModel):
    title: str
    description: str
    published: bool = True
    rating: Optional[int] = None
    id: int = None


my_post =  [{"title": "hey title 1", "description": "description 1", "id": 1},{"title": "hey title 2", "description": "description 2", "id": 2}]

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
async def update_item(item_id:int, item: Item):
    return {"item_name": item.name, "item_id": item_id} 

# @app.post("/createPost")
# async def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"post": f"title: {payload['title']}, description: {payload['description']}", "title": payload["title"],"description": payload["description"]}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_post(new_post: Post):
    print(new_post)
    val = new_post.dict()
    val["id"] = randrange(1,1000000)
    my_post.append(val)

    return {"dict": my_post}

    
# initialize the first python file


from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel
from fastapi.params import Body
from typing import Optional

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

@app.post("/createPost")
async def create_post(new_post: Post):
    print(new_post)
    val = new_post.dict()
    return {"post": f"title: {new_post.title}, description: {new_post.description}", "dict": val}
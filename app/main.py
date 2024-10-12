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

from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

load_dotenv()


app = FastAPI()


while True:
        try:
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
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def read_root():

    return {"Hello": "World"}

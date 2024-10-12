from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from typing import List, Union
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

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
from .. import schema, models
from sqlalchemy.orm import Session


router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schema.Token)
def login(user_info: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_info.username).first()
    # print(user)

    if not user or not utils.verify_password(user_info.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
    
    access_token = oAuth.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}
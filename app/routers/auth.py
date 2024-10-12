from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from typing import List, Union

from .. import schema, models, utils


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


@router.post('/login')
def login(user_info: schema.UserLogin, db: Session = Depends(get_db)):
    # print(user_info)
    
    user = db.query(models.User).filter(models.User.email == user_info.email).first()
    # print(user)

    if not user or not utils.verify_password(user_info.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

    # access_token_expires = time.timedelta(minutes=60)
    # access_token = utils.create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)

    # return {'access_token': access_token, 'token_type': 'bearer'}
    return {'message': 'Logged in successfully'}

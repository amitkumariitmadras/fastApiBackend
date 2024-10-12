from jose import jwt, JWTError
from datetime import datetime, timedelta
# secret key
#Algorithm  : hs256
# Expiration time
import os
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from . import schema, models, database
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
# Load environment variables from.env file
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire_delta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    expire = datetime.utcnow() + expire_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_access_token(token: str, credentials_exception):

    print("verify_access_token")
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)

        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        
        token_data = schema.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    # user = db.query(models.User).filter(models.User.id == token.id).first()

    return token

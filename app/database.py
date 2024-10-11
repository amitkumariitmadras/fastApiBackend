import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from dotenv import load_dotenv


load_dotenv()

host=os.getenv('HOST'),
database=os.getenv('DATABASE'),
user= os.getenv('USERNAME'),
password=os.getenv('PASSWORD')


SQLALCHEMY_DATABASE_URL = "postgresql://{user}:{password}@{host}/{database}"
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
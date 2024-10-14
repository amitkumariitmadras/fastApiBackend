import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from .config import settings

print(settings.database_username)


# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

load_dotenv()

# host=os.getenv('HOST')
# database=os.getenv('DATABASE')
# user= os.getenv('USERNAME')
# password=os.getenv('PASSWORD')



# SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{database}"
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

print("database connection established")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




#Just for documentation

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

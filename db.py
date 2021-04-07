from sqlalchemy import create_engine
import sqlalchemy


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

try:
    DATABASE_URL = os.environ['DATABASE_URL']
except KeyError as e:
    print("Using static database URL")
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/morr"

database = sqlalchemy.create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database)

Base = declarative_base()
connection = database.connect()
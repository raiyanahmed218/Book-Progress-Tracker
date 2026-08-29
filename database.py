from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# create the engine — this is the connection to the database
engine = create_engine(DATABASE_URL)

# each request gets its own session — a session is a transaction with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for all our models
Base = declarative_base()

# define the User model — this maps to a "users" table in the database
class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    password = Column(String)

# define the Book model — this maps to a "books" table in the database
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)  # links the book to a user
    title = Column(String)
    total_pages = Column(Integer)
    current_page = Column(Integer)

# create all tables in the database if they don't exist
Base.metadata.create_all(bind=engine)

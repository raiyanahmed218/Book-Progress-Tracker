import fastapi
import pydantic
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal, User, Book, engine
from dotenv import load_dotenv
import os

load_dotenv()

# what app is is the FastAPI instance, we will use it to define our endpoints and run the server
app = fastapi.FastAPI()

# CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"])

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
ALGORITHM = "HS256"

# pydantic models for request body parsing
class BookModel(pydantic.BaseModel):
    title: str
    total_pages: int = pydantic.Field(gt=0)
    current_page: int = pydantic.Field(ge=0)

class NewUser(pydantic.BaseModel):
    password: str

class LoginUser(pydantic.BaseModel):
    password: str

# helper to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# root endpoint
@app.get("/")
async def root():
    return {"message": "BPT API is running"}

# retrieve books for a user
@app.get("/books/{username}")
async def get_books(username: str, db: Session = fastapi.Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return fastapi.responses.JSONResponse(content={"error": "User not found"}, status_code=404)
    books = db.query(Book).filter(Book.username == username).all()
    return fastapi.responses.JSONResponse(content=[
        {"title": b.title, "total_pages": b.total_pages, "current_page": b.current_page}
        for b in books
    ], status_code=200)

# create a new user
@app.post("/newUser/{newUserName}")
async def make_new_user(newUserName: str, newUser: NewUser, db: Session = fastapi.Depends(get_db)):
    existing = db.query(User).filter(User.username == newUserName).first()
    if existing:
        return fastapi.responses.JSONResponse(content={"error": f"User '{newUserName}' already exists"}, status_code=409)
    
    hashed_password = pwd_context.hash(newUser.password)
    user = User(username=newUserName, password=hashed_password)
    db.add(user)
    db.commit()
    return fastapi.responses.JSONResponse(content={"message": f"User '{newUserName}' successfully created"}, status_code=201)

# login
@app.post("/login/{username}")
async def login(username: str, loginUser: LoginUser, db: Session = fastapi.Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return fastapi.responses.JSONResponse(content={"error": "User not found"}, status_code=404)
    
    if not pwd_context.verify(loginUser.password, user.password):
        return fastapi.responses.JSONResponse(content={"error": "Incorrect password"}, status_code=401)
    
    token = jwt.encode({
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }, SECRET_KEY, algorithm=ALGORITHM)
    
    return fastapi.responses.JSONResponse(content={"token": token}, status_code=200)

# add a book
@app.post("/books/{username}")
async def add_book(username: str, book: BookModel, db: Session = fastapi.Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return fastapi.responses.JSONResponse(content={"error": "User not found"}, status_code=404)
    
    existing_book = db.query(Book).filter(Book.username == username, Book.title == book.title).first()
    if existing_book:
        return fastapi.responses.JSONResponse(content={"error": "Book already exists"}, status_code=409)
    
    new_book = Book(username=username, title=book.title, total_pages=book.total_pages, current_page=book.current_page)
    db.add(new_book)
    db.commit()
    return fastapi.responses.JSONResponse(content={"message": "Successfully added entry!"}, status_code=201)

# update a book
@app.put("/books/{username}/{prevBookName}")
async def update_book(username: str, prevBookName: str, updatesToBook: BookModel, db: Session = fastapi.Depends(get_db)):
    book = db.query(Book).filter(Book.username == username, Book.title == prevBookName).first()
    if not book:
        return fastapi.responses.JSONResponse(content={"error": f"Book '{prevBookName}' not found"}, status_code=404)
    
    book.title = updatesToBook.title
    book.total_pages = updatesToBook.total_pages
    book.current_page = updatesToBook.current_page
    db.commit()
    return fastapi.responses.JSONResponse(content={"message": f"Book '{prevBookName}' successfully updated"}, status_code=200)

# delete a book
@app.delete("/books/{username}/{bookName}")
async def delete_book(username: str, bookName: str, db: Session = fastapi.Depends(get_db)):
    book = db.query(Book).filter(Book.username == username, Book.title == bookName).first()
    if not book:
        return fastapi.responses.JSONResponse(content={"error": f"Book '{bookName}' not found"}, status_code=404)
    
    db.delete(book)
    db.commit()
    return fastapi.responses.JSONResponse(content={"message": f"Book '{bookName}' successfully removed"}, status_code=200)

# to run use -> python3 -m uvicorn main:app --reload

from fastapi import FastAPI
from pathlib import Path
from pydantic import BaseModel
import json

app = FastAPI()

class Book(BaseModel):
    title: str
    total_pages: int
    current_page: int


@app.get("/")
async def root():
    return {"message": "BPT API is running"}

# retrieve data
@app.get("/books/{username}")
async def get_books(username: str):
    file = Path("Users") / f"{username}.json"
    if not file.exists():
        return {"error": "User not found"}
    with open(file, 'r') as f:
        return json.load(f)
    

@app.post("/books/{username}")
async def add_book(username: str,book: Book):
        
        file = Path("Users") / f"{username}.json" # this makes a Path object
        with open(file, 'r') as f:
             userData = json.load(f)
        
        for b in userData:
             if b["title"] == book.title:
                  return {"error": "Book already exists"}
        if book.total_pages <= 0:
             return {"error": "Total pages must exceed 0"}
        if book.current_page < 0:
             return {"error": "Current page must be positive"}
        

        userData.append(book.model_dump())

        with open(file, 'w') as f:
                json.dump(userData, f)
        return {"message": "Successfully added entry!"}
    
# TO DO NEXT: figure out how to read from file in main.py and error check like in bookPageTracker.py

from fastapi import FastAPI
from pathlib import Path
from pydantic import BaseModel, Field
import json

app = FastAPI()

class Book(BaseModel):
    title: str
    total_pages: int = Field(gt=0)
    current_page: int = Field(ge=0)


@app.get("/")
async def root():
    return {"message": "BPT API is running"}

# retrieve data
@app.get("/books/{username}")
async def get_books(username: str):
    file = Path("Users") / f"{username}.json"
    # because we dont open the file here, it wont create the file if it doesn't exist, so we can check for the file's existence before trying to read it
    if not file.exists():
        return {"error": "User not found"}
    with open(file, 'r') as f:
        return json.loads(f)
    

@app.post("/books/{username}")
async def add_book(username: str, book: Book):
        
        file = Path("Users") / f"{username}.json" # this makes a Path object
        if not file.exists():
             return {"error": "User not found"}
        with open(file, 'r') as f: # this will create the file if it doesn't exist, and open it for reading
            content = f.read()
            if content == "":
                userData = []
            else:
                userData = json.loads(content)
        
        for b in userData:
             if b["title"] == book.title:
                  return {"error": "Book already exists"}
             
        # so bcz we got Field validators from Pydantic, we don't need to check for total_pages and current_page validity here
        # if book.total_pages <= 0:
        #      return {"error": "Total pages must exceed 0"}
        # if book.current_page < 0:
        #      return {"error": "Current page must be positive"}
        

        userData.append(book.model_dump())

        with open(file, 'w') as f:
                json.dump(userData, f)
        return {"message": "Successfully added entry!"}

@app.put("/books/{username}")
async def update_book(username: str, prevBook: Book, updatedBook: Book):
     # verification first
    file = Path("Users") / f"{username}.json"
    with open(file, 'r') as f:
        content = f.read()
        if content == "":
            return {"error": "No books to update"}
        else:
            userData = json.loads(content)
    for b in userData:
        if b["title"] == prevBook.title:
            b["title"] = updatedBook.title
        
        
    

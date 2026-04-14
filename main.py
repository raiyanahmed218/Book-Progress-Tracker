import fastapi
import pathlib
import pydantic
import json

app = fastapi.FastAPI()

class Book(pydantic.BaseModel): # this handles automatic parsing from body to fit the structure specified and matches exactly with the name of the keys in the model and from the body.
    title: str
    total_pages: int = pydantic.Field(gt=0)
    current_page: int = pydantic.Field(ge=0)


@app.get("/")
async def root():
    return {"message": "BPT API is running"}

# helper function to get the file
def get_user_file(username: str):
    file = pathlib.Path("Users")/f"{username}.json" # this makes a Path object
    if file.exists():
        return file
    else:
        return None

# retrieve data
@app.get("/books/{username}")
async def get_books(username: str):
    # because we dont open the file here, it wont create the file if it doesn't exist, so we can check for the file's existence before trying to read it
    file = get_user_file(username)
    if not file:
        return {"error": "User not found"}
    with open(file, 'r') as f:
        return json.load(f)

# add a new user 
@app.post("/newUser/{newUserName}")
async def make_new_user(newUserName: str):
    file = get_user_file(newUserName)
    if file:
        return {"error": f"User {newUserName} already exists"}
    
    try:
        with open(file, 'w') as f:
            json.dump([], f)
        return {"message": f"User {newUserName} successfully created"}
    except OSError as e:
        return {"error": str(e)}
    

@app.post("/books/{username}")
async def add_book(username: str, book: Book):
        file = get_user_file(username)
        if not file:
             return {"error": "User not found"}
        with open(file, 'r') as f: # this will not create a new file if "file" doesnt exist, only in w or a mode it makes a new empty file if the file alr doesnt exist
            # 'r' - read, errors if file doesn't exist
            # 'w' - write, creates file if doesn't exist, OVERWRITES if it does
            # 'a' - append, creates file if doesn't exist, adds to end if it does
            # 'x' - create, creates file, errors if it already exists
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

        with open(file, 'w') as f: # we write here and not append because we read the existing data, modify and re-wrtie (overwriting the previous data).
                json.dump(userData, f)
        return {"message": "Successfully added entry!"}

@app.put("/books/{username}/{prevBookName}") # we have prevBookName in the url because data can only be retrieved from body or from url and since we cant send two Book as python wont know which json structure to parse to prevBook and updatedBook, we changed prevBook to just the name and now we send it through url
async def update_book(username: str, prevBookName: str, updatesToBook: Book):
    file = get_user_file(username)
    # check if file exists
    if not file:
         return {"error": "User does not exist"}
    
    # get the current userdata
    with open(file, 'r') as f:
        content = f.read()
        if content == "":
            return {"error": "No books to update"}
        else:
            userData = json.loads(content)
    # check for if the specified book exists
    for b in userData:
        # update book
        if b["title"] == prevBookName:
            b["title"] = updatesToBook.title
            b["total_pages"] = updatesToBook.total_pages
            b["current_page"] = updatesToBook.current_page
            # write new userdata back to file
            with open(file, 'w') as f:
                json.dump(userData, f)
            return {"message": f"Book {prevBookName} successfully updated"}
    
    return {"error": f"Book {prevBookName} not found"}

     
    
# to run use -> python -m uvicorn main:app --reload














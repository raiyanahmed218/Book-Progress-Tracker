import fastapi
import pathlib
import pydantic
import json
# CORS (Cross-Origin Resource Sharing) is a security feature implemented by web browsers to restrict web pages from making requests to a different domain than the one that served the web page. This is done to prevent malicious websites from accessing sensitive data on other domains without the user's consent. By default, web browsers block cross-origin requests for security reasons.
from fastapi.middleware.cors import CORSMiddleware
# what we will use to hash.
from passlib.context import CryptContext
# settings for the hash we will use.
pwd_context = CryptContext(schemes=["bcrypt"])

# we will use this to generate and verify JWT tokens for authentication.
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key-change-this"
ALGORITHM = "HS256"

# what app is is the FastAPI instance, we will use it to define our endpoints and run the server
app = fastapi.FastAPI()

# CORS middleware is added to the FastAPI application to allow cross-origin requests from the specified origin (http://localhost:5173). This is necessary for the frontend (running on a different port) to communicate with the backend API without being blocked by the browser's same-origin policy.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models are used to define the structure and validation of data that is sent to and received from the API. They help ensure that the data adheres to the expected format and types, making it easier to work with and reducing the likelihood of errors.
class LoginUser(pydantic.BaseModel):
    password: str

class Book(pydantic.BaseModel): # this handles automatic parsing from body to fit the structure specified and matches exactly with the name of the keys in the model and from the body.
    title: str
    total_pages: int = pydantic.Field(gt=0)
    current_page: int = pydantic.Field(ge=0)

class NewUser(pydantic.BaseModel):
    password: str


# this is the root endpoint, just to check if the server is running, we can test it by going to http://
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

# retrieve data/ view book data
@app.get("/books/{username}")
async def get_books(username: str):
    # because we dont open the file here, it wont create the file if it doesn't exist, so we can check for the file's existence before trying to read it
    file = get_user_file(username)
    if not file:
        return fastapi.responses.JSONResponse(content={"error": "User not found"}, status_code=404)
    with open(file, 'r') as f:
        userData = json.load(f)
        return fastapi.responses.JSONResponse(content=userData["books"], status_code=200)

# add a new user 
@app.post("/newUser/{newUserName}")
async def make_new_user(newUserName: str, newUser: NewUser):
    file = pathlib.Path("Users") / f"{newUserName}.json"
    # this makes the parent directory if it doesn't exist, and if it does exist, it does nothing because of exist_ok=True, and parents=True allows it to make multiple levels of directories if needed, but in this case we only have one level of directory which is "Users"
    file.parent.mkdir(exist_ok=True, parents=True)
    # if the file already exists, return an error 
    if file.exists():
        return fastapi.responses.JSONResponse(content={"error": f"User '{newUserName}' already exists"}, status_code=409)

    try:
        # this makes the file
        with open(file, 'w') as f:
            json.dump({"password": pwd_context.hash(newUser.password), "books": []}, f)
        return fastapi.responses.JSONResponse(content={"message": f"User '{newUserName}' successfully created"}, status_code=201)
    except OSError as e:
        return fastapi.responses.JSONResponse(content={"error": str(e)}, status_code=400)
    
# add a book to a user that exists
@app.post("/books/{username}")
async def add_book(username: str, book: Book):
        file = get_user_file(username)
        if not file:
            return fastapi.responses.JSONResponse(content={"error": "User not found"}, status_code=404)
        with open(file, 'r') as f: # this will not create a new file if "file" doesnt exist, only in w or a mode it makes a new empty file if the file alr doesnt exist
            # 'r' - read, errors if file doesn't exist
            # 'w' - write, creates file if doesn't exist, OVERWRITES if it does
            # 'a' - append, creates file if doesn't exist, adds to end if it does
            # 'x' - create, creates file, errors if it already exists


            # content = f.read()
            # if content == "":
            #     userData = []
            # else:
                # userData = json.loads(content)
            userData = json.load(f) # so since make new user creates a file with [] and also at the start of this function we check if the file exists, we can be sure that the file exists and has [] if there are no books, so we can just do json.load without checking for empty string first.
            
        for b in userData["books"]: # this is reading Book objects from a list
             if b["title"] == book.title:
                  return fastapi.responses.JSONResponse(content={"error": "Book already exists"}, status_code=409)
             
        # so bcz we got Field validators from Pydantic, we don't need to check for total_pages and current_page validity here
        # if book.total_pages <= 0:
        #      return {"error": "Total pages must exceed 0"}
        # if book.current_page < 0:
        #      return {"error": "Current page must be positive"}
        

        userData["books"].append(book.model_dump())

        with open(file, 'w') as f: # we write here and not append because we read the existing data, modify and re-wrtie (overwriting the previous data).
                json.dump(userData, f)
        return fastapi.responses.JSONResponse(content={"message": "Successfully added entry!"}, status_code=201)

# update a book for a user that exists
@app.put("/books/{username}/{prevBookName}") # we have prevBookName in the url because data can only be retrieved from body or from url and since we cant send two Book as python wont know which json structure to parse to prevBook and updatedBook, we changed prevBook to just the name and now we send it through url
async def update_book(username: str, prevBookName: str, updatesToBook: Book):
    file = get_user_file(username)
    # check if file exists
    if not file:
        return fastapi.responses.JSONResponse(content={"error": "User does not exist"}, status_code=404)
    
    # get the current userdata
    with open(file, 'r') as f:
        # content = f.read()
        # if content == "":
        #     return {"error": "No books to update"}
        # else:
        #     userData = json.loads(content)
        userData = json.load(f)
    # check for if the specified book exists
    for b in userData["books"]:
        # update book
        if b["title"] == prevBookName:
            b["title"] = updatesToBook.title
            b["total_pages"] = updatesToBook.total_pages
            b["current_page"] = updatesToBook.current_page
            # write new userdata back to file
            with open(file, 'w') as f:
                json.dump(userData, f)
            return fastapi.responses.JSONResponse(content={"message": f"Book '{prevBookName}' successfully updated"}, status_code=200)
    
    return fastapi.responses.JSONResponse(content={"error": f"Book '{prevBookName}' not found"}, status_code=404)

# delete a book for a user that exists
@app.delete("/books/{username}/{bookName}")
async def delete_book(username: str, bookName: str):
    file = get_user_file(username)

    if not file:
        return fastapi.responses.JSONResponse(content={"error": "User does not exist"}, status_code=404)

    with open(file, "r") as f:
        userData = json.load(f)
    
    for b in userData["books"]:
        if b["title"] == bookName:
            # .pop(index) or .remove(specific element) for lists
            # .pop(key) for dicts and we also get the value
            userData["books"].remove(b)
            with open(file, "w") as f:
                json.dump(userData, f)
            return fastapi.responses.JSONResponse(content={"message": f"Book '{bookName}' successfully removed"}, status_code=200)
    return fastapi.responses.JSONResponse(content={"error": f"Book '{bookName}' not found"}, status_code=404)

# login a user
@app.post("/login/{username}")
async def login(username: str, loginUser: LoginUser):
    file = get_user_file(username)
    if not file:
        return fastapi.responses.JSONResponse(content={"error": "User not found"}, status_code=404)
    
    with open(file, 'r') as f:
        userData = json.load(f)
    
    if not pwd_context.verify(loginUser.password, userData["password"]):
        return fastapi.responses.JSONResponse(content={"error": "Incorrect password"}, status_code=401)
    
    token = jwt.encode({
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }, SECRET_KEY, algorithm=ALGORITHM)
    
    return fastapi.responses.JSONResponse(content={"token": token}, status_code=200)


# to run use -> python -m uvicorn main:app --reload
# python3 -m uvicorn main:app --reload













# Imports
from pathlib import Path
import sys
import json
import math


# check if user exists
def userFinder(name):
        while 1:
                file = Path("Users") / f"{name}.json" # creates a path object
                if file.exists():       # we cant just do "if file" since path objects are truthy by default unless explicitly empty e.g. {}
                        print("User found!")
                        break
                else:
                        print("User not found")
                        while 1:
                                newUser = input("Would you like to make a new user? (Y/N): ")
                                if newUser.upper() == "Y":
                                        file.touch() # This creates a new user and incase they exists doesnt do anything
                                        with open(file, "w") as f:
                                                json.dump([], f)
                                        print("New user created!")
                                        break
                                elif newUser.upper() == "N":
                                        print("Try again later with a valid user")
                                        sys.exit()
                break
# reads file and transforms into python objects
def retrieveData(name):
                file = Path("Users") / f"{name}.json" # this makes a Path object
                with open(file, 'r') as f:
                        content = f.read()
                        if content == "":
                                return []
                        else:
                                 return json.loads(content)
# add an entry          
def addEntry(name, userData):
        userDataNew = {}
        while True:
                newBook = input("What is the name of the book? ").upper()
                for book in userData:
                        if newBook == book["Book Name"]:
                                print(f"Book {newBook} already exists! Try again.")
                                return
                break
        userDataNew["Book Name"] = newBook
        while True:
                pages = input("what is the total number of pages? ")
                try:
                        totalPages = int(pages)
                        if totalPages <= 0:
                                print("Total pages must be more than 0!")
                                continue
                        break
                except ValueError:
                        print("Please enter a valid number.")
        userDataNew["Total Pages"] = totalPages
        while True:
                pages = input("what is the current page you're on? ")
                try:
                        currentPage = int(pages)
                        break
                except ValueError:
                        print("Please enter a valid number.")
        userDataNew["Current Page"] = currentPage
        
        userData.append(userDataNew)
        file = Path("Users") / f"{name}.json" # this makes a Path object
        with open(file, 'w') as f:
                json.dump(userData, f)
        print("Successfully added entry!")
# view books for a user
def viewBooks(userData):
        for book in userData:
                for key, value in book.items():
                        print(f"{key} : {value}")
                print("\n")
# update an entry
def updateEntry(name):
        bookName = str(input("What is the name of the book you want to update? ")).upper()
        userData = retrieveData(name)
        for book in userData:
                if book["Book Name"] == bookName:
                        print("Entry found and ready to update. ")
                        bookPosNum = userData.index(book)
                        userData.remove(book)
                        while True:
                                updateName = input(f"Would you like to change the name of the book? It is currently '{book['Book Name']}' (Y/N) ").upper()
                                if updateName == "Y":
                                        book["Book Name"] = input("What is the name of the book? ").upper()
                                        break
                                elif updateName == "N":
                                        print(f"Name kept as '{book['Book Name']}'")
                                        break
                                else:
                                        continue
                        while True:
                                updateTotalPages = input(f"Would you like to change the total pages for the book? It is currently '{book['Total Pages']}' (Y/N) ").upper()
                                if updateTotalPages == "Y":
                                        while True:
                                                totalPages = input("What is the total page number of the book? ")
                                                try:
                                                        newTotalPages = int(totalPages)
                                                        break
                                                except ValueError:
                                                        print("Please enter a valid number.")
                                        book["Total Pages"] = newTotalPages   
                                        break    
                                elif updateTotalPages == "N":
                                        print(f"Total pages for '{book['Book Name']}' kept at {book['Total Pages']}")
                                        break
                                else:
                                        continue
                        while True:
                                updateCurrentPages = input(f"Would you like to change the current page you're on in the book? It is currently '{book['Current Page']}' (Y/N) ").upper()
                                if updateCurrentPages == "Y":
                                        while True:
                                                currPage = input("What is the current peage you are on in the book? ")
                                                try:
                                                        newCurrPages = int(currPage)
                                                        break
                                                except ValueError:
                                                        print("Please enter a valid number.")
                                        book["Current Page"] = newCurrPages     
                                        break
                                elif updateCurrentPages == "N":
                                        print(f"Current page for '{book['Book Name']}' kept at {book['Current Page']}")
                                        break
                                else:
                                        continue
                        userData.insert(bookPosNum, book)
                        file = Path("Users") / f"{name}.json"
                        with open (file, 'w') as f:
                                json.dump(userData, f)
                        print(f"Successfully Updated to {book['Book Name']}")
                        return
                else:   
                        continue                        
        print("Book Not Found")

# delete an entry
def deleteEntry(name):
        userData = retrieveData(name)
        bookToDelete = input(f"What is the name of the book you wish to delete? ").upper()
        for book in userData:
                if book["Book Name"] == bookToDelete:
                        userData.remove(book)
                        print(f"{bookToDelete} removed")
                        file = Path("Users") / f"{name}.json"
                        with open (file, 'w') as f:
                                json.dump(userData, f)  
                        return
        print(f"No book found by the name '{bookToDelete}'")             

# main
def main():
        print("\n----- Welcome to BPT, the Book Progress Tracker software -----\n\n\n")
        name = input("What is your username? ")
        userFinder(name)
        print(f"Welcome {name}")
        while True:
                userData = retrieveData(name)
                command = input("Enter a command (H for Help): ")
                print("\n")
                if command.upper() == "V":
                        viewBooks(userData)
                elif command.upper() == "Q":
                        sys.exit()
                elif command.upper() == "A":
                        addEntry(name, userData)
                elif command.upper() == "U":
                        updateEntry(name)
                elif command.upper() == "D":
                        deleteEntry(name)
                elif command.upper() == "H":
                        print("V = View Entries\nQ = Quit\nA = Add Entry\nU = Update Entry\nD = Delete Entry\nH = Help\n")



main()



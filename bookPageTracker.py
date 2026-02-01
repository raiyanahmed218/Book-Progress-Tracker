# Imports
from pathlib import Path
import sys
import json
import math
# Introduction Sequence
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
                                newUser = input("Would you like to make a new user? (y/n): ")
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

def retrieveData(name):
                file = Path("Users") / f"{name}.json" # this makes a Path object
                with open(file, 'r') as f:
                        content = f.read()
                        if content == "":
                                return []
                        else:
                                 return json.loads(content)
        
def addEntry(name, userData):
        userDataNew = {}
        userDataNew["Book Name"] = input("What is the name of the book? ").upper()
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

def viewBooks(userData):
        for book in userData:
                for key, value in book.items():
                        print(f"{key} : {value}")
                print("\n")

def updateEntry(name):
        bookName = input("What is the name of the book you want to update? ")
        userData = retrieveData(name)




def main():
        print("\n----- Welcome to BPT, the Book Progress Tracker software -----\n\n\n")
        name = input("What is your username? ")
        userFinder(name)
        print(f"Welcome {name}")
        global userData
        userData = retrieveData(name)
        while True:
                command = input("Enter a command: ")
                print("\n")
                if command.upper() == "V":
                        viewBooks(userData)
                elif command.upper() == "Q":
                        sys.exit()
                elif command.upper() == "A":
                        addEntry(name, userData)
                elif command.upper() == "U":
                        updateEntry(name)
                        #update
                        #delete




main()

# 

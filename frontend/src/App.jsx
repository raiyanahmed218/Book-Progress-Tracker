import React from "react"
import './App.css'

function App() {
    // --- STATE ---
    // IMPORTANT: general loop is make a variable that also gets set and then in the return,
    // check if the variable is set and return something on the webpage based on that

    const [username, setUsername] = React.useState("")         // the username typed in the search bar
    const [password, setPassword] = React.useState("")         // password input, reused for both login and create account
    const [token, setToken] = React.useState(localStorage.getItem("token") || "")               // JWT token returned from the server after login
    const [loggedIn, setLoggedIn] = React.useState(false)      // whether the user is logged in
    const [showLogin, setShowLogin] = React.useState(false)    // show the login password form (user exists)
    const [showCreateAccount, setShowCreateAccount] = React.useState(false) // show create account form (user doesn't exist)

    const [books, setBooks] = React.useState([])               // list of books for the logged in user
    const [covers, setCovers] = React.useState({})             // map of book title -> cover image URL
    const [newTitle, setNewTitle] = React.useState("")         // new book title input
    const [newCurrentPage, setNewCurrentPage] = React.useState("") // new book current page input
    const [newTotalPages, setNewTotalPages] = React.useState("")   // new book total pages input
    const [addBook, setAddBook] = React.useState(false)        // whether to show the add book form

    const [loading, setLoading] = React.useState(false)        // whether a request is in flight
    const [errors, setErrors] = React.useState("")             // error message to display
    const [success, setSuccess] = React.useState("")           // success message to display

    const [okButtonClicked, setOkButtonClicked] = React.useState(false) // whether the OK button was clicked to check user existence

    // --- FUNCTIONS ---

    // checkUser: called when the user clicks OK
    // checks if the user exists and shows the appropriate form
    // if the user exists -> show login form
    // if the user doesn't exist -> show create account form
    async function checkUser() {
        setLoading(true)
        setErrors("")
        setShowLogin(false)
        setShowCreateAccount(false)
        setPassword("")
        try {
            const response = await fetch(`http://127.0.0.1:8000/books/${username}`)
            if (response.status === 404) {
                setShowCreateAccount(true)
                throw new Error("User not found — create an account to continue")
            }
            if (!response.ok) {
                throw new Error("Something went wrong")
            }
            // user exists, show the login form
            setShowLogin(true)
            setOkButtonClicked(true)
        } catch (err) {
            setErrors(err.message)
        } finally {
            setLoading(false)
        }
    }

    // login: called when the user clicks Login
    // sends the username and password to the server
    // if the password matches the stored hash, the server returns a JWT token
    // we store the token and call getBooks to load the user's books
    async function login() {
        setLoading(true)
        setErrors("")
        try {
            const response = await fetch(`http://127.0.0.1:8000/login/${username}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ password })  // send password in body, not URL, for security
            })
            if (response.status === 401) {
                throw new Error("Incorrect password")
            }
            if (response.status === 404) {
                throw new Error("User not found")
            }
            if (!response.ok) {
                throw new Error("Something went wrong")
            }
            const data = await response.json()
            setToken(data.token)       // store the JWT token for future authenticated requests
            setLoggedIn(true)          // mark the user as logged in
            setShowLogin(false)        // hide the login form
            setPassword("")            // clear the password field
            setSuccess("")
            // after login, save to localStorage
            localStorage.setItem("token", data.token)
            await getBooks()           // load the user's books
        } catch (err) {
            setErrors(err.message)
        } finally {
            setLoading(false)
        }
    }

    // createAccount: called when the user clicks Create Account
    // sends the username and password to the server to create a new user
    // on success, automatically logs the user in
    async function createAccount() {
        setLoading(true)
        setErrors("")
        try {
            const response = await fetch(`http://127.0.0.1:8000/newUser/${username}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ password })
            })
            if (response.status === 409) {
                throw new Error("Username already exists")
            }
            if (!response.ok) {
                throw new Error("Something went wrong")
            }

            setSuccess("Account created! Logging you in...")
            setShowCreateAccount(false)
            await login()   // automatically log in after creating account
        } catch (err) {
            setErrors(err.message)
        } finally {
            setLoading(false)
        }
    }

    // getBooks: fetches the user's books from the server and updates the books state
    // also fetches cover images for each book from the Open Library API
    async function getBooks() {
        setLoading(true)
        setErrors("")
        setBooks([])
        setAddBook(false)
        try {
            const response = await fetch(`http://127.0.0.1:8000/books/${username}`)
            if (!response.ok) {
                throw new Error("Something went wrong")
            }

            const data = await response.json()
            setBooks(data)
            setAddBook(true)

            // fetch cover images for each book and store in a map keyed by title
            const coverMap = {}
            for (const book of data) {
                const url = await getBookCover(book.title)
                if (url) {
                    coverMap[book.title] = url
                }
            }
            setCovers(coverMap)
        } catch (err) {
            setErrors(err.message)
        } finally {
            setLoading(false)
        }
    }

    // addBookFunc: called when the user clicks Add Book
    // sends the new book data to the server and refreshes the book list
    async function addBookFunc() {
        setLoading(true)
        setErrors("")
        try {
            const response = await fetch(`http://127.0.0.1:8000/books/${username}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    title: newTitle,
                    current_page: parseInt(newCurrentPage), // parseInt because input values are always strings
                    total_pages: parseInt(newTotalPages)
                })
            })
            if (!response.ok) {
                throw new Error("Something went wrong")
            }
            await getBooks()        // refresh the book list after adding
            setNewTitle("")         // clear the input fields
            setNewCurrentPage("")
            setNewTotalPages("")
        } catch (err) {
            setErrors(err.message)
        } finally {
            setLoading(false)
        }
    }

    // getBookCover: fetches the cover image URL for a book from the Open Library API
    // uses optional chaining (?.) to safely access nested properties without crashing
    // returns a default image if no cover is found
    async function getBookCover(title) {
        const response = await fetch(`https://openlibrary.org/search.json?title=${encodeURIComponent(title)}&limit=1`)
        const data = await response.json()
        const coverId = data.docs[0]?.cover_i  // ?. means "if docs[0] exists, get cover_i, otherwise return undefined"
        if (coverId) {
            return `https://covers.openlibrary.org/b/id/${coverId}-M.jpg`
        }
        return "/BookCoverNotFound.jpg"         // default image if no cover found
    }
    // signOut: clears the token and resets all state to initial values
    async function signOut() {
        localStorage.removeItem("token")
        setToken("")
        setLoggedIn(false)
        setUsername("")
        setPassword("")
        setShowLogin(false)
        setShowCreateAccount(false)
        setBooks([])
        setCovers({})
        setAddBook(false)
        setErrors("")
        setSuccess("")
        setNewTitle("")
        setNewCurrentPage("")
        setNewTotalPages("")
        setOkButtonClicked(false)
    }
    // deleteBook: called when the user clicks Delete on a book
    // sends a DELETE request to the server and refreshes the book list
    async function deleteBook(bookTitle) {
        setLoading(true)
        setErrors("")
        try {
            const response = await fetch(`http://127.0.0.1:8000/books/${username}/${encodeURIComponent(bookTitle)}`, {
                method: "DELETE"
            })
            if (!response.ok) {
                throw new Error("Something went wrong")
            }
            await getBooks()
        } catch (err) {
            setErrors(err.message)
        } finally {
            setLoading(false)
        }
    }

    // --- RENDER ---
    // each section is conditionally rendered based on state
    return (
        <div className="container">
            <div className="header-bar">
                <div className="header">
                    <h1>Book Page Tracker</h1>
                    <h2>Track the progress of books you are reading!</h2>
                </div>
                {loggedIn && (
                    <div className="signout">
                        <button onClick={signOut}>Sign Out</button>
                    </div>
                )}
            </div>

            {/* username search bar — hidden after logging in */}
            {loggedIn && (
                <div className="welcome">
                    <h3 className="welcome-message">Welcome, {username}!</h3>
                </div>
            )}
            {!loggedIn && (
                <div className="search-bar">
                    <input
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Enter username"
                    />
                    {!okButtonClicked && <button onClick={checkUser}>OK</button>}
                </div>
            )}

            {/* login form — shown when user exists and needs to enter password */}
            {showLogin && (
                <div className="search-bar">
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter password"
                    />
                    <button onClick={login}>Login</button>
                </div>
            )}

            {/* create account form — shown when user doesn't exist */}
            {showCreateAccount && (
                <div className="search-bar">
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Choose a password"
                    />
                    <button onClick={createAccount}>Create Account</button>
                </div>
            )}

            {errors && <p style={{color: "red", marginBottom: "20px"}}>{errors}</p>}
            {success && <p style={{color: "green"}}>{success}</p>}
            {loading && <p>Loading...</p>}

            {/* add book form — shown after logging in */}
            {addBook && (
                <div className="add-book">
                    <input
                        value={newTitle}
                        onChange={(e) => setNewTitle(e.target.value)}
                        placeholder="Book title"
                    />
                    <input
                        value={newCurrentPage}
                        onChange={(e) => setNewCurrentPage(e.target.value)}
                        placeholder="Current page"
                        type="number"
                    />
                    <input
                        value={newTotalPages}
                        onChange={(e) => setNewTotalPages(e.target.value)}
                        placeholder="Total pages"
                        type="number"
                    />
                    <button onClick={addBookFunc}>Add Book</button>
                </div>
            )}

            {/* book list */}
            <div className="book-list">
                {books.map((book, index) => (
                    <div className="book-item" key={index}>
                        <img className="image" src={covers[book.title]} alt={book.title} />
                        <div className="book-info">
                            <h4 className="h4InLine">Book {index + 1}</h4>
                            <h2 className="h2InLine">{book.title}</h2>
                            <h3 className="h3InLine">Page {book.current_page} of {book.total_pages}</h3>
                            <button className="delete-btn" onClick={() => deleteBook(book.title)}>Delete</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default App

// to start the app, run 'npm run dev' in the terminal

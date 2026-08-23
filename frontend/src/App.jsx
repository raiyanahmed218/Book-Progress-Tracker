import React from "react"
import './App.css'
function App() {
    // Using array destructuring to get the username and setUsername from useState
    // state[0] is the current value of username, and state[1] is the function to update it called the setter
    const [username, setUsername] = React.useState("")
    // alternatively, we could have done it without destructuring like this:
    // const state = React.useState("")
    // const username = state[0]
    // const setUsername = state[1]
    const [books, setBooks] = React.useState([])
    const [errors, setErrors] = React.useState("")
    // IMPORTANT: general loop is make a variable that also get set and then in the return, check if the variable is set and return something on the webpage based on that
    const [loading, setLoading] = React.useState(false)
    const [newUser, setNewUser] = React.useState(false)
    const [password, setPassword] = React.useState("")
    const [success, setSuccess] = React.useState("")


    
    async function getBooks() {
        setLoading(true)
        setErrors("")
        setBooks([])
        setNewUser(false)

        try {
            const response = await fetch(`http://127.0.0.1:8000/books/${username}`)

            if (response.status == 404) {
                setNewUser(true)
                throw new Error("User Not Found")
            }

            if (!response.ok) {
                throw new Error("Something Went Wrong")
            }

            const data = await response.json()
            setSuccess("")
            setNewUser(false)
            setBooks(data)
        } catch (err) {
            setErrors(err.message)
        } finally {
            setLoading(false)
        }
    }

    async function createAccount() {
        setLoading(true)
        setErrors("")
        setBooks([])
        setNewUser(false)

        try {
            const response = await fetch(`http://127.0.0.1:8000/newUser/${username}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ password })
            })

            if (response.status == 409) {
                throw new Error("Username already exists")
            }
            
            if (!response.ok) {
                throw new Error("Something Went Wrong")
            }
            
            setSuccess("Account created! You can now load your books.")
            setPassword("")
        } catch (err) {
            setErrors(err.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="container">
            <h1>Book Page Tracker</h1>
            <h2>Track the progress of books you are reading!</h2>
            <div className="search-bar">
                <input 
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Enter username"
                />
                <button onClick={getBooks}>Load Books</button>
            </div>

            {newUser && (
                <div className="search-bar">
                    <input 
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter password"
                    />
                    <button onClick={createAccount}>Create Account</button>
                </div>
            )}

            {success && <p style={{color: "green"}}>{success}</p>}

            {loading && <p>Loading...</p>}

            {errors && (
                <p style={{color: "red"}}>
                    {errors}
                </p>
            )}


            <div>
                {books.map((book, index) => (
                    <div className="book-item" key={index}>
                        <h4 className="h4InLine">Book: {index + 1}</h4>
                        <h2 className="h2InLine">Title: {book.title}</h2>
                        <h3 className="h3InLine">Page {book.current_page} of {book.total_pages}</h3>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default App

// to start the app, run 'npm run dev' in the terminal, and it will open in the browser at http://localhost:3000/

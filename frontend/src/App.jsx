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


    
    async function getBooks() {
        const response = await fetch(`http://127.0.0.1:8000/books/${username}`)
        const data = await response.json()
        setBooks(data)
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

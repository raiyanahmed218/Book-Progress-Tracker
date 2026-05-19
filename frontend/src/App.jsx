import React from "react"

function App() {
    // Using array destructuring to get the username and setUsername from useState
    // state[0] is the current value of username, and state[1] is the function to update it called the setter
    const [username, setUsername] = React.useState("")
    // alternatively, we could have done it without destructuring like this:
    // const state = React.useState("")
    // const username = state[0]
    // const setUsername = state[1]
  
    return (
        <div>
            <h1>Book Page Tracker</h1>
            <input 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter username"
            />
            <p>Hello, {username}</p>
        </div>
    )
}

export default App

// SignupForm.jsx
// This component is used for user signup. It takes in the username, password, and their respective setter functions, as well as an onSignup function that is called when the user clicks the "Create Account" button.
function SignupForm({ username, setUsername, password, setPassword, onSignup }) {
    return (
        <div className="search-bar">
            <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Choose a username"
            />
            <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Choose a password"
            />
            <button onClick={onSignup}>Create Account</button>
        </div>
    )
}

export default SignupForm

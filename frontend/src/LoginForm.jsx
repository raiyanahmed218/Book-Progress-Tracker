// LoginForm.jsx
// This component is used for user login. It takes in the username, password, and their respective setter functions, as well as an onLogin function that is called when the user clicks the "Login" button. It also takes in an onCheckUser function that is called when the user clicks the "OK" button to check if the username exists. The showLogin prop determines whether to show the password input and login button, and the okButtonClicked prop determines whether the "OK" button has been clicked.
function LoginForm({ username, setUsername, password, setPassword, onLogin, onCheckUser, showLogin, okButtonClicked }) {
    return (
        <>
            <div className="search-bar">
                <input
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Enter username"
                />
                {!okButtonClicked && <button onClick={onCheckUser}>OK</button>}
            </div>

            {showLogin && (
                <div className="search-bar">
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter password"
                    />
                    <button onClick={onLogin}>Login</button>
                </div>
            )}
        </>
    )
}

export default LoginForm

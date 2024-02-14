import React, { useState } from 'react';
import './Login.css';
import HomePage from './HomePage'; // Import the HomePage component

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loggedIn, setLoggedIn] = useState(false); // State to track login status
    const [error, setError] = useState(''); // State to track login error

    const handleLogin = (e) => {
        e.preventDefault();
        // Check if email and password match
        if ((username === 'ommprakash@iitbhilai.ac.in' && password === 'Demopassword@2004' ) || (username === 'haso' && password ==='haso')) {
            // Set logged in state to true if match
            setLoggedIn(true);
        } else {
            // Set error message if not match
            setError('Invalid email or password');
        }
    }

    // If logged in, render the HomePage component
    if (loggedIn) {
        return <HomePage />;
    }

    return (
        <div className="login-container">
            <h2 className="login-heading">Login</h2>
            {error && <p className="error-message">{error}</p>}
            <form onSubmit={handleLogin}>
                <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
                <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default Login;

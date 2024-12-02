import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Register.css'

export default function Register() {
  const navigate = useNavigate();
  const [showForm, setShowForm] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');

  const handleRegister = (e) => {
    e.preventDefault();
    // Basic form validation
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    if (password < 5 ||password > 14 || !/^[a-zA-Z0-9]+$/.test(password)) {
        setError('Password should be between 5 and 14 characters, Contains both english letters and numbers only');
        return;
      }

    // Clear error message
    setError('');
    registerUser();

  };

  // Update your register function
  const registerUser = async () => {
    try {
        const response = await fetch(`http://localhost:5000/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
            }),
        });
        if (!response.ok) {
            throw new Error('Username or Email Already Exists!');
        }

        const data = await response.json();
        console.log(data.message);
        navigate('/Welcome');
    } catch (error) {
        console.error('Error:', error);
        alert('Error: ' + error.message);
    }
};


const handleSubmit = (event) => {
  event.preventDefault(); // Prevent the default form submission
  registerUser(); // Call the register function
};

  return (
    <div className="register-container">
      <h1>Welcome!</h1>
      <p>Please register to get started.</p>
      {!showForm ? (
        <button onClick={() => setShowForm(true)} className="register-toggle-button">
          Register
        </button>
      ) : (
        <form onSubmit={handleRegister} className="register-form">
          {error && <p className="error">{error}</p>}
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onInvalid={(e) => {
                e.preventDefault();
                setError('Please enter a valid email address');
              }}
              onInput={() => setError('')} // Clear error when user starts typing again
              required
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Confirm Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="register-button">Register</button>
        </form>
      )}
    </div>
  );
}

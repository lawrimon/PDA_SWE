import './Settings.css';
import logo from '../cAPItan_Logo.jpg';
import React, { useState } from 'react';
import { Link } from 'react-router-dom';

export function Settings() {
 
    const [darkMode, setDarkMode] = useState(false);
    const [displayName, setDisplayName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [user_id, setUser_id] = useState('');
  
    const handleSave = (event) => {
      event.preventDefault();
      // save settings data here
    };

    const handleToggleChange = () => {
      fetch('http://host:5000/users/'+user_id, {
        method: 'GET',
        body: JSON.stringify({"password": password, "username": user_id, "football_club": email}),
        headers: { 'Content-Type': 'application/json' },
      })
      .then(response => response.json())
      .then(data => {
        if (data.message) {
            console.log(data.message)
            console.log("success User changed")
        }})
      };

    const handleClose = () => {
      // handle closing of overlay here
    };
  
    return (
        <div className="App">
      <div className="overlay-container">
        <div className="overlay">
          <div className="overlay-header">
            <h2>Settings</h2>
            <button className="close-btn" onClick={handleClose}>X</button>
          </div>
          <div className="overlay-content">
            <form onSubmit={handleSave}>
              <label>
                Display Name:
                <input type="text" value={displayName} onChange={(event) => setDisplayName(event.target.value)} />
              </label>
              <label>
                Email:
                <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
              </label>
              <label>
                Password:
                <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
              </label>
              <label>
                Weather
                <div className="switch-container">
              <input
                type="checkbox"
                id="dark-mode-toggle"
                checked={darkMode}
                onChange={handleToggleChange}
              />
              <label htmlFor="dark-mode-toggle" className="switch"></label>
            </div>

              </label>
              <div>
              <button type="submit">Save</button>
              </div>
              <Link to="/">
            <button type="button">Go back Home</button>
        </Link>
            </form>
          </div>
        </div>
      </div>
      </div>
    );
  }
  
  export default Settings;



   

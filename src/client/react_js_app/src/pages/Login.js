import React, { useState, useRef } from "react";
import "./Login.css";
import { Link } from 'react-router-dom';
import { getUserId, setUserId, setUserPreferences } from './User.js';


function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [user_id, setUser_id] = useState("");
  const [userPref, setUserPref] = useState([]);
  const userIdRef = useRef(null);

  function handleUsernameChange(event) {
    setUsername(event.target.value);
    setUser_id(event.target.value);
    userIdRef.current = event.target.value;
  }

  function getUserPref() {
    console.log("in get user for", user_id);
    fetch('http://localhost:5000/users/' + user_id, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        if (data) {
          console.log("We got user data");
          console.log(data);
          setUserPref([data.user_football_club, data.user_stocks, data.user_artists, data.user_spotify_link, data.user_calendar_link]);
        }
      })
      .catch(error => {
        console.error(error);
      });
  }

  function handlePasswordChange(event) {
    setPassword(event.target.value);
  }

  const handleSubmit = () => {
    fetch('http://localhost:5000/users/' + user_id, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        if (data) {
          console.log(data);
          if (data.password == password) {
            console.log("Success logged in");
            console.log(user_id);
            console.log("ref", userIdRef.current);
            setUserId(userIdRef.current);
            console.log("User_id", getUserId());
            getUserPref();
            console.log("lol");
            localStorage.setItem('user_id', userIdRef.current);
            window.location.href = '/';
          }
          else {
            console.log("Error");
          }
        }
      })
      .catch(error => {
        console.error(error);
      });
  }

  return (
    <div className="login-container">
      <div className="login-form">
        <h1>Log In</h1>
        <label>
          Email:
          <input type="username" value={username} onChange={handleUsernameChange} />
        </label>
        <br />
        <label>
          Password:
          <input type="password" value={password} onChange={handlePasswordChange} />
        </label>
        <br />
        <div className="container">
          <label>
            Not a Sailor yet? Get on board <Link to="/register">here</Link>.
          </label>
        </div>
        <button type="submit" onClick={handleSubmit}>Log In</button>
      </div>
    </div>
  );
}

export default LoginPage;


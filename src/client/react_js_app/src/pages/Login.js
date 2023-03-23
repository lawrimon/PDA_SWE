import React, { useState } from "react";
import "./Login.css";
import { Link } from 'react-router-dom';


function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [user_id, setUser_id] = useState("");



  function hanldeUsernameChange(event) {
    setUsername(event.target.value);
  }



  function handlePasswordChange(event) {
    setPassword(event.target.value);
  }

 
  function handleSubmit(event) {
    console.log(password)
    console.log(username)
    event.preventDefault();
    fetch('http://localhost:5000/users/'+user_id, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
      if (data.message) {
          console.log(data.message)
          if (data.message["password"] == password){
            console.log("Success logged in")
          }
          else{
            console.log("Error")
          }
      }})
  }

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h1>Log In</h1>
        <label>
          Email:
          <input type="username" value={username} onChange={hanldeUsernameChange} />
        </label>
        <br />
        <label>
          Password:
          <input type="password" value={password} onChange={handlePasswordChange} />
        </label>
        <br />
        <div className ="container">
        <label>
        Not a Sailor yet? Get on board <Link to="/register">here</Link>.
        </label>
        </div>
        <button type="submit">Log In</button>
        
      </form>
    </div>
  );
}

export default LoginPage;

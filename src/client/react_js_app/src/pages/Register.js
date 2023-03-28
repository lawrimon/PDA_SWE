import React, { useState } from "react";
import "./Register.css";
import { Link } from 'react-router-dom';
import sha256 from 'crypto-js/sha256';
import { setUserId } from '../components/User.js';


function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  let [username, setUsername] = useState("");
  const [userid, setUserid] = useState("");
 
  function hanldeUsernameChange(event) {
    setUsername(event.target.value);
    setUserid(event.target.value)
  }

  function handlePasswordChange(event) {
    setPassword(event.target.value);
  }

  function handleUserIDChange(){
    setUserid(username)
  }

  function handleSubmit() {
    console.log(password)
    console.log(username)
    console.log(userid)
    fetch('http://localhost:5000/users',{
      method: 'POST',
      body: JSON.stringify({"user_id":userid, "password":password, "username":username}),
      headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
      if (data) {
          console.log(data)
          if (data.status == "success, user added"){
            window.location.href = '/preferences';
            setUserId(userid)
            console.log(userid)
          }
      }})
  }


  return (
    <div className="register-container">
      <div className="register-form">
        <h1>Register</h1>
        <label>
          Username:
          <input type="username" value={username} onChange={hanldeUsernameChange} />
        </label>
        <br />
        <label>
          Password:
          <input type="password" value={password} onChange={handlePasswordChange} />
        </label>
        <br />
        <label>
            Repeat Password: 
            <input type="password" value={password} onChange={handlePasswordChange} />

        </label>
       
        <button type="submit" onClick={handleSubmit} >Next Step</button>
      </div>
    </div>
  );
}

export default RegisterPage;

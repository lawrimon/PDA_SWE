import React, { useState } from "react";
import "./Register.css";
import { Link } from 'react-router-dom';
import sha256 from 'crypto-js/sha256';


function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  let [username, setUsername] = useState("");
  let [userid, setUserid] = useState("");

  function hashString(str) {
 
    const hash = sha256(str);
    
    return hash.digest('hex');
  }
  
  function hanldeUsernameChange(event) {
    setUsername(event.target.value);
  }

  function handlePasswordChange(event) {
    setPassword(event.target.value);
  }

  function handleSubmit() {
    console.log(password)
    console.log(username)
    setUserid(hashString(username))
    console.log(userid)
    fetch('https://localhost:5000/users',{
      method: 'POST',
      body: JSON.stringify({"user_id":userid, "password":password, "username":username}),
      headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
      if (data.message) {
          console.log(data.message)
          if (data.message == "Success"){
            //Forward to 
            //window.location.href = '/registersuccess';
          }
      }})
  }

  function handleSubmit2(){
    console.log(password)
    console.log(username)
    setUserid(hashString(username))
    console.log(userid)
  }

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
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
       
        <button type="submit" onClick={handleSubmit2} >Next Step</button>
      </form>
    </div>
  );
}

export default RegisterPage;

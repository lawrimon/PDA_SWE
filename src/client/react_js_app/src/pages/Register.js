import React, { useState, useRef } from "react";
import "./Register.css";
import { setUserId } from '../components/User.js';


function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  let [username, setUsername] = useState("");
  const [userid, setUserid] = useState("");
  const userIdRef = useRef("");

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
            userIdRef.current = username
            localStorage.setItem('user_id', userIdRef.current);
            console.log(userIdRef.current, "is userid")
            setUserId(userid)
            console.log(userid)
            window.location.href = '/preferences';
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

import React, { useState, useRef } from "react";
import "./Register.css";
import { setUserId } from '../components/User.js';


function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");

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

  function handlePassword2Change(event) {
    setPassword2(event.target.value);
  }

  function handleUserIDChange(){
    setUserid(username)
  }
  

  function showErrorMessage(message) {
    const errorMessageElement = document.getElementById('error-message');
    errorMessageElement.innerText = message;
    errorMessageElement.style.color = 'red';
  }

  function handleSubmit() {
    console.log(password)
    console.log(username)
    console.log(userid)
    if(password == password2)
    {
      console.log("password success")
    
    fetch('http://localhost:5009/users',{
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
          else{
            console.log(data.error)
            showErrorMessage(data.error);

          }
      }})
  }
  else{
    showErrorMessage("Passwords do not match");

  }
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
            <input type="password" value={password2} onChange={handlePassword2Change} />

        </label>
        <div id="error-message"></div> {/* Add this div for displaying error message */}

        <button type="submit" onClick={handleSubmit} >Next Step</button>
      </div>
    </div>
  );
}

export default RegisterPage;

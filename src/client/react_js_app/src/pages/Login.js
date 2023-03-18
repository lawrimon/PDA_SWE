import React, { useState } from "react";
import "./Login.css";
import { Link } from 'react-router-dom';


function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleEmailChange(event) {
    setEmail(event.target.value);
  }

  function handlePasswordChange(event) {
    setPassword(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    // handle login request
  }

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h1>Log In</h1>
        <label>
          Email:
          <input type="email" value={email} onChange={handleEmailChange} />
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

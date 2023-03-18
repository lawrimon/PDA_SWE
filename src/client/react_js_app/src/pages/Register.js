import React, { useState } from "react";
import "./Register.css";
import { Link } from 'react-router-dom';


function RegisterPage() {
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
        <h1>Register</h1>
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
        <label>
            Repeat Password: 
            <input type="password" value={password} onChange={handlePasswordChange} />

        </label>
        <Link to="/preferences">
        <button type="submit">Next Step</button>
        </Link>
      </form>
    </div>
  );
}

export default RegisterPage;

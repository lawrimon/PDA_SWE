import React, { useEffect } from 'react';
import './RegisterSuccess.css'; // Import CSS file
import logo from '../cAPItan_Logo.jpg';

function RegistrationSuccess() {

  useEffect(() => {
    const timeout = setTimeout(() => {
      window.location.href = '/';
    }, 3000);

    return () => clearTimeout(timeout);
  }, []);

  return (
    <div>
      <div style={{ marginTop: "3%", right: "50%" }}>
        <img src={logo} alt="Logo" className="logo" style={{ display: "block", margin: "auto" }} />
      </div>
      <div className="registration-success">
        <h2>Registered Successfully!</h2>
        <p>Thank you for registering with our service.</p>
      </div>
    </div>
  );
}

export default RegistrationSuccess;

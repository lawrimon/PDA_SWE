import React, { useEffect } from 'react';
import logo from '../resources/cAPItan_Logo.jpg';

function NotFound() {

  useEffect(() => {
    const timeout = setTimeout(() => {
      window.location.href = '/';
    }, 5000);

    return () => clearTimeout(timeout);
  }, []);

  return (
     
    <div className='notfound' style={{ display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", height: "100vh"}}>
    <div style={{ textAlign: "center", maxWidth: "90%" }}>
      <img src={logo} alt="Logo" className="logo" />
      <h1>404 Page Not Found</h1>
      <p>Sorry, we could not find the page you are looking for.</p>
    </div>
  </div>
  
        );
      }
    

export default NotFound;

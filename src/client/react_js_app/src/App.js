import './App.css';
import logo from './cAPItan_Logo.jpg';

import React, { useState } from 'react';

function App() {
  const [inputValue, setInputValue] = useState('');

  const handleChange = (event) => {
    setInputValue(event.target.value);
  };

  return (
    <div className="App">
      <div style={{marginTop:"5%"}}>
      <img src={logo} alt="Logo" className="logo" />
      </div>
      <h1 style={{color:"white", paddingTop:"5%"}}>cAPItan</h1>
      <div className="search-container">
        <input type="text" value={inputValue} onChange={handleChange} placeholder="Search..." />
        <div>
        <button type="button">Search</button>
        </div>
       
      </div>
     
    </div>
  );
}

export default App;

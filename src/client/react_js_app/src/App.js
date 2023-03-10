import './App.css';
import logo from './cAPItan_Logo.jpg';

import React, { useState, useSyncExternalStore } from 'react';
import SpeechRecognition, {
  useSpeechRecognition
} from 'react-speech-recognition';

function App() {
  const [inputValue, setInputValue] = useState('');

  const handleChange = (event) => {
    setInputValue(event.target.value);
  };

  const { transcript, resetTranscript } = useSpeechRecognition({
    continuous: true
  });
 
  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    alert("This Browser doesn't support Speech-to-Text");
    return null;
  }

  //sending text to flask application
  const sendTranscript = () => {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ transcript: transcript })
    };
    fetch('/submit_transcript', requestOptions)
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));
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
      <div className="record-container">
        <div >
          <p></p>
          <textarea value={transcript} className="converted-speech">
          
          </textarea>
        </div>
        <div>
          <button onClick={SpeechRecognition.startListening}>Record</button>
          <button onClick={sendTranscript}>Submit</button>
        </div>
      </div>
      <div>
    </div>
    </div>
  );
}

export default App;

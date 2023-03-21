import './Home.css';
import logo from '../cAPItan_Logo.jpg';
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';

export function Home() {
  const [inputValue, setInputValue] = useState('');
  const [textToSpeak, setTextToSpeak] = useState('');
  const { SpeechSynthesisUtterance, speechSynthesis } = window;

  const handleChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleTextChange = (event) => {
    setTextToSpeak(event.target.value);
  };

  const handleSpeak = () => {
    if (speechSynthesis.speaking) {
      return; 
    }
    const utterance = new SpeechSynthesisUtterance(transcript);
    utterance.rate = 0.9;
    utterance.pitch = 1;
    speechSynthesis.speak(utterance);
  };
  
  const { transcript, resetTranscript } = useSpeechRecognition({
    continuous: true
  });
 
  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    alert("This Browser doesn't support Speech-to-Text");
    return null;
  }

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
        <div className="settings-button-container">
          <Link to="/settings">
            <button type="button" className="settings-button">&#x2699;</button>
          </Link>
        </div>
      </div>
      <div className="record-container">
        <div >
          <textarea value={transcript} onChange={handleTextChange} className="converted-speech"></textarea>
        </div>
        <div>
          <button onClick={SpeechRecognition.startListening}>Record</button>
          <button onClick={handleSpeak}>Speak</button>
          <button onClick={sendTranscript}>Submit</button>
        </div>
      </div>
    </div>
  );
}

export default Home;

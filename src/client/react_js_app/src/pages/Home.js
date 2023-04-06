import './Home.css';
import logo from '../resources/cAPItan_Logo.jpg';
import React, { useState, useEffect, useRef}  from 'react';

import { Link } from 'react-router-dom';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import NotificationPopup from './Notification';
import { getUserId,setUserId,user_id } from '../components/User.js';


export function Home() {
  const useridRef = useRef(null);

  const [text, setText] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [textToSpeak, setTextToSpeak] = useState('');
  const { SpeechSynthesisUtterance, speechSynthesis } = window;
  const [message, setMessage] = useState('');
  let userid = null;

  useEffect(() => {
    // Call your function here
    // Retrieve the user ID from local storage
    const storedUserId = localStorage.getItem('user_id');
    
    // Set the value of useridRef.current to the retrieved user ID, if it exists
    if (storedUserId) {
      useridRef.current = storedUserId;
      console.log("Userid", useridRef.current);
      setUserId(useridRef.current)
    }
  }, [getUserId()]);

  const toggleModal = () => setShowModal(!showModal);

  const Logout = () => {
    console.log("Logging out!");
    const storedUserId = ""
    localStorage.clear()
    window.location.href = '/login';

  };

  const handleButtonClick = () => {
    setShowPopup(true);
  };

  const handleClosePopup = () => {
    setShowPopup(false);
  };

  const handleChange = (event) => {
    setText(event.target.value);
  };

  const handleSubmit = () => {
    fetch('http://141.31.86.15:8000//postText', {
      method: 'POST',
      body: JSON.stringify({ "text": text }),
      headers: { 'Content-Type': 'application/json' },
    })
      .then(response => response.json())
      .then(data => {
        if (data.message) {
          console.log(data.message)
        }
      })
      .catch(error => {
        console.error(error);
      });
  };
  

  //STT and TTS
  const handleTextChange = (event) => {
    setTextToSpeak(event.target.value);
  };

  async function handleSpeak() {
    if (speechSynthesis.speaking) {
      return; 
    }
    console.log("in handlespeak");
  
    // Wait for sendToFrontend to complete and return a value
    const answer = await sendToFrontend();
    console.log("answer:", answer);
    // Wait for setMessage to complete and then call SpeechSynthesisUtterance
    await new Promise(resolve => setTimeout(resolve, 1000)); // wait for 1 second
    return answer  
  };

  async function say_scuttlebutt(){
    const text = await handleSpeak();
    console.log(text, "is the message then")
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    var voices = window.speechSynthesis.getVoices();
    utterance.voice = voices[15];
    utterance.lang = 'en-US'; 
    speechSynthesis.speak(utterance);


  }
  
  

  async function say_scuttlebutt2() {
    let val = ""
    try {
      const text = await handleSpeak();
      console.log(text, "is the message then");
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1;
      utterance.pitch = 1;
      var voices = window.speechSynthesis.getVoices();
      utterance.voice = voices[15];
      utterance.lang = 'en-US';
  
      await new Promise((resolve, reject) => {
        utterance.onend = resolve;
        utterance.onerror = reject;
        speechSynthesis.speak(utterance);
      });
  
      console.log("After speak");
  
      const recognition = new window.webkitSpeechRecognition();
      recognition.lang = 'en-US';
      recognition.start();
  
      console.log("Listening...");
  
      // Wait for 3 seconds before stopping the recognition
      setTimeout(() => {
        recognition.stop();
        console.log("Stopped listening");
        console.log(transcript," is the transcript");

        recognition.onresult = function(event) {
          const transcript2 = event.results[0][0].transcript;
          console.log(transcript2," is the transcript");
          if (transcript2 !== ""){
            recognition.onend = function() {
              console.log('Speech recognition service disconnected');
              console.log(transcript2," is the transcript right before");
    
              say_additional(transcript2);
    
            };
          }
        };  
      }, 5000);
  
    } catch (error) {
      console.error(error);
    }
  }
  
  
  
  
  
  
  
    
  

  function timeout(delay) {
    return new Promise( res => setTimeout(res, delay) );
}

  const { transcript, resetTranscript } = useSpeechRecognition({
    continuous: true,
    lang: 'en-US'
  });

  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    alert("This Browser doesn't support Speech-to-Text");
    return null;
  }


  async function sendTranscript(trans2) {
    let text = "";
    console.log("transcript in sendTranscript",trans2)
   
    if (trans2.toLowerCase() === "no") {
      setMessage("Alright, have a nice day!");
      return null;
    } else if (trans2.toLowerCase() === "yes") {
      console.log("provide more information");
      try {
        const response = await fetch('http://127.0.0.1:5008/scuttlebutt/additional');
        const data = await response.json();
        text = data[0].toString() + data[1].toString();
        await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for 2 seconds
        setMessage(text);
        console.log(message, "messsssagio");
        return text;
      } catch (error) {
        console.error(error);
      }
    } else {
      console.log("User did not request more information.");
    }
  }
  
  async function say_additional(trans2) {
    const text = await sendTranscript(trans2);
    console.log(text, "is the message then")
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    var voices = window.speechSynthesis.getVoices();
    utterance.voice = voices[15];
    utterance.lang = 'en-US'; 
    speechSynthesis.speak(utterance);
  }
  
  
  

  async function sendToFrontend () {
    const response = await fetch('http://127.0.0.1:5008/scuttlebutt')
    const data = await response.json();
    console.log("this data",data.toString())
    if(data){
      setMessage(data)
      return data
    }
  };

  return (
    <div className="App">
      <div style={{ marginTop: "3%" }}>
        <img src={logo} alt="Logo" className="logo" />
      </div>
      <h1 style={{ color: "white", paddingTop: "1%" }}>cAPItan</h1>
      <div className="search-container">
        <input type="text" value={text} onChange={handleChange} onClick={() => setShowPopup(false)} 
        placeholder="Search..." />
        <div>
          <button type="button" onClick={handleSubmit}>Search</button>
        </div>
        <div className="settings-button-container">
          <div>
          <button type="button"onClick={handleButtonClick}  className="settings-button">✉</button>
                </div>
      
          <Link to="/settings">
            <button type="button" className="settings-button">&#x2699;</button>
          </Link>
          <div className="">
            <div className="notification-icon">

            <button type="button" onClick={Logout} className="settings-button">&#10149;</button>           
            </div>  
            </div>
            <div className="">
            <div className="notification-icon">

            <button type="button" onClick={say_scuttlebutt2} className="settings-button">&#x2603;</button>           
            </div>  
            </div>
          </div>
          </div>
                  
         
          {showPopup && (
        <div className="sidebar">
          <div className="sidebar-header">
            <h2>Notifications</h2>
            <button className="close-button" onClick={handleClosePopup}>
              X
            </button>
          </div>
          <div className="sidebar-content">
            <div className="notification">
              <div className="notification-icon">
                <i className="fas fa-user-circle"></i>
              </div>
              <div className="notification-text">
                <p>
                  You have a new follower on Twitter! Click here to view your
                  profile.
                </p>
                <small>2 mins ago</small>
              </div>
            </div>
            <div className="notification">
              <div className="notification-icon">
                <i className="fas fa-heart"></i>
              </div>
              <div className="notification-text">
                <p>
                  Someone liked your photo on Instagram! Click here to view
                  their profile.
                </p>
                <small>5 mins ago</small>
              </div>
            </div>
            <div className="notification">
              <div className="notification-icon">
                <i className="fas fa-comment"></i>
              </div>
              <div className="notification-text">
                <p>
                  You have a new comment on your blog post! Click here to view
                  it.
                </p>
                <small>10 mins ago</small>
                </div>

            </div>
              </div>

            </div>
          )}
          <div className="record-container">
        <div >
          <textarea value={transcript} onChange={handleTextChange} className="converted-speech"></textarea>
          <textarea value={message} onChange={handleTextChange} className="converted-speech"></textarea>
        </div>
        <div>
          <button onClick={SpeechRecognition.startListening}>Record</button>
          <button onClick={SpeechRecognition.stopListening}>Stop</button>
          <button onClick={say_scuttlebutt2}>Speak</button>
          <button onClick={say_additional}>Submit</button>
        </div>
      </div>
      </div>
  );  
}

export default Home;
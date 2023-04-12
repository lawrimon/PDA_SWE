import './Home.css';
import logo from '../resources/cAPItan_Logo.jpg';
import React, { useState, useEffect, useRef }  from 'react';

import { Link } from 'react-router-dom';
import NotificationPopup from './Notification';
import { getUserId, setUserId, user_id } from '../components/User.js';
import { useSpeech } from '../components/SpeechFunctions';

export function Home() {
  const useridRef = useRef(null);

  const [text, setText] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [message, setMessage] = useState('');
  let userid = null;
  const { textToSpeak, setTextToSpeak, speak, transcript, resetTranscript } = useSpeech();

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


  async function handleSpeakNew(usecase) {
    let answer;
    console.log("usecase", usecase)
    if (speechSynthesis.speaking) {
      return; 
    }
    console.log("in handlespeak");

    if (usecase === "shoreleave"){
      const answer = await getShoreleave();
      console.log("answer:", answer);
      await new Promise(resolve => setTimeout(resolve, 1000)); // wait for 1 second
      return answer
    }
    else if (usecase ==="scuttlebutt"){
      const answer = await sendToFrontend();
      console.log("answer:", answer);
      await new Promise(resolve => setTimeout(resolve, 1000)); // wait for 1 second
      return answer
    }

    else if (usecase ==="lookout"){
      const answer = await getLooktout();
      console.log("answer:", answer);
      await new Promise(resolve => setTimeout(resolve, 1000)); // wait for 1 second
      return answer
    }
    // Wait for sendToFrontend to complete and return a value
   
    // Wait for setMessage to complete and then call SpeechSynthesisUtterance
  };
  
  async function say_scuttlebutt() {
    let val = ""
    try {
      const text = await handleSpeakNew("scuttlebutt");
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
    const response = await fetch('http://127.0.0.1:5008/scuttlebutt'+ useridRef.current)
    const data = await response.json();
    console.log("this data",data.toString())
    if(data){
      setMessage(data)
      return data
    }
  };

  async function getShoreleave(){
    const response = await fetch('http://127.0.0.1:5013/shoreleave')
    const data = await response.json();
    console.log("this data",data.toString())
    if(data){
      setMessage(data)
      return data
    }
  }

  async function getLooktout(){
    const response = await fetch('http://127.0.0.1:5016/lookout?user='+ user_id)
    const data = await response.json();
    console.log("this data",data.toString())
    if(data){
      setMessage(data)
      return data
    }
  }

  async function say_lookout() {
    let val = ""
    try {
      const text = await handleSpeakNew("lookout");
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
        console.log(Home.transcript," is the transcript");

        recognition.onresult = function(event) {
          const transcript2 = event.results[0][0].transcript;
          console.log(transcript2," is the transcript");
          if (transcript2 !== ""){
            recognition.onend = function() {
              console.log('Speech recognition service disconnected');
              console.log(transcript2," is the transcript right before");
    
              //say_additional(transcript2);
    
            };
          }
        };  
      }, 5000);
  
    } catch (error) {
      console.error(error);
    }
  }

   async function say_shoreleave() {
    let val = ""
    try {
      const text = await handleSpeakNew("shoreleave");
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
        console.log(Home.transcript," is the transcript");

        recognition.onresult = function(event) {
          const transcript2 = event.results[0][0].transcript;
          console.log(transcript2," is the transcript");
          if (transcript2 !== ""){
            recognition.onend = function() {
              console.log('Speech recognition service disconnected');
              console.log(transcript2," is the transcript right before");
    
              //say_additional(transcript2);
    
            };
          }
        };  
      }, 5000);
  
    } catch (error) {
      console.error(error);
    }
  }
  



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

            <button type="button" style={{backgroundColor: "gray"}} onClick={say_scuttlebutt} className="settings-button">&#x2603;</button>           
            </div>  
            </div>
            <div className="">
            <div className="notification-icon">

            <button type="button" style={{backgroundColor: "orange"}} onClick={say_shoreleave} className="settings-button">&#128062;</button>           
            </div>  
            </div>
            <div className="">
            <div className="notification-icon" >

            <button type="button" style={{backgroundColor: "lightgreen"}} onClick={say_lookout} className="settings-button">&#x2656;</button>           
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
          <button onClick={console.log("lol")}>Record</button>
          <button onClick={console.log("lol")}>Stop</button>
          <button onClick={say_scuttlebutt}>Speak</button>
          <button onClick={say_additional}>Submit</button>
        </div>
      </div>
      </div>
  );  
 
} 

export default Home;

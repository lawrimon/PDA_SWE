import './Home.css';
import logo from '../resources/cAPItan_Logo.jpg';
import React, { useState, useEffect, useRef }  from 'react';

import { Link } from 'react-router-dom';
import NotificationPopup from './Notification';
import { getUserId, setUserId, user_id } from '../components/User.js';
import { useSpeech } from '../components/SpeechFunctions';
import io from 'socket.io-client';

export function Home() {
  const useridRef = useRef(null);

  // Rabbit
  const [queueName, setQueueName] = useState(null);
  const socketRef = useRef(null);
  const [message, setMessage] = useState("");
  const ENDPOINT = 'http://localhost:5010/';

  const [text, setText] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [showModal, setShowModal] = useState(false);
  
  let userid = null;
  const { textToSpeak, setTextToSpeak, speak, transcript, resetTranscript } = useSpeech();

  useEffect(() => {
    // Call your function here
    // Retrieve the user ID from local storage
    const storedUserId = localStorage.getItem('user_id');

    // Set the value of useridRef.current to the retrieved user ID, if it exists
    if (storedUserId || storedUserId.length()) {
      useridRef.current = storedUserId;
      console.log("Userid: ", useridRef.current);
      setUserId(useridRef.current)
      setQueueName(storedUserId)

      // connect to websocket server on mount
      handleConnect()
    }
    // invalid login user
    else{
      // disconnect current socket
      if (socketRef.current) {
        console.log(`Disconnected from ${queueName} room Print4`);
        socketRef.current.disconnect();
        socketRef.current = null;
      }
      Logout()
      
    }

    // disconnect socket on unmount
    return () => {
      if (socketRef.current) {
        console.log(`Disconnected from ${queueName} room Print4`);
        socketRef.current.disconnect();
        socketRef.current = null;
      }
    };
  }, [getUserId()]);

   // Function to connect to the socket server
   const handleConnect = () => {
    // Disconnect from previous socket room
    if (socketRef.current) {
      console.log(`Disconnected from ${queueName} room Print1`);
      socketRef.current.disconnect();
      socketRef.current = null;
    }

    // Connect to the socket server and emit 'start' event with user_id
    const socket = io(ENDPOINT, {});
    socketRef.current = socket;

    socket.emit('start', { user_id: queueName });
    console.log(`Connected to ${queueName} room Print2`);

    // Listen for 'message' event and update messages state
    socket.on('message', (message) => {
      
    });

    // Listen for 'disconnect' event and log
    socket.on('disconnect', () => {
      console.log(`Disconnected from server Print3`);
    });

    // Return cleanup function to disconnect from socket
    return () => {
      socket.disconnect();
    };
  };

  // Function to acknowledge a message
  const handleAcknowledge = (deliveryTag) => {

    try {
    // Check if the delivery tag is a valid integer
    if (deliveryTag) {
      // Acknowledge Message by emitting 'ack' event with delivery_tag
      socketRef.current.emit('ack', { delivery_tag: deliveryTag });

      // Remove acknowledged message from messages array
      console.log("Message Acknowledged")
      setMessage(null);
    } else {
      console.error('Invalid delivery tag:', deliveryTag);
    }
    } catch (error) {
      console.error(error);
    }
  };

  // Function to handle incoming messages
  const handleMessages = (message) => {
    console.log('Message received');
    // Add message to messages state
    setMessage(message);
  };


  const Logout = () => {
    console.log("Logging out!");
    setUserId("")
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
  
  async function say_use_case(use_case) {

    var text  = null;
    // get the right data to spreak
    if (use_case == "scuttlebutt"){
       text = await getScuttlebutt();
    }
    else if (use_case == "lookout"){
       text = await getLooktout();
    }
    else if (use_case == "racktime"){
       text = await getRackTime();
    }
    else if (use_case == "shoreleave"){
       text = await getShoreleave();
    }
      console.log( "Starts speaking...");
      let i = 0;
      
      for (const [key, value] of Object.entries(text)) {
        console.log("Part", i)
        console.log("Text:", value)
        speechSynthesis.cancel()
        var utterance = new SpeechSynthesisUtterance(value);
        utterance.rate = 1;
        utterance.pitch = 1;
        var voices = window.speechSynthesis.getVoices();
        utterance.voice = voices[15];
        utterance.lang = 'en-US';
      
        await new Promise((resolve, reject) => {
          utterance.addEventListener('start', function () {
            setMessage(value)
            console.log("speaking")
          })
          utterance.addEventListener("error", (event) => {
            reject();
          });
       
          utterance.addEventListener('end', function () {
            resolve();
          })
          
          speechSynthesis.speak(utterance);
        });
        i += 1;
      }
      console.log("Finished Speaking");
  
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
  
  async function getScuttlebutt () {
    const response = await fetch('http://127.0.0.1:5008/scuttlebutt?user='+ useridRef.current)
    const data = response.json();
    console.log("this data", data)
    if(data){
      setMessage(data)
      return data
    }
  };

  async function getShoreleave(){
    const response = await fetch('http://127.0.0.1:5013/shoreleave')
    const data = await response.json();
    console.log("this data",data)
    if(data){
      setMessage(data)
      return data
    }
  }

  async function getLooktout(){
    const response = await fetch('http://127.0.0.1:5016/lookout?user='+ user_id)
    const data = await response.json();
    console.log("this data",data)
    if(data){
      setMessage(data)
      return data
    }
  }

  async function getRackTime(){
    const response = await fetch('http://127.0.0.1:5019/racktime?user='+ user_id)
    const data = await response.json();
    console.log("this data",data)
    if(data){
      setMessage(data)
      return data
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

            <button type="button" style={{backgroundColor: "gray"}} onClick={() => say_use_case("scuttlebutt")} className="settings-button">&#x2603;</button>           
            </div>  
            </div>
            <div className="">
            <div className="notification-icon">

            <button type="button" style={{backgroundColor: "orange"}} onClick={() => say_use_case("lookout")} className="settings-button">&#128062;</button>           
            </div>  
            </div>
            <div className="">
            <div className="notification-icon" >

            <button type="button" style={{backgroundColor: "lightgreen"}} onClick={() => say_use_case("shoreleave")} className="settings-button">&#x2656;</button>           
            </div>  
            </div>
            <div className="">
            <div className="notification-icon" >

            <button type="button" style={{backgroundColor: "lightbrown"}} onClick={() => say_use_case("racktime")} className="settings-button">&#9742;</button>           
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
          <button onClick={() => say_use_case("scuttlebutt")}>Speak</button>
          <button onClick={say_additional}>Submit</button>
        </div>
      </div>
      </div>
  );  
 
} 

export default Home;

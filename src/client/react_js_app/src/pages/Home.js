import './Home.css';
import './NotificationCenter.css'
import logo from '../resources/cAPItan_Logo.jpg';
import logo2 from '../resources/spongie2.gif';
import React, { useState, useEffect, useRef } from 'react';

import { Link } from 'react-router-dom';
import { getUserId, setUserId, user_id } from '../components/User.js';
import io from 'socket.io-client';




export function Home() {
  var originalColor;

  const useridRef = useRef(null);
  const [notifications, setNotifications] = useState([]);

  const [logoSrc, setLogoSrc] = useState(logo);

  // Rabbit
  const [queueName, setQueueName] = useState(null);
  const socketRef = useRef(null);
  const [message, setMessage] = useState("");
  const ENDPOINT = 'http://localhost:5010/';
  const deliveryTagRef = useRef("");
  var connected = false;

  const [text, setText] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [transcript, setTranscript] = useState('');

  // function to update delivery tag
  function updateDeliveryTag(tag) {
    deliveryTagRef.current = tag;
  }

  var next_message = true;

  const NotificationColors = {
    Scuttlebutt: "gray",
    Shoreleave: "lightpink",
    Lookout: "lightgreen",
    Racktime: "brown"
  };

  const addNotification = (message, color) => {
    const newNotifications = [...notifications, { message, color }];
    setNotifications(newNotifications);
  };

  const removeNotification = (index) => {
    const newNotifications = [...notifications];
    newNotifications.splice(index, 1);
    setNotifications(newNotifications);
  };

  useEffect(() => {
    // Call your function here
    // Retrieve the user ID from local storage
    const storedUserId = localStorage.getItem('user_id');

    // Set the value of useridRef.current to the retrieved user ID, if it exists
    if (storedUserId) {
      useridRef.current = storedUserId;
      console.log("Userid: ", useridRef.current);
      setUserId(useridRef.current)
      setQueueName(storedUserId)

      // connect to websocket server on mount
      // handleConnect()
    }

    // invalid login user
    else {
      // disconnect current socket
      handleDisconnect()
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

  function buttonConnect(){
    if (connected){
      connected = false
      handleConnect();
    }
    else{
      connected = true
      handleDisconnect();
    }
  }

  // Function to connect to the socket server
  const handleConnect = () => {
    // Disconnect from previous socket room
    handleDisconnect()

    // Connect to the socket server and emit 'start' event with user_id
    const socket = io(ENDPOINT, {});
    socketRef.current = socket;

    socket.emit('start', { user_id: queueName });
    console.log(`Connected to ${queueName} room Print2`);

    // Listen for 'message' event and update messages state
    socket.on('message', (message) => {
      handleMessages(message)
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

  function handleDisconnect(){

    // disconnect from websocket server
    if (socketRef.current) {
      console.log(`Disconnected from ${queueName} room Print1`);
      socketRef.current.disconnect();
      socketRef.current = null;
    }


  }

  // Function to acknowledge a message
  const handleAcknowledge = (deliveryTag) => {

    try {
      // Check if the delivery tag is a valid integer
      if (deliveryTag) {
        // Acknowledge Message by emitting 'ack' event with delivery_tag
        socketRef.current.emit('ack', { delivery_tag: deliveryTag });

        // Remove acknowledged message from messages array
        console.log("Message Acknowledged")
        setMessage("");
      } else {
        console.error('Invalid delivery tag:', deliveryTag);
      }
    } catch (error) {
      console.error(error);
    }
  };

  // Function to handle incoming messages
  const handleMessages = (message) => {
    console.log('Message received', message);
    // Add message to messages state
    updateDeliveryTag(message.delivery_tag)
    console.log("Delivery Tag", deliveryTagRef.current)
    say_use_case("rabbit", message.message)
      .then(() => {
        if (next_message) {
          handleAcknowledge(deliveryTagRef.current)
        }
      })
      .catch((error) => console.error("Error occurred:", error));
  };


  const handleLogo = (insertlogo) => {
    setLogoSrc(insertlogo);
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
    addNotification("Error Notification", NotificationColors.Lookout)
    };

  function changeColor(div) {
    var button = document.getElementById(div);
    if (!button.classList.contains('red')) {
      originalColor = button.style.backgroundColor;
      button.style.backgroundColor = 'red';
    }
  }

  function setColor(div) {
    console.log("in Setcolor")
    console.log(div)
    var button = document.getElementById(div);
      button.style.backgroundColor = originalColor;
    
  }



  async function listenForSpeech() {

    const recognition = new window.webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onresult = event => {
      let interimTranscript = '';
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        let transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript + ' ';
        } else {
          interimTranscript += transcript;
        }
      }

      setTranscript(finalTranscript.trim());
    };

    recognition.onerror = event => {
      console.error('Speech recognition error:', event);
    };

    return new Promise((resolve, reject) => {
      recognition.start();

      let timeoutId = setTimeout(() => {
        recognition.stop();
        resolve(transcript.trim());
      }, 5000);

      recognition.onend = () => {
        clearTimeout(timeoutId);
        resolve(transcript.trim());
      };

      recognition.onerror = () => {
        clearTimeout(timeoutId);
        reject('Speech recognition error');
      };
    });
  }

  async function say_use_case(use_case, speaking_text = "") {
    var text = null;
    // get the right data to spreak
    if (use_case === "scuttlebutt") {
      text = await getScuttlebutt();
    } else if (use_case === "lookout") {
      text = await getLooktout();
    } else if (use_case === "racktime") {
      text = await getRackTime();
    } else if (use_case === "shoreleave") {
      text = await getShoreleave();
    } else if (use_case === "rabbit") {
      text = speaking_text;
    } else {
      // handle the case where use_case is not recognized
      return;
    }

    console.log("Starts speaking...");
    let i = 0;
    const keysInOrder = Object.keys(text);
    console.log(keysInOrder)
    for (const key of keysInOrder) {
      const value = text[key];
      console.log("Part", i)
      console.log("Text:", value)
      await say_text(value)
      i += 1;
    }

    console.log("Finished Speaking");
    console.log("Listening...");

    try {
      const tmp_transcript = await listenForSpeech();
      console.log("Transcript:", tmp_transcript);
      await handleTranscript(tmp_transcript);
    } catch (error) {
      console.error("Speech recognition error:", error);
    }

    handleAcknowledge(deliveryTagRef.current)
  }

  async function say_text(text) {

    speechSynthesis.cancel()
    const voices = speechSynthesis.getVoices();
    var utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = voices.find((voice) => voice.name === 'Google UK English Female');
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.lang = 'en-US';

    await new Promise((resolve, reject) => {
      utterance.addEventListener('start', function () {
        setMessage(text)
        console.log("speaking")
      })
      utterance.addEventListener("error", (event) => {
        console.log("Error: rejected");
        reject();
      });

      utterance.addEventListener('end', function () {
        resolve();
      })

      utterance.onend = function (event) {
        console.log('Speech finished after ' + event.elapsedTime + ' seconds.');
        // Do something here after the speech has finished
        resolve();
      };
      speechSynthesis.cancel()
      speechSynthesis.speak(utterance);
    });
  }

  async function handleTranscript(transcript) {
    if (transcript.toLowerCase() === "no") {
      console.log("Alright, have a nice day!");
    } else if (transcript.toLowerCase() === "yes.") {
      console.log("provide more information");
      try {
        const response = await fetch('http://127.0.0.1:5008/scuttlebutt/additional');
        const data = await response.json();
        const text = data[0].toString() + data[1].toString();
        console.log("Message:", text);
        await say_text(text)
      } catch (error) {
        console.error(error);
        console.log("Sorry, there was an error getting more information.");
      }
    } else {
      console.log("User did not request more information.");
    }
  }


  async function getScuttlebutt() {
    const response = await fetch('http://127.0.0.1:5008/scuttlebutt?user=' + useridRef.current)
    const data = await response.json();
    console.log("this data", data)
    if (data) {
      setMessage(data)
      return data
    }
  };

  async function getShoreleave() {

    const response = await fetch('http://127.0.0.1:5013/shoreleave?user=' + user_id)
    const data = await response.json();
    console.log("this data", data)

    if (data) {
      setMessage(data)
      return data
    }
  }

  async function getLooktout() {
    const response = await fetch('http://127.0.0.1:5016/lookout?user=' + user_id)
    const data = await response.json();

    console.log("this data", data)
    if (data) {
      setMessage(data)
      return data
    }
  }


  async function getRackTime() {
    const response = await fetch('http://127.0.0.1:5019/racktime?user=' + user_id)
    const data = await response.json();
    console.log("this data", data)
    if (data) {
      setMessage(data)
      return data
    }
  }


  return (
    <div className="App">
      <div style={{ marginTop: "3%" }}>
        <img src={logoSrc} style={{ width: "12%" }} alt="Logo" className="logo" />
      </div>
      <h1 style={{ color: "white", paddingTop: "1%" }}>cAPItan</h1>
      <div className="search-container">
        <input type="text" value={text} onChange={handleChange} onClick={() => setShowPopup(false)}
          placeholder="Search..." />

        <button type="button" onClick={() => handleSubmit()}>Search</button>
        <div className="settings-button-container">

          <Link to="/settings">
            <button type="button" className="settings-button">&#x2699;</button>
          </Link>
          <button type="button" id="lookout" onClick={() => buttonConnect()}  className="lookout">&#128062;</button>

          <button type="button" id="scuttlebutt" onClick={() => say_use_case("scuttlebutt")} className="scuttlebutt">&#x2603;</button>

          <button type="button" id="shoreleave" onClick={() => say_use_case("shoreleave")} className="shoreleave">&#128062;</button>

          <button type="button" id="lookout" onClick={() => say_use_case("lookout")}  className="lookout">&#x2656;</button>
          
          <button type="button" style={{ backgroundColor: "lightbrown" }} onClick={() => say_use_case("racktime")} className="settings-button">&#9742;</button>

          <button type="button" id="Logout" onClick={() => Logout()} className="settings-button">&#10149;</button>

        </div>
      </div>

      <div className="nots">
        <div className="notification-centerNew">
          <div className="notification-containerNew">
            {notifications.map((notification, index) => (
              <div key={index} className={`notificationNew ${notification.color}`}>
                <div className={`notification-iconNew`} style={{ backgroundColor: notification.color }}></div>
                <div className="notification-textNew">{notification.message}</div>
                <button onClick={() => removeNotification(index)} className="notification-closeNew">×</button>
              </div>
            ))}
          </div>
        </div>
      </div>

    </div>


  );

}

export default Home;

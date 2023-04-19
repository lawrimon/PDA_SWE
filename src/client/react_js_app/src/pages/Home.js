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
  const [message, setMessage] = useState(""); //  do we need this ?
  const deliveryTagRef = useRef("");
  const [text, setText] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [expanded, setExpanded] = useState(false);

  const ENDPOINT = 'http://localhost:5010/';
  var globalTranscript = ""
  var next_message = false;
  var connected = false;
  const NotificationColors = {
    scuttlebutt: "gray",
    shoreleave: "lightpink",
    lookout: "lightgreen",
    racktime: "brown"
  };

  // set to true to avoid long TTS
  var debug = false

  //intent returned by dialogflow
  const [intent, setIntent] = useState(null);

  // function to update delivery tag
  function updateDeliveryTag(tag) {
    deliveryTagRef.current = tag;
  }

  const addNotification = (message, color) => {
    setNotifications(notifications => [...notifications, { message, color }]);
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

  async function buttonConnect(){
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

      // acknowledge message before disconnecting
      if(deliveryTagRef.current){
        handleAcknowledge(deliveryTagRef.current)
      }
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
        deliveryTagRef.current = null
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
        if (deliveryTagRef.current && next_message) {
          handleAcknowledge(deliveryTagRef.current)
        }
      })
      .catch((error) => console.error("Error occurred:", error));
  };


  // asking user for additional information
  async function handleAdditional(){
    const question_text = "Thank you for listening. Do you want any additional information? "
    await say_text(question_text)
  }


  const handleLogo = (insertlogo) => {
    setLogoSrc(insertlogo);
  };

  const Logout = () => {
    console.log("Logging out!");
    setUserId("")
    localStorage.clear()
    window.location.href = '/login';
  };

  const handleChange = (event) => {
    setText(event.target.value);
  };

  const handleSubmit = () => {
    const url = `http://localhost:50021/dialogflow/get_intent?transcript=${text}`;
    fetch(url)
      .then(response => response.json())
      .then(data => {
        console.log(data.intent);
        setIntent(data.intent);
      })
      .catch(error => console.error(error));
  }
  
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

      console.log("event",event)

      for (let i = event.resultIndex; i < event.results.length; i++) {
        let transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript + ' ';
        } else {
          interimTranscript += transcript;
        }
      }

      globalTranscript = finalTranscript.trim();
    };

    recognition.onerror = event => {
      console.error('Speech recognition error:', event);
    };

    return new Promise((resolve, reject) => {
      recognition.start();

      let timeoutId = setTimeout(() => {
        recognition.stop();
        resolve(globalTranscript.trim());
      }, 5000);

      recognition.onend = () => {
        clearTimeout(timeoutId);
        resolve(globalTranscript.trim());
      };

      recognition.onerror = () => {
        clearTimeout(timeoutId);
        reject('Speech recognition error');
      };
    });
  }
  
  const [isASelected, setIsASelected] = useState(false);
  const [buttonColor, setButtonColor] = useState("transparent");
  const recognitionRef = useRef(null);
  const transcriptRef = useRef("");

  const startListening = () => {
    const recognition = new window.webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognitionRef.current = recognition;

    recognition.onresult = (event) => {
      let interimTranscript = "";
      let finalTranscript = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        } else {
          interimTranscript += transcript;
        }
      }
      console.log(interimTranscript);


      transcriptRef.current = interimTranscript + finalTranscript;
    };

    recognition.start();
    console.log("listening started");
    

  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      console.log("listening stopped");
      console.log("final transcript:", transcriptRef.current);
      setText(transcriptRef.current)
      transcriptRef.current = "";
    }
  };

  const handleClick = () => {
    if (isASelected) {
      setButtonColor("transparent");
      console.log("B");
      stopListening();
    } else {
      setButtonColor("#F62817");
      console.log("A");
      startListening();
    }
    setIsASelected(!isASelected);
  };


  // function that returns a Promise that resolves after a specified delay
  function delay(delayInMilliseconds) {
    return new Promise(resolve => setTimeout(resolve, delayInMilliseconds));
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
    console.log(use_case, "usecase")
    console.log(text)

    let name = text._name
    delete text._name
    const keysInOrder = Object.keys(text);
    
    if (debug){
      let textToSay = "this is a little example text"
      let use_case  = "scuttlebutt"
      addNotification(textToSay, NotificationColors[use_case])
      await say_text(textToSay)
    }
    else {
    let i = 0;
    handleLogo(logo2)
    changeColor(name)
    for (const key of keysInOrder) {
      const value = text[key];
      addNotification(value, NotificationColors[name])
      await say_text(value)
      i += 1;
      }
    }

    // pause for 1 seconds using Promises
    delay(1000).then(() => {});
    if (name === "scuttlebutt"){
      await handleAdditional()
      console.log("Finished Speaking");
      handleLogo(logo)
      setColor(name)
      try {
        console.log("Listening...");
        const tmp_transcript = await listenForSpeech();
        console.log("Transcript:", tmp_transcript);
        await handleTranscript(tmp_transcript);
        
        // reset transcript
        globalTranscript = ""
      } catch (error) {
        console.error("Speech recognition error:", error);
      }
    }

    // acknowledge message so that next message can be consumed
    if (deliveryTagRef.current){
      handleAcknowledge(deliveryTagRef.current)
    }
  }

  async function say_text(text) {

    speechSynthesis.cancel()
    var utterance = new SpeechSynthesisUtterance(text);
    // utterance.voice = voices.find((voice) => voice.name === 'Google UK English Female');
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
      // check if user said something -> intend recognition here
    } else if (transcript.toLowerCase().length > 2) {
      console.log("provide more information");
      try {
        const response = await fetch('http://127.0.0.1:5008/scuttlebutt/additional');
        const data = await response.json();
        if (response.status != 200){
          console.log("Error in response from Scuttlebut")
        }
        else{
        let addtional_text = ""
        for (const part of data["text"]) {
          addtional_text += part.toString()
        }

        if (debug){
          const slice1 = addtional_text.slice(0,10)
          console.log("Additional Message:", slice1);
          await say_text(slice1)
        }
        else{
          const slice1 = addtional_text.slice(0,10)
          console.log("Additional Message:", slice1);
          await say_text(addtional_text)
        }
        
        }
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
        {intent && <p>Intent: {intent}</p>}
        <button type="button" class="ios-button" onClick={() => handleSubmit()}>&#127929;</button>

        <button class="ios-button"  style={{ backgroundColor: buttonColor,  }} onClick={() => handleClick()}  onMouseEnter={() => setButtonColor("#007aff")}  onMouseLeave={() =>setButtonColor(isASelected ? "#ff3b30" : "transparent")}> &#128483; </button>
        
        <div className="settings-button-container">

          <Link to="/settings">
            <button type="button" className="settings-button">&#9881;</button>
          </Link>
          <button type="button" id="rabbit" onClick={() => buttonConnect()}  className="rabbit">&#128048;</button>

          <button type="button" id="scuttlebutt" onClick={() => say_use_case("scuttlebutt")} className="scuttlebutt">&#128240;</button>

          <button type="button" id="shoreleave" onClick={() => say_use_case("shoreleave")} className="shoreleave">&#127861;</button>

          <button type="button" id="lookout" onClick={() => say_use_case("lookout")}  className="lookout">&#128065;</button>
          
          <button type="button" id= "racktime" onClick={() => say_use_case("racktime")} className="racktime">&#128164;</button>

          <button type="button" id="Logout" onClick={() => Logout()} className="settings-button">&#x23FB;</button>

        </div>
      </div>

      <div className="nots">
        <div className="notification-centerNew">
        <div className={"notification-containerNew"}>
            {notifications.map((notification, index) => (
              <div key={index} className={`notificationNew ${notification.color} ${!expanded ? 'expanded' : ''}`} onClick={() => setExpanded(!expanded)}>
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

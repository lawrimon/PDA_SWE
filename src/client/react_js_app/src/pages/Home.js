import './Home.css';
import './NotificationCenter.css'
import logo from '../resources/cAPItan_Logo.jpg';
import logo2 from '../resources/spongie2.gif';
import React, { useState, useEffect, useRef } from 'react';
import { speak, stopListening, startListening, listenForSpeech } from '../components/SpeechFunctions';
import { Link } from 'react-router-dom';
import { getUserId, setUserId, user_id } from '../components/User.js';
import io from 'socket.io-client';


export function Home() {
  var originalColor;
  const [notifications, setNotifications] = useState([]);
  const [logoSrc, setLogoSrc] = useState(logo);
  const [queueName, setQueueName] = useState(null);
  const [text, setText] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const [isASelected, setIsASelected] = useState(false);
  const [buttonColor, setButtonColor] = useState('transparent');

  const useridRef = useRef(null);
  const socketRef = useRef(null);
  const deliveryTagRef = useRef('');

  const ENDPOINT = 'http://localhost:5010/';
  let next_message = false;
  let connected = false;

  const NotificationColors = {
    scuttlebutt: 'gray',
    shoreleave: 'lightpink',
    lookout: 'lightgreen',
    racktime: 'brown',
  };

  const UsecasePorts = {
    shoreleave: '13',
    lookout: '19',
    scuttlebutt: '08',
    racktime: '16',
  };

  // set to true to avoid long TTS
  const debug = false;

  // function to update delivery tag
  const updateDeliveryTag = (tag) => {
    deliveryTagRef.current = tag;
  };

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
    }

    // invalid login user
    else {
      // disconnect current socket
      handleDisconnect()
      Logout()
    }

    // disconnect socket on unmount
    return () => {
      handleDisconnect()
    };
  }, [getUserId()]);

  function buttonConnect() {
    if (connected) {
      connected = false
      handleConnect();
    }
    else {
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

  function handleDisconnect() {

    // disconnect from websocket server
    if (socketRef.current) {

      // acknowledge message before disconnecting
      if (deliveryTagRef.current) {
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
    say_use_case("rabbit", message.message)
      .then(() => {
        if (deliveryTagRef.current && next_message) {
          handleAcknowledge(deliveryTagRef.current)
        }
      })
      .catch((error) => console.error("Error occurred:", error));
  };


  // asking user for additional information
  async function handleAdditional() {
    const question_text = "Thank you for listening. Do you want any additional information? "
    await speak(question_text)
  }


  const handleLogo = (insertlogo) => {
    setLogoSrc(insertlogo);
  };

  const Logout = () => {
    setUserId("")
    localStorage.clear()
    window.location.href = '/login';
  };

  const handleChange = (event) => {
    setText(event.target.value);
  };

  async function handleSubmit() {
    let intent1 = "";
    const url = `http://localhost:5021/dialogflow/get_intent?transcript=${text}`;
    await fetch(url)
      .then((response) => response.json())
      .then((data) => {
        intent1 = data.intent;
        console.log("intent", intent1)
        say_use_case(intent1);
      })
      .catch((error) => console.error(error));
  }


  function changeColor(div) {
    var button = document.getElementById(div);
    if (!button.classList.contains('red')) {
      originalColor = button.style.backgroundColor;
      button.style.backgroundColor = 'red';
    }
  }

  function setColor(div) {
    var button = document.getElementById(div);
    button.style.backgroundColor = originalColor;
  }

  const handleClick = () => {
    if (isASelected) {
      setButtonColor("transparent");
      setText(stopListening());
    } else {
      setButtonColor("#F62817");
      startListening();
    }
    setIsASelected(!isASelected);
  };


  // function that returns a Promise that resolves after a specified delay
  function delay(delayInMilliseconds) {
    return new Promise(resolve => setTimeout(resolve, delayInMilliseconds));
  }

  async function say_use_case(use_case, speaking_text = "") {
    try {
      let text;
      let tmp_use_case = use_case;

      if (use_case === "rabbit") {
        tmp_use_case = speaking_text._name;
        text = speaking_text;
      } else {
        switch (use_case) {
          case "scuttlebutt":
            text = await getScuttlebutt();
            break;
          case "lookout":
            text = await getLooktout();
            break;
          case "racktime":
            text = await getRackTime();
            break;
          case "shoreleave":
            text = await getShoreleave();
            break;
          default:
            return;
        }
      }

      const name = text._name;
      delete text._name;
      const keysInOrder = Object.keys(text);

      if (debug) {
        const textToSay = "This is a little example text";
        const use_case = "scuttlebutt";
        addNotification(textToSay, NotificationColors[use_case]);
        await speak(textToSay);
      } else {
        handleLogo(logo2);
        changeColor(name);

        for (const key of keysInOrder) {
          const value = text[key];
          addNotification(value, NotificationColors[name]);
          await speak(value);
        }
      }

      // pause for 2 seconds using Promises
      await delay(2000);
      handleLogo(logo);
      setColor(name);

      if (tmp_use_case === "scuttlebutt" || tmp_use_case === "shoreleave") {
        const tmp_transcript = await listenForSpeech();
        if(tmp_transcript){
          await handleTranscript(tmp_transcript, name);
        }
        
      }

      // acknowledge message so that next message can be consumed
      if (deliveryTagRef.current) {
        handleAcknowledge(deliveryTagRef.current);
      }
    } catch (error) {
      console.error("Error in say_use_case:", error);
    }
  }

  async function handleTranscript(transcript, usecase) {
    if (transcript.toLowerCase().includes("no")) {
      console.log("Alright, have a nice day!");
      return;
    }

    if (transcript.toLowerCase().length <= 2) {
      console.log("User did not request more information.");
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:50${UsecasePorts[usecase]}/${usecase}/additional`);
      const data = await response.json();

      if (response.status !== 200) {
        console.log("Error in response from Scuttlebut");
        return;
      }

      const additionalText = data.text.join("");
      addNotification(additionalText, NotificationColors[usecase]);
      await speak(additionalText);
    } catch (error) {
      console.log(error);
      console.log("Sorry, there was an error getting more information.");
    }
  }

  async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    if (data) {
      return data;
    }
  }

  async function getScuttlebutt() {
    const url = `http://127.0.0.1:5008/scuttlebutt?user=${useridRef.current}`;
    return fetchData(url);
  }

  async function getShoreleave() {
    const url = `http://127.0.0.1:5013/shoreleave?user=${user_id}`;
    return fetchData(url);
  }

  async function getLooktout() {
    const url = `http://127.0.0.1:5016/lookout?user=${user_id}`;
    return fetchData(url);
  }

  async function getRackTime() {
    const url = `http://127.0.0.1:5019/racktime?user=${user_id}`;
    return fetchData(url);
  }


  return (
    <div className="App">
      <div style={{ marginTop: "3%" }}>
        <img src={logoSrc} style={{ width: "12%" }} alt="Logo" className="logo" />
      </div>
      <h1 style={{ color: "white", paddingTop: "1%" }}>cAPItan</h1>
      <div className="search-container">
        <input type="text" value={text} onChange={handleChange} onClick={() => setShowPopup(false)}
          placeholder="Try: When should I go to bed ?" />
        <button type="button" className="ios-button" onClick={() => handleSubmit()}>&#127929;</button>
        <button className="ios-button" style={{ backgroundColor: buttonColor, }} onClick={() => handleClick()} onMouseEnter={() => setButtonColor("#007aff")} onMouseLeave={() => setButtonColor(isASelected ? "#ff3b30" : "transparent")}> &#128483; </button>
        <div className="settings-button-container">
          <Link to="/settings">
            <button type="button" className="settings-button">&#9881;</button>
          </Link>
          <button type="button" id="rabbit" onClick={() => buttonConnect()} className="rabbit">&#128048;</button>
          <button type="button" id="scuttlebutt" onClick={() => say_use_case("scuttlebutt")} className="scuttlebutt">&#128240;</button>
          <button type="button" id="shoreleave" onClick={() => say_use_case("shoreleave")} className="shoreleave">&#127861;</button>
          <button type="button" id="lookout" onClick={() => say_use_case("lookout")} className="lookout">&#128065;</button>
          <button type="button" id="racktime" onClick={() => say_use_case("racktime")} className="racktime">&#128164;</button>
          <button type="button" id="Logout" onClick={() => Logout()} className="settings-button">&#x23FB;</button>
        </div>
      </div>
      <div className="nots">
        <div className="notification-centerNew">
          <div className={"notification-containerNew"}>
            {notifications.map((notification, index) => (
              <div key={index} className={`notificationNew ${notification.color}`} onClick={() => setExpanded(!expanded)}>
                <div className={`notification-iconNew`} style={{ backgroundColor: notification.color }}></div>
                <div className="notification-textNew">{notification.message}</div>
                <button className="notification-closeNew" onClick={() => removeNotification(index)} >×</button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>


  );

}

export default Home;

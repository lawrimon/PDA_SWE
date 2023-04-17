import './Home.css';
import './NotificationCenter.css'
import logo from '../resources/cAPItan_Logo.jpg';
import logo2 from '../resources/spongie2.gif';

import React, { useState, useEffect, useRef } from 'react';

import { Link } from 'react-router-dom';
import { getUserId, setUserId, user_id } from '../components/User.js';
import { useSpeech } from '../components/SpeechFunctions';



export function Home() {
  var originalColor;

  const useridRef = useRef(null);
  const [notifications, setNotifications] = useState([]);

  const [logoSrc, setLogoSrc] = useState(logo);

  const [text, setText] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [message, setMessage] = useState('');
  let userid = null;
  const { textToSpeak, setTextToSpeak, speak, transcript, resetTranscript } = useSpeech();


  const addNotification = (message) => {
    const newNotifications = [message, ...notifications];
    setNotifications(newNotifications);
  }

  const removeNotification = (index) => {
    const newNotifications = [...notifications];
    newNotifications.splice(index, 1);
    setNotifications(newNotifications);
  }

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

  const handleLogo = (insertlogo) => {
    setLogoSrc(insertlogo);
  };

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
    addNotification("New Notification", notifications, setNotifications);
    handleLogo()
  };

  //STT and TTS
  const handleTextChange = (event) => {
    setTextToSpeak(event.target.value);
  };

  function changeColor(div) {
    var button = document.getElementById(div);
    if (!button.classList.contains('red')) {
      originalColor = button.style.backgroundColor;
      button.style.backgroundColor = 'red';
    }
  }

  function setColor(div){
    var button = document.getElementById(div);
    if (button.classList.contains('red')) {
      button.style.backgroundColor = originalColor;
    }
  }
  


  async function handleSpeakNew(usecase) {
    let answer;
    console.log("usecase", usecase)
    if (speechSynthesis.speaking) {
      return;
    }
    console.log("in handlespeak");

    if (usecase === "shoreleave") {
      const answer = await getShoreleave();
      console.log("answer:", answer);
      await new Promise(resolve => setTimeout(resolve, 1000)); // wait for 1 second
      return answer
    }
    else if (usecase === "scuttlebutt") {
      const answer = await sendToFrontend();
      console.log("answer:", answer);
      await new Promise(resolve => setTimeout(resolve, 1000)); // wait for 1 second
      return answer
    }

    else if (usecase === "lookout") {
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
    await changeColor('scuttlebutt')

    try {
      const text = await handleSpeakNew("scuttlebutt");
      console.log(text, "is the message then");
      addNotification(text, notifications, setNotifications);
      handleLogo(logo2)

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
      handleLogo(logo)
      await setColor('scuttlebutt')
      // Wait for 3 seconds before stopping the recognition
      setTimeout(() => {
        recognition.stop();
        console.log("Stopped listening");

        console.log(transcript, " is the transcript");

        recognition.onresult = function (event) {
          const transcript2 = event.results[0][0].transcript;
          console.log(transcript2, " is the transcript");
          if (transcript2 !== "") {
            recognition.onend = function () {
              console.log('Speech recognition service disconnected');
              console.log(transcript2, " is the transcript right before");

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
    return new Promise(res => setTimeout(res, delay));
  }

  async function sendTranscript(trans2) {
    let text = "";
    console.log("transcript in sendTranscript", trans2)

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

  async function sendToFrontend() {
    const response = await fetch('http://127.0.0.1:5008/scuttlebutt?user=' + useridRef.current)
    const data = await response.json();
    console.log("this data", data.toString())
    if (data) {
      setMessage(data)
      return data
    }
  };

  async function getShoreleave() {
    const response = await fetch('http://127.0.0.1:5013/shoreleave')
    const data = await response.json();
    console.log("this data", data.toString())
    if (data) {
      setMessage(data)
      return data
    }
  }

  async function getLooktout() {
    const response = await fetch('http://127.0.0.1:5016/lookout?user=' + user_id)
    const data = await response.json();
    console.log("this data", data.toString())
    if (data) {
      setMessage(data)
      return data
    }
  }

  async function say_lookout() {
    let val = ""
    await changeColor('lookout')

    try {
      const text = await handleSpeakNew("lookout");
      console.log(text, "is the message then");
      console.log(text, "is the message then");
      addNotification(text, notifications, setNotifications);
      handleLogo(logo2)

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
      handleLogo(logo)
      console.log("After speak");
      const recognition = new window.webkitSpeechRecognition();
      recognition.lang = 'en-US';
      recognition.start();
      await setColor('lookout')

      // Wait for 3 seconds before stopping the recognition
      setTimeout(() => {
        recognition.stop();
        console.log("Stopped listening");

        console.log(transcript, " is the transcript");

        recognition.onresult = function (event) {
          const transcript2 = event.results[0][0].transcript;
          console.log(transcript2, " is the transcript");
          if (transcript2 !== "") {
            recognition.onend = function () {
              console.log('Speech recognition service disconnected');
              console.log(transcript2, " is the transcript right before");

              say_additional(transcript2);

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
    await changeColor('shoreleave')
    try {
      const text = await handleSpeakNew("shoreleave");
      console.log(text, "is the message then");
      
      //setColor("shoreleave")
      handleLogo(logo2)
      addNotification(text, notifications, setNotifications);
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
      await setColor('shoreleave')

      const recognition = new window.webkitSpeechRecognition();
      recognition.lang = 'en-US';
      recognition.start();

      console.log("Listening...");
      
      // Wait for 3 seconds before stopping the recognition
      setTimeout(() => {
        recognition.stop();
        console.log("Stopped listening");
        handleLogo(logo)
        console.log(transcript, " is the transcript");

        recognition.onresult = function (event) {
          const transcript2 = event.results[0][0].transcript;
          console.log(transcript2, " is the transcript");
          if (transcript2 !== "") {
            recognition.onend = function () {
              console.log('Speech recognition service disconnected');
              console.log(transcript2, " is the transcript right before");
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
        <img src={logoSrc} style={{ width: "20%" }} alt="Logo" className="logo" />
      </div>
      <h1 style={{ color: "white", paddingTop: "1%" }}>cAPItan</h1>
      <div className="search-container">
        <input type="text" value={text} onChange={handleChange} onClick={() => setShowPopup(false)}
          placeholder="Search..." />
          <button type="button" onClick={handleSubmit}>Search</button>
        <div className="settings-button-container">

          <Link to="/settings">
            <button type="button" className="settings-button">&#x2699;</button>
          </Link>


          <button type="button" id ="scuttlebutt"  onClick={say_scuttlebutt} className="scuttlebutt">&#x2603;</button>

          <button type="button" id="shoreleave" onClick={say_shoreleave} className="shoreleave">&#128062;</button>

          <button type="button" id="lookout" onClick={say_lookout} className="lookout">&#x2656;</button>

          <button type="button" id ="Logout" onClick={Logout} className="settings-button">&#10149;</button>

        </div>
      </div>

      <div className="nots">
        <div className="notification-centerNew">
          <div className="notification-containerNew">
            {notifications.map((notification, index) => (
              <div key={index} className="notificationNew">
                <div className="notification-iconNew"></div>
                <div className="notification-textNew">{notification}</div>
                <button onClick={() => removeNotification(index)} className="notification-closeNew">×</button>
              </div>
            ))}
          </div>
          <button onClick={() => addNotification("New Notification")} className="add-notification-btnNew">
            Add Notification
          </button>
        </div>
      </div>

    </div>

  );

}

export default Home;

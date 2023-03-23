import './Home.css';
import logo from '../cAPItan_Logo.jpg';
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import NotificationPopup from './Notification';


export function Home() {
  const [text, setText] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [showModal, setShowModal] = useState(false);

  const toggleModal = () => setShowModal(!showModal);


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
            <button type="button" onClick={handleButtonClick} className="settings-button">✉</button>
          </div>

          <Link to="/settings">
            <button type="button" className="settings-button">&#x2699;</button>
          </Link>
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
    </div>
  );
}

export default Home;

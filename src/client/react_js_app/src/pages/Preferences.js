import React, { useState, useEffect, useRef } from "react";
import "./Preferences.css";
import { Link } from 'react-router-dom';
import { getUserId, setUserId } from './User.js';
import { getUserPreferences, setUserPreferences } from './User.js';


function PreferencesPage() {
  const useridRef = useRef(null);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [user_football_club, setFootballClub] = useState("FC Bayern München");
  const [user_stocks, setStocks] = useState("Apple");
  const [user_spotify_link, setSpotify] = useState("/spotify/url");
  const [user_calendar_link, setCalendar] = useState("/calender/url");
  const [user_artists, setArtist] = useState("Justin Bieber");
  
  let user_pref = [];
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

  function handleEmailChange(event) {
    setEmail(event.target.value);
  }

  function handleFootball(event) {
    setFootballClub(event.target.value);
  }

  function handleArtists(event) {
    setArtist(event.target.value);
  }

  function handleCalendar(event) {
    setCalendar(event.target.value);
  }

  function handleSpotify(event) {
    setSpotify(event.target.value);
  }

  function handleStocks(event) {
    setStocks(event.target.value);
  }


  function handlePasswordChange(event) {
    setPassword(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    user_pref = []
    setUserPreferences([user_football_club, user_stocks, user_artists, user_spotify_link, user_calendar_link])
    window.location.href = '/registersuccess';
    // handle login request

  }

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h1>Preferences</h1>
        <label>
          Email:
          <input type="email" value={email} onChange={handleEmailChange} />
        </label>
        <br />
        <label>
          Password:
          <input type="password" value={password} onChange={handlePasswordChange} />
        </label>
        <br />
        <label>
          Favorite Football Club
          <input type="text" value={user_football_club} onChange={handleFootball} />
        </label>
        <br />
        <label>
          Favorite Stocks:
          <input type="text" value={user_stocks} onChange={handleStocks} />
        </label>
        <br />
        <label>
          Favorite Artist:
          <input type="text" value={user_artists} onChange={handleArtists} />
        </label>
        <br />
        <label>
          Spotify Link:
          <input type="text" value={user_spotify_link} onChange={handleSpotify} />
        </label>
        <br />
        <label>
           Calendar Link
          <input type="text" value={user_calendar_link} onChange={handleCalendar} />
        </label>
        <br />
        <Link to="/">
        <button type="submit">Finish Setup</button>
        </Link>
     
      </form>
    </div>
  );
}

export default PreferencesPage;

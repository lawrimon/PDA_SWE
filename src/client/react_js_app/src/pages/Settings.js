import './Settings.css';
import logo from '../cAPItan_Logo.jpg';
import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { getUserId, setUserId } from './User.js';
import { getUserPreferencesDB, getUserPreferences } from './User.js';

export function Settings() {
    const useridRef = useRef(null);

    const [user_id, setUser_id] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [user_football_club, setFootballClub] = useState("FC Bayern München");
    const [user_stocks, setStocks] = useState("Apple");
    const [user_spotify_link, setSpotify] = useState("/spotify/url");
    const [user_calendar_link, setCalendar] = useState("/calender/url");
    const [user_artists, setArtist] = useState("Justin Bieber");
    let user_pref = []

    const handleSave = (event) => {
      event.preventDefault();
      // save settings data here
    };

    function handleUsernameChange(event) {
      setUsername(event.target.value);
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

    useEffect(() => {
      // Define an async function to retrieve the user preferences
      async function getUserPreferences() {
        // Retrieve the user ID from local storage
        const storedUserId = localStorage.getItem('user_id');
        if (storedUserId) {
          useridRef.current = storedUserId;
          console.log("Userid", useridRef.current);
          setUserId(useridRef.current)
        }
        // Call getUserPreferencesDB and wait for it to finish
        const pref = await getUserPreferencesDB(useridRef.current);
        return pref
      }
      
      async function setUserPreferences() {
        const pref = await getUserPreferences();
        console.log("this the pref", pref)
        setUsername(useridRef.current)
        setFootballClub(pref.football_club)
        setStocks(pref.stocks)
        setSpotify(pref.spotify_link)
        setCalendar(pref.calendar_link)
        setArtist(pref.artists)
      }
      
      setUserPreferences();
    }, []);
    
      
    const TestToggle = () =>{
      console.log(JSON.stringify({"username": useridRef.current, "football_club": user_football_club, "user_calendar_link": user_calendar_link, "user_spotify_link":user_spotify_link, "user_stocks":user_stocks, "user_artists": user_artists}),
      )
    }
    

    const  handleToggleChange = () => {
      fetch('http://localhost:5000/users/'+ useridRef.current, {
        method: 'PUT',
        body: JSON.stringify({"username": useridRef.current, "football_club": user_football_club, "user_calendar_link": user_calendar_link, "user_spotify_link":user_spotify_link, "user_stocks":user_stocks, "user_artists": user_artists}),
        headers: { 'Content-Type': 'application/json' },
      })
      .then(response => response.json())
      .then(data => {
        if (data) {
            console.log(data)
            console.log("success User changed")
        }
        else {
          console.log("Error");
        }
      })
    .catch(error => {
      console.error(error);
    });
      };

    const handleClose = () => {
      // handle closing of overlay here
    };
  
    return (
        <div className="App">
      <div className="overlay-container">
        <div className="overlay">
          <div className="overlay-header">
            <h2>Settings</h2>
          </div>
          <div className="overlay-content">
          <div className="login-form">
        <h1>Preferences</h1>
        <label>
          Username:
          <input type="username" value={username} onChange={handleUsernameChange} />
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
        <button type="submit" onClick={handleToggleChange} >Save Changes</button>
        <Link to="/">
        <button type="submit"  >Back to Home</button>
          </Link>
       
      </div>
          </div>
        </div>
      </div>
      </div>
    );
  }
  
  export default Settings;



   

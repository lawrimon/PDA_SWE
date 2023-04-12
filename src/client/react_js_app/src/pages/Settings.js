import './Settings.css';
import logo from '../resources/cAPItan_Logo.jpg';
import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { getUserId, setUserId } from '../components/User.js';
import { getUserPreferencesDB, getUserPreferences } from '../components/User.js';
import Select from 'react-select';
import makeAnimated from 'react-select/animated';

export function Settings() {
  const useridRef = useRef(null);

  const [user_id, setUser_id] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [user_football_club, setFootballClub] = useState(["Bayern München"]);
  const [user_stocks, setStocks] = useState(["Apple"]);
  const [user_spotify_link, setSpotify] = useState("/spotify/url");
  const [user_calendar_link, setCalendar] = useState("/calender/url");
  const [user_artists, setArtist] = useState(["Justin Bieber"]);
  const [user_news, setNews] = useState(["National"]);
  const [user_books, setBooks] = useState(["Non-Fiction"]);

  let user_pref = []

  const options = [
    { value: 'chocolate', label: 'Chocolate' },
    { value: 'strawberry', label: 'Strawberry' },
    { value: 'vanilla', label: 'Vanilla' }
  ]
  const animatedComponents = makeAnimated();

  const soccer_options = [
    { value: 'FC Bayern München', label: 'FC Bayern München' },
    { value: 'Borussia Dortmund', label: 'Borussia Dortmund' },
    { value: 'VFB Stuttgart', label: 'VFB Stuttgart' },
    { value: 'Real Madrid', label: 'Real Madrid' },
    { value: 'FC Barcelona', label: 'FC Barcelona' },
    { value: 'Manchester United', label: 'Manchester United' },
    { value: 'Paris Saint Germain', label: 'Paris Saint Germain' },
    { value: 'AC Milan', label: 'AC Milan' },
  ]

  const stock_options = [
    { value: 'Apple', label: 'Apple' },
    { value: 'Microsoft', label: 'Microsoft' },
    { value: 'Alphabet', label: 'Alphabet' },
    { value: 'Amazon', label: 'Amazon' },
    { value: 'NVIDIA', label: 'NVIDIA' },
    { value: 'Tesla', label: 'META Platforms' },
    { value: 'TSMC', label: 'TSMC' },
    { value: 'Ford', label: 'Ford' },
  ]

  const artist_options = [
    { value: 'Justin Bieber', label: 'Justin Bieber' },
    { value: 'Central Cee', label: 'Central Cee' },
    { value: 'Ski Aggu', label: 'Ski Aggu' },
    { value: 'RIN', label: 'RIN' },
    { value: 'Selena Gomez', label: 'Selena Gomez' },
    { value: 'Rihanna', label: 'Rihanna' },
    { value: 'Doja Cat', label: 'Doja Cat' },
    { value: 'Helene Fischer', label: 'Helene Fischer' },
  ]

  const news_options = [
    { value: 'Business', label: 'Business' },
    { value: 'Sport', label: 'Sport' },
    { value: 'National', label: 'National' },
    { value: 'International', label: 'International' },
    { value: 'Politics', label: 'Politics' },
    { value: 'Lifestyle', label: 'Lifestyle' }
  ]

  const book_options = [
    { value: 'Non-Fiction', label: 'Non-Fiction' },
    { value: 'Fiction', label: 'Fiction' },
    { value: 'Miscellaneous', label: 'Miscellaneous' },
    { value: 'Picture Books', label: 'Picture Books' }
  ]

  const handleSave = (event) => {
    event.preventDefault();
    // save settings data here
  };

  function handleUsernameChange(event) {
    setUsername(event.target.value);
  }

  function handleNews(selectedOptions) {
    setNews(selectedOptions.map(option => option.value));
  }

  function handleBooks(selectedOptions) {
    setBooks(selectedOptions.map(option => option.value));
  }

  function handleFootball(selectedOptions) {
    setFootballClub(selectedOptions);
    console.log(setFootballClub.map(option => option.value));
  }

  function handleFootball(selectedOptions) {
    setFootballClub(selectedOptions.map(option => option.value));
  }
  function handleArtists(selectedOptions) {
    setArtist(selectedOptions.map(option => option.value));
  }

  function handleCalendar(event) {
    setCalendar(event.target.value);
  }

  function handleSpotify(event) {
    setSpotify(event.target.value);
  }

  function handleStocks(selectedOptions) {
    setStocks(selectedOptions.map(option => option.value));
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
      setFootballClub([pref.football_club])
      setStocks([pref.stocks])
      setSpotify(pref.spotify_link)
      setCalendar(pref.calendar_link)
      setArtist([pref.artists])
      setBooks([pref.books])
    }

    setUserPreferences();
  }, []);

  

  const TestToggle = () => {
    console.log(JSON.stringify({ "username": useridRef.current, "football_club": user_football_club, "user_calendar_link": user_calendar_link, "user_spotify_link": user_spotify_link, "user_stocks": user_stocks, "user_artists": user_artists, "user_books": user_books }),
    )
  }


  const handleToggleChange = () => {
    console.log("handle triggered")
    fetch('http://localhost:5000/users/' + useridRef.current, {
      method: 'PUT',
      body: JSON.stringify({ "username": useridRef.current, "football_club": user_football_club, "user_calendar_link": user_calendar_link, "user_spotify_link": user_spotify_link, "user_stocks": user_stocks, "user_artists": user_artists, "news": user_news}),
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
    <div className='overlay-container'>
      <div className="overlay">
        <div className="overlay-header">
          <h2>Settings</h2>
        </div>
        <div className="overlay-content">
          <div className="settings-form">
            <label>
              <h4> Username</h4>
              <input type="email" value={username} onChange={handleUsernameChange} />
            </label>
            <br />
            <h4>Favorite Football Club </h4>
            <Select
              closeMenuOnSelect={false}
              components={animatedComponents}
              isMulti
              options={soccer_options}
              value={user_football_club.map(fc => ({ label: fc, value: fc }))}
              onChange={handleFootball}
            />
            <br />
            <br />
            <h4>Favorite Stocks  </h4>
            <Select
              closeMenuOnSelect={false}
              components={animatedComponents}
              isMulti
              options={stock_options}
              value={user_stocks.map(fc => ({ label: fc, value: fc }))}
              onChange={handleStocks}
            />
            <br />
            <h4>Favorite Artists  </h4>
            <Select
              closeMenuOnSelect={false}
              components={animatedComponents}
              isMulti
              options={artist_options}
              value={user_artists.map(fc => ({ label: fc, value: fc }))}
              onChange={handleArtists}
            />
            <br />
        <h4>Favorite News-Topics  </h4>
          <Select
            closeMenuOnSelect={false}
            components={animatedComponents}
            isMulti
            options={news_options}
            value={user_news.map(fc => ({ label: fc, value: fc }))}
            onChange={handleNews}
          />
        <br />
        <h4>Favorite Book-Topics  </h4>
          <Select
            closeMenuOnSelect={false}
            components={animatedComponents}
            isMulti
            options={book_options}
            value={user_books.map(fc => ({ label: fc, value: fc }))}
            onChange={handleBooks}
          />
        <br />
            <label>
              <h4>Spotify Link </h4>
              <input type="email" value={user_spotify_link} onChange={handleSpotify} />
            </label>
            <label>
              <h4>Calendar Link  </h4>
              <input type="email" value={user_calendar_link} onChange={handleCalendar} />
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
  );
}

export default Settings;






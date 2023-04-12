import React, { useState, useEffect, useRef } from "react";
import "./Preferences.css";
import { Link } from 'react-router-dom';
import { getUserId, setUserId } from '../components/User.js';
import { getUserPreferences, setUserPreferences } from '../components/User.js';
import Select from 'react-select';
import makeAnimated from 'react-select/animated';

function PreferencesPage() {
  const useridRef = useRef(null);

  const [username, setUsername] = useState(useridRef.current);
  const [password, setPassword] = useState("");
  const [user_football_club, setFootballClub] = useState(["Bayern München"]);
  const [user_stocks, setStocks] = useState(["Apple"]);
  const [user_spotify_link, setSpotify] = useState("/spotify/url");
  const [user_calendar_link, setCalendar] = useState("/calender/url");
  const [user_artists, setArtist] = useState(["Justin Bieber"]);
  const [user_news, setNews] = useState(["National"]);
  const [user_books, setBooks] = useState(["Non-Fiction"]);

  let user_pref = [];
  let userid = null;
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
  const animatedComponents = makeAnimated();

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

  function handleUsernameChange(event) {
    setUsername(event.target.value);
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

  function handleNews(selectedOptions) {
    setNews(selectedOptions.map(option => option.value));
  }

  function handleBooks(selectedOptions) {
    setBooks(selectedOptions.map(option => option.value));
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

  async function handleSubmit(event) {
    event.preventDefault();
    await uploadSubmit();
    setUserPreferences([user_football_club, user_stocks, user_artists, user_spotify_link, user_calendar_link, user_news, user_books])
    window.location.href = '/registersuccess';
  }
  
    
    
    // handle login request


  const uploadSubmit = async () => {
    console.log("handle triggered")
    console.log(useridRef.current)
    try {
      const response = await fetch('http://localhost:5009/users/'+useridRef.current, {
        method: 'PUT',
        body: JSON.stringify({"football_club": user_football_club.toString(), "user_calendar_link": user_calendar_link, "user_spotify_link": user_spotify_link, "stocks": user_stocks.toString(), "artists": user_artists.toString(), "news": user_news.toString(), "books": user_books.toString()}),
        headers: { 'Content-Type': 'application/json' },
      });
      const data = await response.json();
      console.log("lol")
      if (data) {
        console.log(data)
        console.log("success preferences saved")
        return data
      }
      else {
        console.log("Error");
      }
    } catch (error) {
      console.error(error);
    }
  };
  

  return (
    <div className="pref-container">
      <form onSubmit={handleSubmit} className="pref-form">
        <h1>Preferences</h1>
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
        <br />
        <h4>Favorite Book Topics </h4>
          <Select
            closeMenuOnSelect={false}
            components={animatedComponents}
            isMulti
            options={book_options}
            value={user_books.map(fc => ({ label: fc, value: fc }))}
            onChange={handleBooks}
          />
        <br />
        <h4>Spotify Link </h4>
          <input type="text" value={user_spotify_link} onChange={handleSpotify} />
        <label>
        <h4>Calendar Link  </h4>
          <input type="text" value={user_calendar_link} onChange={handleCalendar} />
        </label>
        
        <button type="submit">Finish Setup</button>
     
      </form>
    </div>
  );
}

export default PreferencesPage;

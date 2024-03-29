import React, { useState, useRef, useEffect } from "react";
import "./Login.css";
import { Link } from 'react-router-dom';
import { getUserId, setUserId, setUserPreferences } from '../components/User.js';
import Nominatim from 'nominatim-geocoder';


function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [user_id, setUser_id] = useState("");
  const [userPref, setUserPref] = useState([]);
  const userIdRef = useRef(null);
  const [user_location, setUserLocation] = useState("");



  useEffect(() => {
    // Call your function here
    // Retrieve the user ID from local storage
    componentDidMount()
    let position = UserDidMount()
    if (position) {
      console.log(position.coords)
      console.log(user_location, "userrr")
    }
  }, [getUserId()]);

   

  function handleUsernameChange(event) {
    setUsername(event.target.value);
    setUser_id(event.target.value);
    userIdRef.current = event.target.value;
  }

  function handleLocationChange(location){
    setUserLocation(location)
  }

  const getCityName = async (lat, lng) => {
    const nominatim = new Nominatim();
    const result = await nominatim.reverse({
      lat: lat,
      lon: lng,
      addressdetails: 1,
      zoom: 18
    });
    const city = result.address.city || result.address.town || result.address.village;
    return city;
  };
  

  function getUserPref() {
    fetch('http://localhost:5009/users/' + user_id, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
      .then(response => response.json())
      .then(data => {
        if (data) {
          setUserPref([data.user_football_club, data.user_stocks, data.user_artists, data.user_spotify_link, data.user_calendar_link]);
        }
      })
      .catch(error => {
        console.error(error);
      });
  }

  function componentDidMount() {
        if ("geolocation" in navigator) {
          console.log("Available");
        } else {
          console.log("Not Available");
        }
      }

  function UserDidMount() {
        let coord = navigator.geolocation.getCurrentPosition(
          function(position) {
            console.log(position.coords);
            setUserLocation(position.coords)
          },
          function(error) {
            console.error("Error Code = " + error.code + " - " + error.message);
        }
    );
    return coord
     }

     async function handleLocationSubmit(event) {
      const city = await getCityName(user_location.latitude, user_location.longitude);
      await pushUserLocation(city)
      getUserPref();
      localStorage.setItem('user_id', userIdRef.current);
      window.location.href = '/'
    }

  function Register(){
    localStorage.setItem('user_id', userIdRef.current);
    window.location.href = '/register'
  }

  function pushUserLocation(city){
     let lat = user_location.latitude
     let lon =  user_location.longitude
      fetch('http://localhost:5009/users/' + user_id, {
        method: 'PUT',
        body: JSON.stringify({"location":city, "coordinates":[lat,lon].toString()}),
        headers: { 'Content-Type': 'application/json' },
      })
        .then(response => response.json())
        .then(data => {
          if (data) {
            console.log("success location saved")
          }
          else {
            console.log("Error");
          }
        })
        .catch(error => {
          console.error(error);
        });
    };
    

  function handlePasswordChange(event) {
    setPassword(event.target.value);
  }

  function showErrorMessage(message) {
    const errorMessageElement = document.getElementById('error-message');
    errorMessageElement.innerText = message;
    errorMessageElement.style.color = 'red';
  }

  async function handleSubmit (){
    await fetch('http://localhost:5009/users/' + user_id, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        if (data["error"]){
          showErrorMessage('Wrong credentials, try again!');


        }
        else if (data) {
          console.log(data);
          if (data.password == password) {
            console.log("ref", userIdRef.current);
            setUserId(userIdRef.current);}
            handleLocationSubmit()}
        else {
          console.log("login failed")
        }})
          
      .catch(error => {
        console.error(error);
      });
  }

  return (
    <div className="login-overall">
      <div className="login-container">
        <div className="login-form">
          <h1>Log In</h1>
          <label>
            Email:
            <input type="username" value={username} onChange={handleUsernameChange} />
          </label>
          <br />
          <label>
            Password:
            <input type="password" value={password} onChange={handlePasswordChange} />
          </label>
          <br />
          <div className="container">
            <label>
              Not a Sailor yet? Get on board <Link onClick={Register}>here</Link>.
            </label>
            <div id="error-message"></div> {/* Add this div for displaying error message */}

          </div>
          <button type="submit" onClick={handleSubmit}>Log In</button>

        </div>

      </div>
    </div>
  );
}

export default LoginPage;


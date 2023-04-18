
export let user_id = null;
export let user_name = null;
export let user_password = null;
export let user_football_club = null;
export let user_stocks = null;
export let user_artists = null;
export let user_calendar_link = null;
export let user_github = null;
export let user_event_location = null;
export let user_transportation = null;

export let user_preferences = [user_football_club, user_stocks, user_artists, user_calendar_link, user_event_location, user_github, user_transportation]

export function setUserId(userId) {
  user_id = userId;
}

export function getUserId() {
  return user_id;
}

export function getUserPreferences() {
    return user_preferences;
  }

  export function getUserPreferencesDB(userid) {
    console.log("this userid gets searched", userid);
    return fetch('http://localhost:5009/users/' + userid, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        if (!data) {
          throw new Error('Failed to send data to server');
        } else {
          console.log(data);
          console.log('Data sent successfully');
          return data;
        }
      })
      .catch(error => {
        console.error(error);
      });
  }
  
export function setUserPreferences(pref_list){
    let old_list = [user_football_club, user_stocks, user_artists, user_calendar_link, user_event_location, user_github, user_transportation]
    for (let i = 0; i < pref_list.length; i++) {
      old_list.push(pref_list[i]);
    }
  }

function pushUserPreferences(pref_list){
    const user_preferences = {
        "user_football_club": user_football_club,
        "user_stocks": user_stocks,
        "user_artists": user_artists,
        "user_calendar_link" : user_calendar_link,
      };
    
    const jsonPreferences = JSON.stringify(user_preferences);
    fetch('https://example.com/api/preferences', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: jsonPreferences
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to send data to server');
        }
        console.log('Data sent successfully');
      })
      .catch(error => {
        console.error(error);
      });
}

   
    
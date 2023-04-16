"""This application is the rack time use case.

Every evening one hour before the calcuated bedtime, the rack time use case proactively informs the user about his open issues and events for the next day.

Typical endpoints usage:

    GET /racktime?user=cr7thegoat
"""

from flask import Flask, jsonify, request
import requests
import flask_cors
from datetime import date, datetime
app = Flask(__name__)
flask_cors.CORS(app)

def get_issues(username):
    """Get assigned issues.
    
    This functions call the issues endpoint of the coding service and returns the open issues assigned to a user.
    
    Args:
        username: The username of the user. Only one username can be selected.
        
    Returns:
        Information about the open issues assigned to the user wrappen in an answer sentence.
    """

    url = f"http://coding:5000/issues"
    params = {"username": username}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Error getting issues"}), 500
    
    issues = response.json()

    if not issues:
        answer = "Congrats! There are no open issues assigned to you."
        return answer
    
    answer = "The following issue is a perfect candidate for your workday tomorrow: " + issues[0]["title"] + " in the " + issues[0]["repository"] + " repository." + " It is about " + issues[0]["description"] + ". These are the labels: "
    for label in issues[0]["labels"]:
        answer += label + ", "
    answer = answer[:-2] + "."

    return answer

def play_music(artist):
    """Play music.
    
    This functions calls the play endpoint of the music service and plays music of a given artist.

    Args:
        artist: The artist of the song to be played. Only one artist can be selected.
    """

    url = f"http://music:5000/music"
    params = {"artist": artist}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Error playing music"}), 500

    return 

def get_route(origin, destination, mode):
    """Get route.
    
    This functions calls the route endpoint of the maps and returns the route from origin to destination.

    Args:
        origin: The origin of the route.
        destination: The destination of the route.
        mode: The mode of transportation. Can be "driving", "walking", "bicycling" or "transit". Only one mode can be selected.
        
    Returns:
        Information about the route wrappen in an answer sentence.
    """

    url = f"http://maps:5000/route"
    params = {"origin": origin, "destination": destination, "mode": mode}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Error getting route"}), 500
    
    route = response.json()


    answer = "The route from your home to your first appointment is " + route["distance"]["text"] + " long and will take " + route["duration"]["text"] + " with your preferred mode " + mode + "."

    return answer

def get_user_preferences(user):
    """Get user preferences.

    This functions calls the user endpoint of the database service and returns the user preferences.

    Args:
        user: The username of the user. Only one username can be selected.

    Returns:
        The user preferences.
    """

    url = "http://db:5000/users/" + user

    response = requests.get(url)
    if response.status_code != 200:
        jsonify({"error": "Error getting stock news information"}), 500

    data = response.json()
    return data

def get_calendar_events_tomorrow(user):
    """
    Get tomorrow's calendar events endpoint.

    This endpoint makes a GET request to a specified URL to fetch tomorrow's calendar events for the given user. The user parameter is included in the request as a query parameter. If the response status code is not 200, an error message is returned. Otherwise, the response data is parsed as JSON and returned.

    Args:
        user: The username of the user whose calendar events to fetch.
    
    Returns:
        data: A dictionary containing the calendar events for tomorrow.
    """

    url = "http://127.0.0.1:5000/calendar/appointments/tomorrow"

    response = requests.get(url, params={"user": user})
    if response.status_code != 200:
        jsonify({"error": "Error getting tomorrows calendar events"}), 500

    data = response.json()
    return data
    
def summarize_tomorrows_events(events_tomorrow):
    """Summarize tomorrow's events endpoint.

    This endpoint takes a list of events for tomorrow and summarizes them into a single string. The resulting summary includes the start and end times, the event name, and the location (extracted from the event dictionary).

    Args:
        events_tomorrow: A list of event dictionaries for tomorrow.
    
    Returns:
        summarize_events: A summary string of tomorrow's events.
    """

    summarize_events = "tomorrow "

    for event in events_tomorrow:
        start_time = datetime.fromisoformat(event["start"]["dateTime"]).strftime("%I:%M %p")
        end_time = datetime.fromisoformat(event["end"]["dateTime"]).strftime("%I:%M %p")
        location = event["location"].split(",")[0]
        summarize_events += f"at {start_time} until {end_time} the {event['summary']} takes place in {location}. "

    return summarize_events

@app.route("/racktime")
def get_racktime():
    """Rack time endpoint.
    
    This endpoint provides the rack time use case logic. 

    Args:
        user: The username of the user. Only one username can be selected.
    
    Returns:
        The rack time information.
    """

    if not request.args.get("user"):
        return jsonify({"error": "Missing parameters"}), 400
    
    user = request.args.get("user")

    # TODO: Remove mock data
    github_user = "maxkie1"
    artist = "Ski Aggu"
    origin = "48.889124,9.122071"
    destination = "48.69047409776592,8.993838658674152"
    mode = "driving"
    mock_calendar_user = "maxkie1"


    user_preferences = get_user_preferences(user)
    github_user = user_preferences["github"]
    artist = user_preferences["artists"].split(",")[0]
    origin = user_preferences["coordinates"]
    mode = user_preferences["transportation_mode"]

    
    events_tomorrow = get_calendar_events_tomorrow(mock_calendar_user)
    if events_tomorrow:
        destination = events_tomorrow[0].get("location")
        route = get_route(origin, destination, mode)
        tomorrows_events_summarized = summarize_tomorrows_events(events_tomorrow)
    else:
        route = ""
        tomorrows_events_summarized = "There are no events in your calendar tomorrow."

    issues = get_issues(github_user)

    play_music(artist)

    introduction = "Good evening, it's rack time. According to your sleep schedule, you should go to bed in one hour. "
    additional_information = "Thank you for listening. Do you want any additional information?"

    return jsonify (
        introduction,
        tomorrows_events_summarized,
        issues,
        route,
        additional_information,
    )


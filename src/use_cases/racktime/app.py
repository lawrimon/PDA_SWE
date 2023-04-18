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
        Information about the open issues assigned to the user or an explanatory string if no issues information could be retrieved.
    """

    url = f"http://coding:5000/issues"
    params = {"username": username}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return "No open issues found for the provided user."
        # return jsonify({"error": "Error getting issues"}), 500

    issues = response.json()
    if not issues:
        answer = "Congrats! There are no open issues assigned to you."
        return answer
    answer = (
        "The following issue is a perfect start for your day tomorrow: "
        + issues[0]["title"]
        + " in the "
        + issues[0]["repository"]
        + " repository."
        + " It is about "
        + issues[0]["description"]
        + ". These are the labels: "
    )
    for label in issues[0]["labels"]:
        answer += label + ", "
    answer = answer[:-2] + ". "

    return answer


def play_music(artist):
    """Play music.

    This functions calls the play endpoint of the music service and plays music of a given artist.

    Args:
        artist: The artist of the song to be played. Only one artist can be selected.

    Returns:
        Acknowledgement that the music is playing or an explanatory string if no music could be played.
    """

    url = f"http://music:5000/music"
    params = {"artist": artist}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return "No music found for the provided artist. "
        # return jsonify({"error": "Error playing music"}), 500

    answer = "Music of your favorite artist " + artist + " is playing. Groove on! "

    return answer


def get_route(origin, destination, mode):
    """Get route.

    This functions calls the route endpoint of the maps and returns the route from origin to destination.

    Args:
        origin: The origin of the route.
        destination: The destination of the route.
        mode: The mode of transportation. Can be "driving", "walking", "bicycling" or "transit". Only one mode can be selected.

    Returns:
        Information about the route or an explanatory string if no route information could be retrieved.
    """

    transportation_modes = {
        "Walking": "walking",
        "Car": "driving",
        "Bicycle": "bicycling",
        "Public Transport": "transit",
    }

    url = f"http://maps:5000/route"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": transportation_modes[mode],
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return "No route found for the provided origin and destination. "
        # return jsonify({"error": "Error getting route"}), 500

    route = response.json()
    answer = (
        "The route from your home to your first appointment is "
        + route["distance"]["text"]
        + " long and will take "
        + route["duration"]["text"]
        + " with your preferred means of transportation "
        + mode
        + ". "
    )

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
        jsonify({"error": "Error getting user preferences"}), 500

    data = response.json()

    return data


def get_calendar_events_tomorrow(user):
    """Get tomorrow's calendar events.

    This function calls the calendar service and returns the calendar events for tomorrow.

    Args:
        user: The username of the user whose calendar events to fetch.

    Returns:
        A list of calendar events for tomorrow.
    """

    url = "http://calendar:5000/calendar/appointments/tomorrow"
    response = requests.get(url, params={"user": user})
    if response.status_code != 200:
        return None
        # return jsonify({"error": "Error getting tomorrows calendar events"}), 500

    data = response.json()

    return data


def parse_event_locations(events):
    """Parse event locations.

    This function takes a list of event dictionaries and extracts the location information from each event.
    If the location string can be parsed, latitude, longitude, and city data are extracted and stored in a dictionary.
    If the location string cannot be parsed, an error message is printed to the console.

    Args:
        events: A list of event dictionaries.

    Returns:
        A list of dictionaries containing latitude, longitude, and city data for each event.
    """

    locations = []
    for event in events:
        location = event.get("location")
        if location:
            try:
                lat, lon, city = location.split(" ")
                data = {"lat": lat, "lon": lon, "city": city}
                locations.append(data)
            except ValueError:
                print(f"Error parsing location string: {location}")

    return locations


def summarize_tomorrows_events(events_tomorrow, locations):
    """Summarize tomorrow's events.

    This function takes a list of events for tomorrow and summarizes them into a single string.
    The resulting summary includes the start and end times, the event name, and the location (extracted from the event dictionary).

    Args:
        events_tomorrow: A list of event dictionaries for tomorrow.
        locations: A list of location dictionaries.

    Returns:
        A summary of tomorrow's events or an explanatory string if no events could be found.
    """

    summarize_events = "Here is a summary of your events for tomorrow: "

    for event, location in zip(events_tomorrow, locations):
        start_time = datetime.fromisoformat(event["start"]["dateTime"]).strftime(
            "%I:%M %p"
        )
        end_time = datetime.fromisoformat(event["end"]["dateTime"]).strftime("%I:%M %p")
        summarize_events += f"At {start_time} until {end_time} the {event['summary']} takes place in {location.get('city')}. "

    return summarize_events


@app.route("/racktime")
def get_racktime():
    """Rack time endpoint.

    This endpoint provides the rack time use case logic.

    Args:
        user: The username of the user. Only one username can be selected.

    Returns:
        The rack time use case response containing tomorrow's calendar events, the route to the first event and open issues.
    """

    if not request.args.get("user"):
        return jsonify({"error": "Missing parameters"}), 400

    user = request.args.get("user")

    # TODO: Remove mock data
    mock_calendar_user = "maxkie1"

    user_preferences = get_user_preferences(user)
    github_user = user_preferences["github"]
    artist = user_preferences["artists"].split(",")[0]
    origin = user_preferences["coordinates"]
    mode = user_preferences["transportation"]

    events_tomorrow = get_calendar_events_tomorrow(mock_calendar_user)
    event_locations = parse_event_locations(events_tomorrow)

    if events_tomorrow:
        destination = f"{event_locations[0].get('lat')},{event_locations[0].get('lon')}"
        route = get_route(origin, destination, mode)
        tomorrows_events_summarized = summarize_tomorrows_events(
            events_tomorrow, event_locations
        )
    else:
        route = "There is no transportation needed. You can stay in your bed all day. "
        tomorrows_events_summarized = "There are no events in your calendar tomorrow. "

    issues = get_issues(github_user)

    music = play_music(artist)

    introduction = "Good evening, it's rack time. According to your sleep schedule, you should go to bed in one hour. "

    return jsonify(
        {
            "1introduction": introduction,
            "tomorrows_events": tomorrows_events_summarized,
            "route": route,
            "issues": issues,
            "music": music,
        }
    )

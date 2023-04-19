"""This application is the lookout duty use case.

The lookout duty use case provides the user with information about upcoming events and spport fixtures.

Example Usage:

    GET /lookoutduty?user=cr7thegoat
"""

from flask import Flask, jsonify, request
import requests, flask_cors
import json
from datetime import datetime

app = Flask(__name__)
flask_cors.CORS(app)


def get_club_ids(clubs):
    """Get club IDs.

    This functions returns the club IDs for a given list of club names.

    Args:
        clubs: The list of club names.

    Returns:
        The club IDs of the given club names.
    """

    ids = {
        "Bayern München": "157",
        "Borussia Dortmund": "165",
        "VfB Stuttgart": "172",
        "Real Madrid": "541",
        "FC Barcelona": "529",
        "Manchester United": "33",
        "Paris Saint Germain": "85",
        "AC Milan": "489",
    }

    club_ids = []
    for club in clubs:
        club_ids.append(ids.get(club, "Club ID not found"))

    return club_ids


def get_events(location, keyword_list, enddate):
    """Get events.

    This functions calls the events endpoint of the events service and returns the events.

    Args:
        location: The location of the events.
        keyword_list: The list of keywords for the events.
        enddate: The end date of the event search.

    Returns:
        Information about the events or an explanatory string if no events information could be retrieved.
    """

    url = f"http://events:5000/events/all"
    params = {"location": location, "artists": keyword_list, "enddate": enddate}
    response = requests.get(url, params)
    if response.status_code != 200:
        return "No events found for the provided search criteria."
        # jsonify({"error": "Error getting weather information"}), 500

    data = response.json()
    if not data:
        return "No events found in your area basedo on your favorite artists."
    
    else:
        answer = "Here are some event suggestions based on your favorite artists: "
        for event in data:
            answer += (
                "On the "
                + event["date"]
                + " in "
                + event["location"]
                + " you can see "
                + event["name"]
                + ". "
                + " The price is "
                + event["price"]
                + " and the genre of the event is "
                + event["topic"]
                + " ."
            )

        return answer


def get_sports(club_ids, clubs):
    """Get sports fixtures.

    This functions calls the fixture endpoint of the sports service and returns the sports fixtures.

    Args:
        club_ids: The list of club IDs.
        clubs: The list of club names.

    Returns:
        Information about the sports fixtures or an explanatory string if no sports fixtures information could be retrieved.
    """

    answer = "Here are some upcoming sports fixtures based on your favorite teams: "
    count = 0

    for club_id in club_ids:
        params = {"team": club_id}
        url = f"http://sports:5000/football/fixture"
        response = requests.get(url, params)
        if response.status_code != 200:
            return "No sports fixtures found for the provided team."
            # jsonify({"error": "Error getting weather information"}), 500

        data = response.json()
        if clubs[count] == data["away_team"]:
            other_team = data["home_team"]
        else:
            other_team = data["away_team"]

        dt_obj = datetime.fromisoformat(data["time"]["date"])
        date_str = dt_obj.strftime("%Y-%m-%d")
        time_str = dt_obj.strftime("%I:%M %p")

        game = (
            "Your favorite team "
            + clubs[count]
            + " will play against "
            + other_team
            + " on the "
            + date_str
            + " at "
            + time_str
            + ". "
            + " The game will be played in "
            + data["venue"]["city"]
            + " at the "
            + data["venue"]["name"]
            + ". "
        )

        count = count + 1
        answer += game

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


@app.route("/lookout")
def get_lookout():
    """Lookout duty endpoint.

    This endpoint provides the lookout duty use case information.

    Args:
        user: The username of the user. Only one username can be selected.

    Returns:
        The lookout duty information containing the events and sports fixtures.
    """

    if not request.args.get("user"):
        return jsonify({"error": "Missing parameters"}), 400

    user = request.args.get("user")

    user_preferences = get_user_preferences(user)
    user_location = user_preferences["location"]
    fotball_clubs = user_preferences["football_club"].split(",")
    football_ids = get_club_ids(fotball_clubs)
    artists = str(user_preferences["artists"].split(",")).replace("'", '"')
    enddate = "2023-06-01T14:00:00Z"

    events = get_events(user_location, artists, enddate)
    sports = get_sports(football_ids, fotball_clubs)

    name = "lookout"
    return jsonify({"_name": name, "events": events, "sports": sports})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5016, debug=True)

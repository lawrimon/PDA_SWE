from flask import Flask, jsonify, request
import requests, flask_cors
import json
from datetime import datetime

app = Flask(__name__)
flask_cors.CORS(app)

more_stocks = []
more_news = []


def get_club_shortcuts(club_names):
    clubs = {
        "Bayern München": "157",
        "Borussia Dortmund": "165",
        "VFB Stuttgart": "172",
        "Real Madrid": "541",
        "FC Barcelona": "529",
        "Manchester United": "33",
        "Paris Saint Germain": "85",
        "AC Milan": "489",
    }
    club_shortcuts = []
    for club_name in club_names:
        club_shortcuts.append(clubs.get(club_name, "Stock shortcut not found"))

    print(club_shortcuts, "club shortcuts")
    return club_shortcuts


def get_events(location, keyword_list, enddate):
    print(keyword_list, "keywordlist")
    params = {"location": location, "artists": keyword_list, "enddate": enddate}
    url = f"http://events:5000/events/all"
    response = requests.get(url, params)
    if response.status_code != 200:
        jsonify({"error": "Error getting weather information"}), 500
    try:
        event_list = ""
        data = response.json()
        for i in data:
            event_list += (
                "On the "
                + i["date"]
                + " in "
                + i["location"]
                + " you can see "
                + i["name"]
                + ". "
                + " The price is: "
                + i["price"]
                + " and the topic of the event is: "
                + i["topic"]
                + " ."
            )
        return event_list
    except Exception as e:
        print(e)


def get_sports(team_shortcuts, team_names):
    sport_news = ""
    count = 0
    print(team_names)
    for i in team_shortcuts:
        params = {"team": i}
        url = f"http://sports:5000/football/fixture"
        response = requests.get(url, params)
        if response.status_code != 200:
            jsonify({"error": "Error getting weather information"}), 500
        data = response.json()
        print(data)
        if team_names[count] == data["away_team"]:
            other_team = data["home_team"]
        else:
            other_team = data["away_team"]

        dt_obj = datetime.fromisoformat(data["time"]["date"])
        date_str = dt_obj.strftime("%Y-%m-%d")
        time_str = dt_obj.strftime("%I:%M %p")

        game = (
            "Your favorite team: "
            + team_names[count]
            + " is playing against: "
            + other_team
            + " on the: "
            + date_str
            + " at: "
            + time_str
            + " ."
        )

        count = count + 1
        sport_news += game

    return sport_news


def get_user_preferences(user):
    url = "http://db:5000/users/" + user

    response = requests.get(url)
    if response.status_code != 200:
        jsonify({"error": "Error getting stock news information"}), 500

    data = response.json()
    print(data)
    return data


@app.route("/lookout")
def get_scuttlebutt():
    try:
        user = request.args["user"]
    except:
        return jsonify("ERROR! : No User given!")

    user_pref = get_user_preferences(user)

    location_pref = user_pref["location"]
    print(user_pref["football_club"])

    footbal_pref = user_pref["football_club"].split(",")
    football_shortcuts = get_club_shortcuts(footbal_pref)

    artist_pref = str(user_pref["artists"].split(",")).replace("'", '"')

    print(artist_pref, "the artists")
    """
    Todo: Implement enddate logic:
    """
    enddate = "2023-05-01T14:00:00Z"

    print(artist_pref)
    print(location_pref)
    print(enddate)

    events = get_events(location_pref, artist_pref, enddate)
    sports = get_sports(football_shortcuts, footbal_pref)

    lookout_string = (
        "We have following events based on your favorite artists: "
        + events
        + " and following soccer games based on your preferences "
        + sports
        + "Thank you for listening. Do you want any additional information? "
    )

    return jsonify(lookout_string)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5016, debug=True)

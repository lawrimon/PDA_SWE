"""This application is the sports service.

The sports service is a service that provides fixture information for different sports.
Football and Formula 1 are supported. More sports will be added in the future.
The infomation is based on the services offered by API Sports.

Typical endpoints usage:
    GET /football/fixture?team=33
    GET /formulaone/fixture
"""

from flask import Flask, jsonify, request
import requests
import dotenv
import os

dotenv.load_dotenv()
SPORTS_API_KEY = os.getenv("SPORTS_API_KEY")

app = Flask(__name__)


@app.route("/football/fixture")
def get_football_fixture():
    """Football fixture endpoint.

    This endpoint provides information about the upcoming fixture for a given team.

    Args:
        team: The team ID of the team to get information for (e.g. 33 for Manchester United). See https://dashboard.api-football.com/soccer/ids/teams for a list of team IDs.

    Returns:
        Information about the upcoming fixture for the given team.
    """

    if request.args.get("team") is None:
        return jsonify({"error": "Missing parameters"}), 400
    
    if not request.args.get("team").isnumeric():
        return jsonify({"error": "Invalid parameters"}), 400

    team = request.args.get("team")
    next = 1
    timezone = "Europe/Berlin"

    url = f"https://v3.football.api-sports.io/fixtures"
    params = {
        "team": team,
        "next": next,
        "timezone": timezone,
    }
    headers = {
        "x-apisports-key": SPORTS_API_KEY,
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Error getting football fixtures information"}), 500

    data = response.json()

    fixture = {
        "home_team": data["response"][0]["teams"]["home"]["name"],
        "away_team": data["response"][0]["teams"]["away"]["name"],
        "venue": {
            "name": data["response"][0]["fixture"]["venue"]["name"],
            "city": data["response"][0]["fixture"]["venue"]["city"],
        },
        "league": {
            "name": data["response"][0]["league"]["name"],
            "country": data["response"][0]["league"]["country"],
        },
        "time": {
            "date": data["response"][0]["fixture"]["date"],
            "timestamp": data["response"][0]["fixture"]["timestamp"],
            "timezone": data["response"][0]["fixture"]["timezone"],
        },
    }

    return jsonify(fixture)

@app.route("/formulaone/fixture")
def get_formulaone_fixture():
    """Formula 1 fixture endpoint.

    This endpoint provides information about the upcoming Formula 1 fixture.

    Returns:
        Information about the upcoming fixture.
    """

    next = 1
    timezone = "Europe/Berlin"
    type = "Race"

    url = f"https://v1.formula-1.api-sports.io/races"
    params = {
        "next": next,
        "timezone": timezone,
        "type": type,
    }
    headers = {
        "x-apisports-key": SPORTS_API_KEY,
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Error getting football fixtures information"}), 500

    data = response.json()

    fixture = {
        "name": data["response"][0]["competition"]["name"],
        "type": data["response"][0]["type"],
        "venue": {
            "name": data["response"][0]["circuit"]["name"],
            "country": data["response"][0]["competition"]["location"]["country"],
            "city": data["response"][0]["competition"]["location"]["city"],
        },
        "time": {
            "date": data["response"][0]["date"],
            "timezone": data["response"][0]["timezone"],
        },
    }

    return jsonify(fixture)
"""This application is the wisdom service.

The wisdom service provides endpoints for wisdom information like quotes, random facts and astronomy picture of the day.
The quotes and random facts are based on API Ninjas. The astronomy picture of the day is based on the NASA API.

Typical endpoints usage:

    GET /wisdom/random_facts
    GET /wisdom/quotes
    GET /wisdom/apod
"""

from flask import Flask, jsonify, request
import requests
import dotenv
import os

dotenv.load_dotenv()
NINJAS_API_KEY = os.getenv("NINJAS_API_KEY")
NASA_API_KEY = os.getenv("NASA_API_KEY")

app = Flask(__name__)


@app.route("/wisdom/random_facts")
def get_random_facts():
    """Random facts endpoint.

    This endpoint provides random facts.

    Returns:
        Several random facts.
    """

    url = f"https://api.api-ninjas.com/v1/facts"
    params = {
        "limit": 5,
    }
    headers = {
        "X-Api-Key": NINJAS_API_KEY,
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Error getting random facts information"}), 500

    data = response.json()

    return jsonify(data)


@app.route("/wisdom/quotes")
def get_quotes():
    """Quotes endpoint.

    This endpoint provides quotes for different categories.

    Returns:
        Several quotes for a random category.
    """

    url = f"https://api.api-ninjas.com/v1/quotes"
    params = {
        "limit": 5,
    }
    headers = {
        "X-Api-Key": NINJAS_API_KEY,
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Error getting quotes information"}), 500

    data = response.json()

    return jsonify(data)


@app.route("/wisdom/apod")
def get_apod():
    """Astronomy picture of the day endpoint.

    This endpoint provides the astronomy picture of the day.

    Returns:
        The astronomy picture of the day and background information.
    """

    url = f"https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": NASA_API_KEY,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return (
            jsonify(
                {"error": "Error getting astronomy picture of the day information"}
            ),
            500,
        )

    data = response.json()

    return jsonify(data)

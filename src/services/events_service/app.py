"""This application is the events service.

The events service provides an endpoint to get event information.
The functionality is based on the Ticketmaster API.

Typical endpoints usage:

    GET /events/location?location=location&enddate=enddate
    GET /events/artists?artists=artists&enddate=enddate
    GET /events/all?location=location&artists=artists&enddate=enddate
"""



from flask import Flask, jsonify, request
import requests
import dotenv
import time
import os
import json
from typing import Dict, List, Optional

app = Flask(__name__)

dotenv.load_dotenv()
EVENTS_API_KEY = os.getenv("EVENTS_API_KEY")


def missing_route_parameters(route_params: Dict) -> bool:
    """
    Returns True if required parameters are missing from the route params.
    """
    required_params = {
        "/events/location": ["location", "enddate"],
        "/events/artists": ["artists", "enddate"],
        "/events/all": ["location", "artists", "enddate"],
    }
    
    route_path = request.path
    missing_params = [p for p in required_params[route_path] if p not in route_params]

    if missing_params:
        print(f"Missing route parameters: {missing_params}")
        return True
    return False


def invalid_route_parameters(route_params: Dict) -> bool:
    """
    Returns True if any of the route params are invalid.
    """
    for param, value in route_params.items():
        if not value:
            print(f"Invalid route parameter '{param}': {value}")
            return True
    return False


@app.route("/events/location")
def get_events_location():
    """Event location endpoint.

    This endpoint provides the current events based on location.

    Args:
        Location: The location where the event is
        Enddate: The latest date of an event

    Returns:
        Events based on the location
    """
    if missing_route_parameters(request.args):
        return jsonify({"error": "Missing route parameters"}), 400
    if invalid_route_parameters(request.args):
        return jsonify({"error": "Invalid route parameters"}), 400
    events = []

    location = request.args.get("location")
    enddate = request.args.get("enddate")
    try:
        url = f"https://app.ticketmaster.com/discovery/v2/events.json"
        params = {"apikey": EVENTS_API_KEY, "city": location, "endDateTime": enddate}

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return jsonify({"error": "Error getting user location information"}), 500

        data = response.json()
        event_list = data["_embedded"]["events"]
        for i in event_list:
            try:
                event = {
                    "name": i["name"],
                    "date": i["dates"]["start"]["localDate"],
                    "topic": i["classifications"][0]["segment"]["name"],
                    "price": str(i["priceRanges"][0]["min"]),
                    "location": i["_embedded"]["venues"][0]["city"]["name"],
                }
                events.append(event)
            except:
                pass
        return events

    except Exception as e:
        print(e)


@app.route("/events/artists")
def get_events_artists():
    """Artist endpoint.

    This endpoint provides events based on artists

    Args:
        Artists: Artists that were set in preferences
        
    Returns:
        The event information.
    """

    if missing_route_parameters(request.args):
        return jsonify({"error": "Missing route parameters"}), 400
    if invalid_route_parameters(request.args):
        return jsonify({"error": "Invalid route parameters"}), 400

    keyword_list = request.args.get("artists")
    if keyword_list is None:
        return jsonify({"error": "Missing artists parameter"}), 400
    keyword_list = json.loads(keyword_list)
    enddate = request.args.get("enddate")
    events = []
    try:
        for keyword in keyword_list:
            url = f"https://app.ticketmaster.com/discovery/v2/events.json"
            params = {
                "apikey": EVENTS_API_KEY,
                "keyword": keyword,
                "endDateTime": enddate,
            }
            response = requests.get(url, params=params)
            if response.status_code != 200:
                return (
                    jsonify({"error": "Error getting user location information"}),
                    500,
                )
            data = response.json()
            event_list = data["_embedded"]["events"]
            for i in event_list:
                event = {
                    "name": i["name"],
                    "date": i["dates"]["start"]["localDate"],
                    "topic": i["classifications"][0]["segment"]["name"],
                    "price": str(i["priceRanges"][0]["min"]),
                    "location": i["_embedded"]["venues"][0]["city"]["name"],
                }
                events.append(event)

        return events

    except Exception as e:
        print(e)
        return None


@app.route("/events/all")
def get_events():
    """Event location and artist

    This endpoint provides the current events based on location and artsits.
    
    Args: 
        Location: The location where the event is
        Enddate: The latest date of an event
        Artists: Artists that were set in preferences

    Returns:
        Events based on preferences

    """
    if missing_route_parameters(request.args):
        return jsonify({"error": "Missing route parameters"}), 400
    if invalid_route_parameters(request.args):
        return jsonify({"error": "Invalid route parameters"}), 400

    events = []

    location = request.args.get("location")
    keyword_list = request.args.get("artists")
    keyword_list = json.loads(keyword_list)
    enddate = request.args.get("enddate")
    events = []
    try:
        for keyword in keyword_list:
            url = f"https://app.ticketmaster.com/discovery/v2/events.json"
            params = {
                "apikey": EVENTS_API_KEY,
                "city": location,
                "keyword": keyword,
                "endDateTime": enddate,
            }

            response = requests.get(url, params=params)
            if response.status_code != 200:
                return (
                    jsonify({"error": "Error getting user location information"}),
                    500,
                )

            data = response.json()
            event_list = data["_embedded"]["events"]
            for i in event_list:
                event = {
                    "name": i["name"],
                    "date": i["dates"]["start"]["localDate"],
                    "topic": i["classifications"][0]["segment"]["name"],
                    "price": str(i["priceRanges"][0]["min"]),
                    "location": i["_embedded"]["venues"][0]["city"]["name"],
                }
                events.append(event)

        return events

    except Exception as e:
        print(e)
        return jsonify({"error": "Error getting user location information"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5014, debug=True)

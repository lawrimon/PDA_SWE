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


@app.route("/events/location")
def get_events_location():
    """Event endpoint based on location.

    This endpoint provides the current events based on the location

    Args:
        location: The location of the event.
        enddate: The end date of the event search.

    Returns:
        Information about the found events.
    """

    if missing_event_parameters(request.args):
        return jsonify({"error": "Missing parameters"}), 400
    
    if invalid_event_parameters(request.args):
        return jsonify({"error": "Invalid  parameters"}), 400
    

    location = request.args.get("location")
    enddate = request.args.get("enddate")

    events = []
    try:
        url = f"https://app.ticketmaster.com/discovery/v2/events.json"
        params = {"apikey": EVENTS_API_KEY, "city": location, "endDateTime": enddate}

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return jsonify({"error": "Error getting event information"}), 500

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
        return jsonify({"error": "Error getting event information"}), 500


@app.route("/events/artists")
def get_events_artists():
    """Artist endpoint based on artists.

    This endpoint provides events based on artists.

    Args:
        artists: The artists of the event.
        enddate: The end date of the event search.
        
    Returns:
        Information about the found events.
    """

    if missing_event_parameters(request.args):
        return jsonify({"error": "Missing parameters"}), 400
    
    if invalid_event_parameters(request.args):
        return jsonify({"error": "Invalid parameters"}), 400

    keyword_list = request.args.get("artists")
    
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
                    jsonify({"error": "Error getting event information"}),
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
        return jsonify({"error": "Error getting event information"}), 500


@app.route("/events/all")
def get_events():
    """Event endpoint based on location and artists.

    This endpoint provides events based on the location and artists.
    
    Args: 
        location: The location of the event.
        artists: The artists of the event.
        enddate: The end date of the event search.

    Returns:
        Information about the found events.
    """

    if missing_event_parameters(request.args):
        return jsonify({"error": "Missing parameters"}), 400
    if invalid_event_parameters(request.args):
        return jsonify({"error": "Invalid parameters"}), 400

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
                    jsonify({"error": "Error getting evemt information"}),
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
        return jsonify({"error": "Error getting event information"}), 500


def missing_event_parameters(event_params: Dict) -> bool:
    """Check if the required event parameters are missing.

    Args:
        args: The request arguments.

    Returns:
        True if a required parameter is missing, False otherwise.
    """

    required_params = {
        "/events/location": ["location", "enddate"],
        "/events/artists": ["artists", "enddate"],
        "/events/all": ["location", "artists", "enddate"],
    }
    
    route_path = request.path
    missing_params = [p for p in required_params[route_path] if p not in event_params]

    if missing_params:
        print(f"Missing parameters: {missing_params}")
        return True
    
    return False


def invalid_event_parameters(event_params: Dict) -> bool:
    """Check if the required route parameters are missing.

    Args:
        args: The request arguments.

    Returns:
        True if a required parameter is missing, False otherwise.
    
    """

    for param, value in event_params.items():
        if not value:
            print(f"Invalid parameters: '{param}': {value}")
            return True
        
    return False

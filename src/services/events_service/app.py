"""This application is the events service.

The events service provides an endpoint to get event information.
The functionality is based on the ticketmaster API.

Typical endpoints usage:

    GET /artist_event
    GET https://app.ticketmaster.com/discovery/v2/events.json?apikey=&city=Stuttgart&keyword=Avril Lavigne
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
    Returns True if required parameters are missing from the route params 
    """
    required_params = {
        "/events/location": ["location", "enddate"],
        "/events/artists": ["artists", "enddate"],
        "/events/all": ["location", "artists", "enddate"]
    }

    route_path = request.path
    missing_params = [p for p in required_params[route_path] if p not in route_params]

    if missing_params:
        print(f"Missing route parameters: {missing_params}")
        return True
    return False


def invalid_route_parameters(route_params: Dict) -> bool:
    """
    Returns True if any of the route params are invalid
    """
    for param, value in route_params.items():
        if not value:
            print(f"Invalid route parameter '{param}': {value}")
            return True
    return False


def missing_query_parameters(query_params: Dict, required_params: List[str]) -> bool:
    """Returns True if required parameters are missing from the query string"""
    missing_params = [p for p in required_params if p not in query_params]
    if missing_params:
        print(f"Missing query parameters: {missing_params}")
        return True
    return False


def invalid_query_parameters(query_params: Dict, valid_params: List[str]) -> bool:
    """Returns True if any of the query params are invalid"""
    for param, value in query_params.items():
        if param not in valid_params:
            print(f"Invalid query parameter '{param}': {value}")
            return True
    return False



@app.route("/events/location")
def get_events_location():
    """Event location endpoint.

    This endpoint provides the current events based on location.

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
        params = {
            "apikey": EVENTS_API_KEY,
            "city": location,
            "endDateTime": enddate
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print (response.json())
            return jsonify({"error": "Error getting user location information"}), 500

        data = response.json()
        #print(data)
        event_list = data["_embedded"]["events"]
        print("here")
        for i in event_list:
            try: 
                event = {"name" :i["name"], 
                         "date" :i["dates"]["start"]["localDate"], 
                         "topic": i["classifications"][0]["segment"]["name"],
                          "price" : str(i["priceRanges"][0]["min"]), 
                          "location" : i["_embedded"]["venues"][0]["city"]["name"]}
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

    Returns:
        The event information.
    

    if missing_route_parameters(request.args):
        return jsonify({"error": "Missing parameters"}), 400

    if invalid_route_parameters(request.args):
        return jsonify({"error": "Invalid parameters"}), 400
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
    print(keyword_list, "keywordlist")
    print(enddate, "enddate")
    print(EVENTS_API_KEY,"APIKEY")
    events =[]
    try: 
        for keyword in keyword_list:
            print("keyword",keyword)
            url = f"https://app.ticketmaster.com/discovery/v2/events.json"
            params = {
                "apikey": EVENTS_API_KEY,
                "keyword": keyword,
                "endDateTime": enddate
            }
            print("before request")
            response = requests.get(url, params=params)
            print(response)
            if response.status_code != 200:
                return jsonify({"error": "Error getting user location information"}), 500
            print("lol")
            data = response.json()
            print("this data",data)
            event_list = data["_embedded"]["events"]
            for i in event_list:
                
                event = {"name" :i["name"], 
                         "date" :i["dates"]["start"]["localDate"], 
                         "topic": i["classifications"][0]["segment"]["name"],
                          "price" : str(i["priceRanges"][0]["min"]), 
                          "location" : i["_embedded"]["venues"][0]["city"]["name"]}
                events.append(event)

        return events

    except Exception as e:  
        print(e)
        return None

@app.route("/events/all")
def get_events():
    """Event location and artist

    This endpoint provides the current events based on location and artsits.

    Returns:
        Events based on preferences
   
    """
    if missing_route_parameters(request.args):
        return jsonify({"error": "Missing route parameters"}), 400
    if invalid_route_parameters(request.args):
        return jsonify({"error": "Invalid route parameters"}), 400

    events = []

    location = request.args.get("city")
    keyword_list = request.args.get("artists")
    keyword_list = json.loads(keyword_list)
    enddate = request.args.get("enddate")
    events =[]
    try: 
        for keyword in keyword_list:
            url = f"https://app.ticketmaster.com/discovery/v2/events.json"
            params = {
                "apikey": EVENTS_API_KEY,
                "city": location,
                "keyword": keyword,
                "endDateTime": enddate
            }

            response = requests.get(url, params=params)
            if response.status_code != 200:
                return jsonify({"error": "Error getting user location information"}), 500

            data = response.json()
            event_list = data["_embedded"]["events"]
            for i in event_list:
                event = {"name" :i["name"], 
                         "date" :i["dates"]["start"]["localDate"], 
                         "topic": i["classifications"][0]["segment"]["name"],
                          "price" : str(i["priceRanges"][0]["min"]), 
                          "location" : i["_embedded"]["venues"][0]["city"]["name"]}
                events.append(event)

        return events

    except Exception as e:  
        print(e)
        return jsonify({"error": "Error getting user location information"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5014, debug=True)




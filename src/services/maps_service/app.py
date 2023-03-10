"""This application is the maps service.

The maps service provides an endpoint to get the current user location.
It also provides an endpoint to get the route between a origin and a destination.
The functionality is based on the Google Maps Platform.
"""

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

#TODO: add api key
API_KEY = ""


@app.route("/user_location")
def get_user_location():
    """User location endpoint.

    This endpoint provides the current user location.

    Returns:
        Latitude and longitude of the current user location.
    """

    url = f"https://www.googleapis.com/geolocation/v1/geolocate"
    params = {
        "key": API_KEY,
    }

    response = requests.post(url, params=params)
    if response.status_code != 200:
        jsonify({"error": "Error getting user location information"}), 500

    data = response.json()
    user_location = {"lat": data["location"]["lat"], "lon": data["location"]["lng"]}

    return jsonify(user_location)


@app.route("/route")
def get_route():
    """Route endpoint.

    This endpoint provides the route from a origin to a destination.

    Args:
        origin: The origin of the route as coordinates.
        destination: The destination of the route as coordinates.
        mode: The mode of transportation. Can be "driving", "walking", "bicycling" or "transit".
        
    Returns:
        The route information. This includes the navigation steps, distance and duration.
    """

    if missing_route_parameters(request.args):
        return jsonify({"error": "Missing parameters"}), 400

    if invalid_route_parameters(request.args):
        return jsonify({"error": "Invalid parameters"}), 400

    origin = request.args.get("origin")
    destination = request.args.get("destination")
    mode = request.args.get("mode")
    units = "metric"

    url = f"https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "units": units,
        "key": API_KEY,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        jsonify({"error": "Error getting route information"}), 500

    data = response.json()

    route = data["routes"][0]["legs"][0]

    return jsonify(route)


def is_valid_coordinates_string(coordinates_string):
    """Check if a string is a valid coordinates string.

    Args:
        coordinates_string: The coordinates string to check.

    Returns:
        True if the string is a valid coordinates string, False otherwise.
    """

    coordinates = coordinates_string.split(",")
    if len(coordinates) != 2:
        return False

    try:
        lat = float(coordinates[0])
        lon = float(coordinates[1])
    except ValueError:
        return False

    if lat < -90 or lat > 90 or lon < -180 or lon > 180:
        return False

    return True


def missing_route_parameters(args):
    """Check if the required route parameters are missing.

    Args:
        args: The request arguments.

    Returns:
        True if a required parameter is missing, False otherwise.
    """

    if not args.get("origin") or not args.get("destination") or not args.get("mode"):
        return True

    return False


def invalid_route_parameters(args):
    """Check if the route parameters are invalid.

    Args:
        args: The request arguments.

    Returns:
        True if a parameter is invalid, False otherwise.
    """

    if (
        not is_valid_coordinates_string(args.get("origin"))
        or not is_valid_coordinates_string(args.get("destination"))
        or not args.get("mode") in ["driving", "walking", "bicycling", "transit"]
    ):
        return True

    return False

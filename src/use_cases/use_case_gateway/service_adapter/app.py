import requests
from flask import Flask, jsonify

app = Flask(__name__)

use_mock = True

# Mock data

# Fetch data from external API
location_data = {"latitude": 37.7749, "longitude": -122.4194}
event_data = [
    {"name": "Music Festival", "time": "2023-05-01T12:00:00.000000Z"},
    {"name": "Art Exhibition", "time": "2023-05-02T10:00:00.000000Z"},
    {"name": "Food Festival", "time": "2023-05-03T18:00:00.000000Z"},
]
appointment_data = [
    {"name": "Doctor Appointment", "time": "2023-05-02T14:00:00.000000Z"},
    {"name": "Meeting with Boss", "time": "2023-05-03T16:00:00.000000Z"},
]


@app.route("/location/<user_id>")
def get_user_location(user_id):
    # Testing only!
    if use_mock:
        return location_data

    # assuming there is a location API that returns user location based on user_id
    response = requests.get(f"https://location-api.com/user/{user_id}")
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"message": "User location not found"}), 404


@app.route("/appointments/<user_id>")
def get_user_appointments(user_id):
    # Testing only!
    if use_mock:
        return jsonify({"data": appointment_data})

    # assuming there is an appointments API that returns user appointments based on user_id
    response = requests.get(f"https://appointments-api.com/user/{user_id}")
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"message": "User appointments not found"}), 404


@app.route("/events/<location>")
def get_events(location):
    # Testing only!
    if use_mock:
        return jsonify({"data": event_data})

    # assuming there is an events API that returns events based on location
    response = requests.get(f"https://events-api.com/location/{location}")
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"message": "No events found in this location"}), 404


if __name__ == "__main__":
    app.run(debug=True)

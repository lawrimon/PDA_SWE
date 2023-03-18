"""This application is weather service.

The weather service is a service that provides weather information for a given location.
It provides an endpoint to get the weather information for a given location for the next day.
The functionality is based in the OpenWeatherMap API.
"""

from flask import Flask, jsonify, request
import requests
import dotenv
import os

dotenv.load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

app = Flask(__name__)


@app.route('/weather')
def get_weather():
    """Weather information endpoint.

    This endpoint provides weather information for a given location for the next day.

    Args:
        lat: The latitude of the location.
        lon: The longitude of the location.

    Returns:
        The weather information for the next day for the given location.
    """

    if not request.args.get('lat') or not request.args.get('lon'):
        return jsonify({'error': 'Missing parameters'}), 400
    
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    cnt = 1
    units = 'metric'
    api_key = WEATHER_API_KEY

    url = f'https://api.openweathermap.org/data/2.5/forecast/daily'
    params = {
        'lat': lat,
        'lon': lon,
        'cnt': cnt,
        'units': units,
        'appid': api_key
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        jsonify({'error': 'Error getting weather information'}), 500

    data = response.json()

    print(data)

    return jsonify(data)

if __name__ == "__main__":
    app.run()

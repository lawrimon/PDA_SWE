"""This application is weather service.

The weather service is a service that provides weather information for a given location.
It provides an endpoint to get the weather information for a given location for the next day.
The functionality is based in the OpenWeatherMap API.
"""

from flask import Flask, jsonify, request
import requests

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
    
    api_key = '10245a3d06eb6a826ddc1bfa3d943829'
    lat = 51.5074
    lon = 0.1278 
    url = f'api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt={1}&appid={api_key}'

    response = requests.get(url)
    if response.status_code != 200:
        jsonify({'error': 'Error getting weather information'}), 500

    data = response.json()

    return jsonify(data)

if __name__ == '__main__':
    app.run()
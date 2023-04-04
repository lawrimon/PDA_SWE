from flask import Flask, jsonify, request
import requests
import dotenv
import os

dotenv.load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

app = Flask(__name__)


@app.route("/usecaseweather")
def get_weather():
    url = f"http://weather-service/weather?lat=40.416775&lon=3.703790"

    response = requests.get(url)
    if response.status_code != 200:
        jsonify({"error": "Error getting weather information"}), 500

    data = response.json()

    print(data)

    return jsonify(data)


if __name__ == "__main__":
    app.run()


from flask import Flask, jsonify, request
import requests
import dotenv
import os

dotenv.load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

app = Flask(__name__)



def get_weather():

    url = f"http://weather-service/weather?lat=40.416775&lon=3.703790"

    response = requests.get(url)
    if response.status_code != 200:
        jsonify({"error": "Error getting weather information"}), 500

    data = response.json()

    max_temp = data["list"]["temp"]["max"]
    min_temp = data["list"]["temp"]["min"]
    description = data["list"]["weather"]["description"]
    
    Answer = "The maximum temperature today is" + max_temp + "and the minimum temperature is " + min_temp + ". The weather today is looking like" + description
    
    print(Answer)
    return Answer


def get_news(user_pref):
    
    url = f"http://127.0.0.1:5000/tagesschau/homepage"

    response = requests.get(url)
    if response.status_code != 200:
        jsonify({"error": "Error getting weather information"}), 500

    data = response.json()
    print(data)

    return data

def get_stocks(user_pref):
    
    symbol_list = user_pref
    url = "/quotes" 
    params = {
        "symbols": symbol_list
    }
    
    response = requests.get(url ,params)
    if response.status_code != 200:
        jsonify({"error": "Error getting weather information"}), 500

    data = response.json()
    print(data)

    return data



@app.route("/scuttlebutt")
def get_scuttlebutt():
    news = get_news()
    print("news----",news)
    weather = get_weather()
    print("weather----",weather)
    stocks = get_stocks()
    print("stocks----",weather)


    return jsonify(news, weather)
  
  

if __name__ == "__main__":
    app.run()

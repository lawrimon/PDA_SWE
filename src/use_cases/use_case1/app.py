from flask import Flask, jsonify, request
import requests
import dotenv
import os


from flask import Flask, jsonify, request
import requests
import dotenv
import os

dotenv.load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

app = Flask(__name__)


def get_weather():

    '''
    TODO:
    Implement UserID Logic to get User Location
    '''
    user_location = {"lat":"50", "lon":"30"}
    params = {
        "lat": user_location["lat"],
        "lon": user_location["lon"]
    }
    url = f"http://127.0.0.1:5002/weather"
    response = requests.get(url, params)
    if response.status_code != 200:
        jsonify({"error": "Error getting weather information"}), 500

    data = response.json()
    print(data)
    
    max_temp = data["list"][0]["temp"]["max"]
    min_temp = data["list"][0]["temp"]["min"]
    description = data["list"][0]["weather"][0]["description"]
    
    Answer = "The maximum temperature today is " + str(max_temp) + " and the minimum temperature is " + str(min_temp) + " . The weather today is looking like " + description
    
    print(Answer)
    return Answer


def get_news():
    
    url = f"http://127.0.0.1:5005/tagesschau/homepage"

    response = requests.get(url)
    if response.status_code != 200:
        jsonify({"error": "Error getting weather information"}), 500

    data = response.json()
    compromised_data = []
    print(data)
    compromised_data.append(data[0]["Summary"]) 
    compromised_data.append(data[1]["Summary"]) 

    Answer = "These are the headline storys for the day : " + str(compromised_data[0]) + " Nächster Artikel " + str(compromised_data[1]) 

    return Answer

def get_stocks():
    
    symbols = ["IBM,MSFT,GOOG"]
    
    url = "http://127.0.0.1:5001/quotes" 

    params = {
        "symbols": symbols
    }
    
    response = requests.get(url ,params)
    if response.status_code != 200:
        jsonify({"error": "Error getting stock service information"}), 500  

    data = response.json()
    print(data)

    return data

def get_stock_news():
    
    symbols = ["IBM,MSFT,GOOG"]
    
    url = "http://127.0.0.1:5001/news"

    params = {
        "symbols": symbols
    }

    response = requests.get(url ,params)
    if response.status_code != 200:
        jsonify({"error": "Error getting stock news information"}), 500

    data = response.json()
    print(data)

    answer = "These are the latest news for the stocks you are interested in : " + data[symbols.split(",")[0]][0]["headline"] + " " + data[symbols.split(",")[0]][0]["summary"]

    return answer

@app.route("/scuttlebutt")
def get_scuttlebutt():
    print("lol")
    news = get_news()
    print("news----",news)
    weather = get_weather()
    print("weather----",weather)
    stock_news = get_stock_news()
    print("stock_news----",stock_news)
    #stocks = get_stocks()
    #print("stocks----",stocks)


    return jsonify(news, weather, stock_news)
  
  

if __name__ == "__main__":
    app.run()

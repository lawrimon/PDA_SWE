from flask import Flask, jsonify, request
import requests, flask_cors
from googletrans import Translator


app = Flask(__name__)
flask_cors.CORS(app)

more_stocks = []
more_news = []


def get_weather():
    """
    TODO:
    Implement UserID Logic to get User Location
    """
    user_location = {"lat": "50", "lon": "30"}
    params = {"lat": user_location["lat"], "lon": user_location["lon"]}
    url = f"http://weather:5000/weather"
    response = requests.get(url, params)
    if response.status_code != 200:
        jsonify({"error": "Error getting weather information"}), 500

    data = response.json()

    max_temp = data["list"][0]["temp"]["max"]
    min_temp = data["list"][0]["temp"]["min"]
    description = data["list"][0]["weather"][0]["description"]

    Answer = (
        "The maximum temperature today is "
        + str(max_temp)
        + " and the minimum temperature is "
        + str(min_temp)
        + " . The weather today is looking like "
        + description
    )

    print(Answer)
    return Answer


def get_news():
    url = f"http://news:5000/tagesschau/homepage"

    response = requests.get(url)
    if response.status_code != 200:
        jsonify({"error": "Error getting weather information"}), 500

    data = response.json()
    compromised_data = []
    compromised_data.append(data[0]["Summary"])
    compromised_data.append(data[1]["Summary"])
    compromised_data.append(data[2]["Summary"])
    compromised_data.append(data[3]["Summary"])


    translator = Translator()

    german_text = compromised_data[0]
    compromised_data[0] = translator.translate(german_text, src='de', dest='en').text
    german_text = compromised_data[1]
    compromised_data[1] = translator.translate(german_text, src='de', dest='en').text


    german_text = compromised_data[2]
    compromised_data[2] = translator.translate(german_text, src='de', dest='en').text
    german_text = compromised_data[3]
    compromised_data[3] = translator.translate(german_text, src='de', dest='en').text

    more_news.append(compromised_data[2])
    more_news.append(compromised_data[3])


    Answer = (
        "These are the headline storys for the day : "
        + str(compromised_data[0])
        + " Here is your next Article: "
        + str(compromised_data[1])
        
    )

    return Answer


def get_stocks():
    symbols = ["IBM,MSFT,GOOG"]

    url = "http://stockmarket:5000/quotes"

    params = {"symbols": symbols}

    response = requests.get(url, params)
    if response.status_code != 200:
        jsonify({"error": "Error getting stock service information"}), 500

    data = response.json()

    return data


def get_stock_news():
    symbols = "MSFT,GOOG,IBM"

    url = "http://stockmarket:5000/news"

    params = {"symbols": symbols}

    response = requests.get(url, params)
    if response.status_code != 200:
        jsonify({"error": "Error getting stock news information"}), 500

    data = response.json()

    answer = (
        "These are the latest news for the stocks you are interested in : "
        + data[symbols.split(",")[0]][0]["headline"]
        + " "
        + data[symbols.split(",")[0]][0]["summary"]
    )

    return answer


@app.route("/scuttlebutt")
def get_scuttlebutt():
    print("lol")
    news = get_news()
    print("news----", news)
    weather = get_weather()
    print("weather----", weather)
    stock_news = get_stock_news()
    print("stock_news----", stock_news)
    # stocks = get_stocks()
    # print("stocks----",stocks)

    return jsonify(news, weather, stock_news, "Thank you for listening. Do you want any additional information? ")



@app.route("/scuttlebutt/additional")
def get_more_scuttlebutt():
    print("lol")
    news = more_news
    print("news----", news)

    return jsonify(news)


if __name__ == "__main__":
    app.run()

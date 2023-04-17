from flask import Flask, jsonify, request
import requests, flask_cors
from googletrans import Translator


app = Flask(__name__)
flask_cors.CORS(app)

more_stocks = []
more_news = []


def get_weather(coords):
    """
    TODO:
    Implement UserID Logic to get User Location
    """
    print(coords, "COOORDS")
    user_location = {"lat": coords[0], "lon": coords[1]}
    print("we HERE", user_location)
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


def get_news(pref):
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
    compromised_data[0] = translator.translate(german_text, src="de", dest="en").text
    german_text = compromised_data[1]
    compromised_data[1] = translator.translate(german_text, src="de", dest="en").text

    german_text = compromised_data[2]
    compromised_data[2] = translator.translate(german_text, src="de", dest="en").text
    german_text = compromised_data[3]
    compromised_data[3] = translator.translate(german_text, src="de", dest="en").text

    more_news.append(compromised_data[2])
    more_news.append(compromised_data[3])

    Answer = (
        "These are the headline storys for the day : "
        + str(compromised_data[0])
        + " Here is your next Article: "
        + str(compromised_data[1])
    )

    return Answer


def get_stocks(pref):
    symbols = ["IBM,MSFT,GOOG"]

    url = "http://stockmarket:5000/quotes"

    params = {"symbols": symbols}

    response = requests.get(url, params)
    if response.status_code != 200:
        jsonify({"error": "Error getting stock service information"}), 500

    data = response.json()

    return data


def get_stock_shortcuts(company_names):
    stocks = {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Alphabet": "GOOG",
        "Amazon": "AMZN",
        "NVIDIA": "NVDA",
        "Tesla": "TSLA",
        "TSMC": "TSM",
        "Ford": "F",
    }
    stock_shortcuts = []
    for company_name in company_names:
        stock_shortcuts.append(stocks.get(company_name, "Stock shortcut not found"))

    stock_shortcuts = ",".join(stock_shortcuts)

    return stock_shortcuts


def get_stock_news(pref):
    symbols = get_stock_shortcuts(pref)
    print(symbols)

    url = "http://stockmarket:5000/news"

    params = {"symbols": symbols}

    response = requests.get(url, params)
    if response.status_code != 200:
        jsonify({"error": "Error getting stock news information"}), 500

    data = response.json()

    news = []
    # iterate over every symbol
    for symbol in symbols.split(","):
        # check if there is a news article for the symbol
        if len(data[symbol]) > 0:
            # get the first article
            news_string = (
                symbol
                + ": "
                + data[symbol][0]["headline"]
                + " "
                + data[symbol][0]["summary"]
            )
            news.append(news_string)

    # if there is no news, return an empty string
    if len(news) == 0:
        answer = "There is no news for the stocks you are interested in."
    else:
        answer = "Here are the news for the stocks you are interested in: " + " ".join(
            news
        )

    return answer


def get_user_preferences(user):
    url = "http://db:5000/users/" + user

    response = requests.get(url)
    if response.status_code != 200:
        jsonify({"error": "Error getting stock news information"}), 500

    data = response.json()
    print(data)
    return data


@app.route("/scuttlebutt")
def get_scuttlebutt():
    try:
        user = request.args["user"]
    except:
        return jsonify("ERROR! : No User given!")

    print("-----")
    user_pref = get_user_preferences(user)

    news_pref = user_pref["news"].split(",")
    stock_pref = user_pref["stocks"].split(",")
    user_coords = user_pref["coordinates"].split(",")
    print(user_coords, "COOORDS")
    user_location = {"lat": user_coords[0], "lon": user_coords[1]}
    print("we HERE", user_location)

    print("lol", user)
    """
     user_pref = ""
    news_pref = ""
    user_coords = ["30,30"]
    stock_pref = ["Apple"]
    """

    news = get_news(news_pref)
    print("news----", news)
    weather = get_weather(user_coords)
    print("weather----", weather)
    stock_news = get_stock_news(stock_pref)
    print("stock_news----", stock_news)
    # stocks = get_stocks()
    # print("stocks----",stocks)

    # artist = "RIN"
    # track = "Sternenstaub"
    # music_url = "http://music:5000/music"
    # params = {"artist": artist, "track": track}
    # music_response = requests.get(music_url, params)
    # if music_response.status_code != 200:
    #     return jsonify({"error": "Error playing music"}), 500

    return jsonify({
        "news":news,
        "weather":weather,
        "stock_news":stock_news,
        "outro": "Thank you for listening. Do you want any additional information? ",
    })


@app.route("/scuttlebutt/additional")
def get_more_scuttlebutt():
    print("lol")
    news = more_news
    print("news----", news)

    return jsonify(news)


if __name__ == "__main__":
    app.run()

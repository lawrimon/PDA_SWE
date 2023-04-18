"""This application is the scuttlebutt use case.

Every day at 8.15 PM the scuttlebutt use case provides the user with some news, weather and stock market information.

Example Usage:

    GET /scuttlebutt?user=cr7thegoat
"""


from flask import Flask, jsonify, request
import requests, flask_cors
from googletrans import Translator


app = Flask(__name__)
flask_cors.CORS(app)

more_news = []

def get_weather(user_coordinates):
    """Get weather.

    This functions calls the weather endpoint of the weather service and returns the weather for the given coordinates.

    Args:
        user_coordinates: The coordinates of the user. Only one set of coordinates can be selected.

    Returns:
        Information about the weather for the given coordinates or an explanatory string if no weather information could be retrieved.
    """

    # TODO: Why this instead of just passing the coordinates?
    user_location = {"lat": user_coordinates[0], "lon": user_coordinates[1]}

    url = f"http://weather:5000/weather"
    params = {"lat": user_location["lat"], "lon": user_location["lon"]}
    response = requests.get(url, params)
    if response.status_code != 200:
        return "No weather information found for the provided coordinates."
        # jsonify({"error": "Error getting weather information"}), 500

    data = response.json()
    max_temp = data["list"][0]["temp"]["max"]
    min_temp = data["list"][0]["temp"]["min"]
    description = data["list"][0]["weather"][0]["description"]

    answer = (
        "Tomorrow the maximum temperature will be "
        + str(max_temp)
        + " and the minimum temperature will be "
        + str(min_temp)
        + ". The weather will be looking like "
        + description
        + ". "
    )

    return answer


def get_news(news_cateogories):
    """Get news.

    This functions calls the news endpoint of the news service and returns the news for the given categories.
    For every category a separate endpoint call is made since the news service endpoints do not support multiple categories.

    Args:
        news_categories: The news categories for which the news should be returned.

    Returns:
        News for the given categories or an explanatory string if no news could be found.
    """

    url = f"http://news:5000/tagesschau/homepage"
    response = requests.get(url)
    if response.status_code != 200:
        return "No news found for the provided categories."
        # jsonify({"error": "Error getting weather information"}), 500

    data = response.json()
    compromised_data = []

    if(data):
        for message in data:
            compromised_data.append(message["Summary"])


        translator = Translator()

        data_TTS = []

        for ind, text in enumerate(compromised_data):
            if ind < 2:
                germnan_text = translator.translate(text, src="de", dest="en").text
                text = germnan_text.replace(".", ". ")
                data_TTS.append(text)
            else:
                germnan_text = translator.translate(text, src="de", dest="en").text
                text = germnan_text.replace(".", ". ")
                more_news.append(text)


        if len(data_TTS) < 2:
            answer = (
                "These are the headline storys for the day: "
                + str(data_TTS[0])
            )
        else:
            answer = (
                "These are the headline storys for the day: "
                + str(data_TTS[0])
                + "Here is your next article: "
                + str(data_TTS[1])
            )
        return answer
    else:
        return "no data found in Scuttlebut!"


def get_stocks(stocks):
    """Get stock quotes.

    This functions calls the quotes endpoint of the stock service and returns the stock quotes for the given stocks.

    Args:
        stocks: The stock names for which the quotes should be returned.

    Returns:
        Quotes for the given stocks or an explanatory string if no quotes could be found.
    """

    symbols = get_stock_symbols(stocks)

    url = "http://stockmarket:5000/quotes"
    params = {"symbols": symbols}
    response = requests.get(url, params)
    if response.status_code != 200:
        return "No quotes found for the provided stocks."
        # jsonify({"error": "Error getting stock service information"}), 500

    data = response.json()
    # TODO: Implement string building

    return data


def get_stock_symbols(stocks):
    """Get stock symbols.

    This functions returns the stock symbols for the given stocks.

    Args:
        stocks: The stock names for which the symbols should be returned.

    Returns:
        The stock symbols for the given stocks.
    """

    symbols = {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Alphabet": "GOOG",
        "Amazon": "AMZN",
        "NVIDIA": "NVDA",
        "Tesla": "TSLA",
        "TSMC": "TSM",
        "Ford": "F",
    }

    symbols_list = []
    for stock in stocks:
        symbols_list.append(symbols.get(stock, "None"))
    symbols_list = ",".join(symbols_list)

    return symbols_list


def get_stock_news(stocks):
    """ "Get stock news.

    This functions calls the news endpoint of the stock service and returns the news for the given stocks.

    Args:
        stocks: The stocks for which the news should be returned. Multiple stocks can be selected.

    Returns:
        The news for the given stocks or an explanatory string if no news could be found.
    """

    symbols = get_stock_symbols(stocks)

    url = "http://stockmarket:5000/news"
    params = {"symbols": symbols}
    response = requests.get(url, params)
    if response.status_code != 200:
        return "No news found for the provided stocks."

    data = response.json()

    stock_news = []
    for symbol in symbols.split(","):
        if len(data[symbol]) > 0:
            news_string = (
                symbol
                + ": "
                + data[symbol][0]["headline"]
                + " "
                + data[symbol][0]["summary"]
            )
            stock_news.append(news_string)

    if len(stock_news) == 0:
        answer = "There is no news for the stocks you are interested in."
    else:
        answer = "Here are the news for the stocks you are interested in: " + " ".join(
            stock_news
        )
        if answer[-1] not in [".", "?", "!"]:
            answer += ". "

    return answer


def get_user_preferences(user):
    """Get user preferences.

    This functions calls the user endpoint of the database service and returns the user preferences.

    Args:
        user: The username of the user. Only one username can be selected.

    Returns:
        The user preferences.
    """

    url = "http://db:5000/users/" + user
    response = requests.get(url)
    if response.status_code != 200:
        jsonify({"error": "Error getting user preferences"}), 500

    data = response.json()

    return data


@app.route("/scuttlebutt")
def get_scuttlebutt():
    """Scuttlebutt endpoint.

    This endpoint provides the scuttlebutt use case logic.

    Args:
        user: The username of the user. Only one username can be selected.

    Returns:
        The scuttlebutt use case response containing news, weather, stock quotes and stock news.
    """

    if not request.args.get("user"):
        return jsonify({"error": "Missing parameters"}), 400

    user = request.args.get("user")

    user_preferences = get_user_preferences(user)
    news_cateogories = user_preferences["news"].split(",")
    stocks = user_preferences["stocks"].split(",")
    user_coordinates = user_preferences["coordinates"].split(",")
    # user_location = {"lat": user_coordinates[0], "lon": user_coordinates[1]}

    news = get_news(news_cateogories)
    weather = get_weather(user_coordinates)
    stock_news = get_stock_news(stocks)

    return jsonify(
        {
            "news": news,
            "weather": weather,
            "stock_news": stock_news,
        }
    )


@app.route("/scuttlebutt/additional")
def get_more_scuttlebutt():
    """Additional scuttlebutt endpoint.

    This endpoint provides additional news for the scuttlebutt use case.

    Returns:
        Additional news for the scuttlebutt use case.
    """

    if len(more_news):
        return jsonify({"text": more_news})
    else:
        return jsonify({"error": "Error getting additional information"}), 500


if __name__ == "__main__":
    app.run()

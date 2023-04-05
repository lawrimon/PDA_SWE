"""This application is the stock market service.

The maps service provides an endpoint to get the latest quote of a list of symbols.
It also provides an endpoint to get the latest news of a list of symbols.
The functionality is based on the Alpaca API.

Typical endpoints usage:

    GET /quotes?symbols=IBM,MSFT,GOOG
    GET /news?symbols=IBM,MSFT,GOOG
"""

from flask import Flask, jsonify, request
import requests
import dotenv
import os
import datetime

app = Flask(__name__)

dotenv.load_dotenv()
#STOCK_MARKET_API_KEY = os.getenv("STOCK_MARKET_API_KEY")
#STOCK_MARKET_SECRET_KEY = os.getenv("STOCK_MARKET_SECRET_KEY")
STOCK_MARKET_API_KEY="PKBR8Q6JBV1ZJIEHHWBV"
STOCK_MARKET_SECRET_KEY="PwcPbNK9dFJ2V10Okwk3Kc2sVtO4txWnxofoy7rg"


@app.route("/quotes")
def get_quotes():
    """Quotes endpoint.

    This endpoint provides the latest quotes of a list of symbols.

    Args:
        symbols: A list of symbols (e.g. "IBM,MSFT,GOOG").

    Returns:
        A list of the latest quotes of the symbols.
    """

    if request.args.get("symbols") is None:
        return jsonify({"error": "Missing parameters"}), 400

    if not request.args.get("symbols").replace(",", "").isalpha():
        return jsonify({"error": "Invalid parameters"}), 400

    symbols = request.args.get("symbols")
    feed = "iex"
    currency = "EUR"

    url = f"https://data.alpaca.markets/v2/stocks/quotes/latest"
    params = {
        "symbols": symbols,
        "feed": feed,
        "currency": currency,
    }
    headers = {
        "APCA-API-KEY-ID": STOCK_MARKET_API_KEY,
        "APCA-API-SECRET-KEY": STOCK_MARKET_SECRET_KEY,
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Error getting quote information"}), 500

    data = response.json()

    quotes = {}
    for symbol in symbols.split(","):
        quote = {
            "bid_price": data["quotes"][symbol]["bp"],
            "ask_price": data["quotes"][symbol]["ap"],
            "currency": currency,
        }
        quotes[symbol] = quote

    return jsonify(quotes)


@app.route("/news")
def get_news():
    """News endpoint.

    This endpoint provides the latest news of a list of symbols.

    Args:
        symbols: A list of symbols (e.g. "IBM,MSFT,GOOG").

    Returns:
        A list of the latest news of the symbols.
    """

    if request.args.get("symbols") is None:
        return jsonify({"error": "Missing parameters"}), 400

    if not request.args.get("symbols").replace(",", "").isalpha():
        return jsonify({"error": "Invalid parameters"}), 400

    symbols = request.args.get("symbols")
    start = datetime.datetime.now() - datetime.timedelta(days=30)
    start = start.isoformat().split("T")[0]
    include_content = "true"

    url = f"https://data.alpaca.markets/v1beta1/news"
    params = {
        "symbols": symbols,
        "start": start,
        "include_content": include_content,
    }
    headers = {
        "APCA-API-KEY-ID": STOCK_MARKET_API_KEY,
        "APCA-API-SECRET-KEY": STOCK_MARKET_SECRET_KEY,
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Error getting news information"}), 500

    data = response.json()

    news = {}
    for symbol in symbols.split(","):
        news[symbol] = []
        for item in data["news"]:
            for item_symbol in item["symbols"]:
                if item_symbol == symbol:
                    article = {
                        "headline": item["headline"],
                        "summary": item["summary"],
                        "url": item["url"],
                        "source": item["source"],
                        "author": item["author"],
                        "created_at": item["created_at"],
                    }
                    news[symbol].append(article)

    return jsonify(news)


if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=5001, debug=True)

from flask import Flask, jsonify, request
import requests, flask_cors
from googletrans import Translator


app = Flask(__name__)
flask_cors.CORS(app)

more_stocks = []
more_news = []


def get_quotes():
    quotes = "Here are some famous quotes: "
    url = "http://wisdom:5000/wisdom/quotes"

    response = requests.get(url)
    if response.status_code != 200:
        jsonify({"error": "Error getting stock service information"}), 500

    data = response.json()
    for i in data:
        quotes += (
            "From the author: " + i["author"] + ". " + "Following quote: " + i["quote"]
        )

    return quotes


def get_nasa():
    nasa = "Here are you lates nasa-star news : "
    url = "http://wisdom:5000/wisdom/apod"

    response = requests.get(url)
    if response.status_code != 200:
        jsonify({"error": "Error getting stock service information"}), 500

    data = response.json()
    nasa += data["explanation"]

    return nasa


def get_random_facts():
    facts = "Here are some random facts: "
    url = "http://wisdom:5000//wisdom/random_facts"

    response = requests.get(url)
    if response.status_code != 200:
        jsonify({"error": "Error getting stock service information"}), 500

    data = response.json()
    for i in data:
        facts += i["fact"]
        facts += ". "

    return facts


def get_books():
    return None


@app.route("/shoreleave")
def get_shoreleave():
    print("lol")
    quotes = get_quotes()
    nasa_facts = get_nasa()
    random_facts = get_random_facts()

    return jsonify(
        quotes,
        nasa_facts,
        random_facts,
        "Thank you for listening. Do you want any additional information? ",
    )


if __name__ == "__main__":
    app.run()

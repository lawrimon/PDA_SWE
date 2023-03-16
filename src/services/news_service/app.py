"""This application is the news service.

 The news service is a service that provides news information.
 The functionality is based on the Tagesschau API and the New York Times API.
 """

from flask import Flask, jsonify, request
import requests
import dotenv
import os

dotenv.load_dotenv()
NYTIMES_API_KEY = os.getenv("NYTIMES_API_KEY")

app = Flask(__name__)


@app.route("/news/tagesschau/here")
def get_tagesschau_here():
    """Tagesschau news endpoint.

    This endpoint provides current news from tagesschau.de.

    Args:
        regions: The german states the news are from. Multiple regions can be combined with a comma. Can be 1=Baden-Württemberg, 2=Bayern, 3=Berlin, 4=Brandenburg, 5=Bremen, 6=Hamburg, 7=Hessen, 8=Mecklenburg-Vorpommern, 9=Niedersachsen, 10=Nordrhein-Westfalen, 11=Rheinland-Pfalz, 12=Saarland, 13=Sachsen, 14=Sachsen-Anhalt, 15=Schleswig-Holstein, 16=Thüringen.
        topic: The topic of the news. Only one topic can be selected. Can be "inland", "ausland", "wirtschaft", "sport", "video", "investigativ" or "faktenfinder".

    Returns:
        The available news based on the regions and topic.
    """

    if not request.args.get("regions") or not request.args.get("topic"):
        return jsonify({"error": "Missing parameters"}), 400

    if invalid_tagesschau_parameters(request.args):
        return jsonify({"error": "Invalid parameters"}), 400

    regions = request.args.get("regions")
    topic = request.args.get("topic")

    url = f"https://www.tagesschau.de/api2/news"
    params = {
        "regions": regions,
        "ressort": topic,
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Error getting tagesschau news information"}), 500

    data = response.json()

    return jsonify(data)


@app.route("/news/tagesschau/homepage")
def get_tagesschau_homepage():
    """Tagesschau homepage endpoint.

    This endpoint provides news information from the Tagesschau homepage.

    Returns:
        The current news from the Tagesschau homepage.
    """

    url = "https://www.tagesschau.de/api2/homepage"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Error getting tagesschau homepage information"}), 500

    data = response.json()

    return jsonify(data)


@app.route("/news/nytimes")
def get_nytimes():
    """New York Times news endpoint.

    This endpoint provides news information from the New York Times top stories.

    Args:
        topic: The topic of the news. Only one topic can be selected. Can be "arts", "automobiles", "books", "business", "fashion", "food", "health", "home", "insider", "magazine", "movies", "nyregion", "obituaries", "opinion", "politics", "realestate", "science", "sports", "sundayreview", "technology", "theater", "t-magazine", "travel", "upshot", "us", "world".

    Returns:
        The current news from the New York Times top stories based on the topic.
    """

    if request.args.get("topic") is None:
        return jsonify({"error": "Missing parameters"}), 400

    topics = [
        "arts",
        "automobiles",
        "books",
        "business",
        "fashion",
        "food",
        "health",
        "home",
        "insider",
        "magazine",
        "movies",
        "nyregion",
        "obituaries",
        "opinion",
        "politics",
        "realestate",
        "science",
        "sports",
        "sundayreview",
        "technology",
        "theater",
        "t-magazine",
        "travel",
        "upshot",
        "us",
        "world",
    ]

    if request.args.get("topic") not in topics:
        return jsonify({"error": "Invalid parameters"}), 400

    topic = request.args.get("topic")

    url = f"https://api.nytimes.com/svc/topstories/v2/{topic}.json"
    params = {
        "api-key": NYTIMES_API_KEY,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200 or (
        response.status_code == 200 and "errorcode" in response.json()
    ):
        return jsonify({"error": "Error getting nytimes news information"}), 500

    data = response.json()

    return jsonify(data)


def invalid_tagesschau_parameters(args):
    """Check if the tagesschau parameters are invalid.

    Args:
        arg: The request arguments.

    Returns:
        True if a parameter is invalid, False otherwise.
    """

    regions = args.get("regions")
    topic = args.get("topic")

    for region in regions.split(","):
        if region not in map(str, range(1, 17)):
            return True

    if topic not in [
        "inland",
        "ausland",
        "wirtschaft",
        "sport",
        "video",
        "investigativ",
        "faktenfinder",
    ]:
        return True

    return False

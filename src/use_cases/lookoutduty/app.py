from flask import Flask, jsonify, request
import requests, flask_cors
import json


app = Flask(__name__)
flask_cors.CORS(app)

more_stocks = []
more_news = []

def get_events(location, keyword_list, enddate):
    params = {"location": location, "keyword_list": keyword_list, "enddate": enddate}
    url = f"http://events:5000/events/all"
    response = requests.get(url, params)
    if response.status_code != 200:
        jsonify({"error": "Error getting weather information"}), 500
    data = response.json()
    return data




def get_sports(team):
    params = {"team":team}
    url = f"http://sports:5000/football/fixture"
    response = requests.get(url, params)
    if response.status_code != 200:
        jsonify({"error": "Error getting weather information"}), 500
    data = response.json()
    return data


@app.route("/lookout")
def get_scuttlebutt():
    location = request.args.get("city")
    keyword_list = request.args.get("artists")
    keyword_list = json.loads(keyword_list)
    enddate = request.args.get("enddate")
    team = request.args.get("team")
    print("lol")

    events = get_events(location,keyword_list, enddate)
    sports = get_sports(team)

    return jsonify(
        events,
        sports,
        "Thank you for listening. Do you want any additional information? ",
    )


if __name__ == "__main__":
    app.run()

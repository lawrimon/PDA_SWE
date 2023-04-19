from flask import Flask, request
import requests
from flask_cors import CORS, cross_origin
import dotenv
import os

app = Flask(__name__)
CORS(app)

dotenv.load_dotenv()


@app.route("/dialogflow/get_intent")
def get_intent():
    """
    Get intent from transcript endpoint

    Retrieve the intent from a given transcript using Dialogflow API.

    Args:
        transcript: A string representing the user's speech transcript to be processed.

    Returns:
        A JSON object containing the intent identified by Dialogflow API.
        If an error occurs while retrieving the intent, returns a 500 error with a JSON object containing the error message.
    """

    transcript = request.args.get("transcript")
    url = "https://capitan.azurewebsites.net/get_intent"
    params = {"transcript": transcript, "key": os.getenv("DIALOGFLOW_KEY")}

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return {
            "intent": response.json().get("intent"),
            "date_time": response.json().get("date_time"),
            "artist": response.json().get("artist"),
            "service": response.json().get("service"),
        }

    else:
        print(response.status_code)
        raise ValueError("Failed to get intent from transcript")


if __name__ == "__main__":
    app.run(debug=True, port=5021)

import os
import uuid
import json
from flask import Flask, request, jsonify
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
from google.protobuf.json_format import MessageToDict

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "capitan-382017-1431f46e0617.json"

app = Flask(__name__)


def create_session_id():
    """
    Generate a unique session ID for Dialogflow API.

    Returns:
        A string representing the unique session ID.
    """
    return str(uuid.uuid4())


def detect_intent_from_text(project_id, session_id, text):
    """
    Detect the intent, date-time, music-artist and service from a given text using Dialogflow API.

    Args:
        project_id: A string representing the ID of the Dialogflow project.
        session_id: A string representing the ID of the Dialogflow session.
        text: A string representing the user's speech transcript to be processed.

    Returns:
        A tuple containing the intent identified by Dialogflow API, the date-time parameter,
        the music-artist parameter, and the service parameter.
        If an error occurs while retrieving the intent, raises a ValueError.
    """
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(
            session=session, query_input=query_input
        )
    except InvalidArgument:
        raise ValueError("Failed to detect intent from transcript.")

    intent = response.query_result.intent.display_name
    date_time = response.query_result.parameters.get("date-time")
    artist = response.query_result.parameters.get("music-artist")
    service = response.query_result.parameters.get("service")

    return intent, date_time, artist, service


@app.route("/get_intent")
def submit_transcript():
    """
    Endpoint to retrieve the intent, date-time, music-artist, and service parameters from a given transcript.
    Args:
        None (parameters are extracted from the HTTP request query parameters).

    Returns:
        A JSON object containing the intent identified by Dialogflow API, the date-time parameter,
        the music-artist parameter, and the service parameter.
        If an error occurs while retrieving the intent, returns a 500 error with a JSON object containing the error message.
    """

    transcript = request.args.get("transcript")
    key = request.args.get("key")
    if key == "8b2936b27de29c5bd8e92845b98f6f4675f0e7bde84cc4523a1ebee65343aae4":
        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"
        ] = "capitan-382017-1431f46e0617.json"
        try:
            intent, date_time, artist, service = detect_intent_from_text(
                "capitan-382017", create_session_id(), transcript
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 500

        return jsonify(
            {
                "intent": intent,
                "date_time": date_time,
                "artist": artist,
                "service": service,
            }
        )


if __name__ == "__main__":
    app.run(debug=True, port=8003)

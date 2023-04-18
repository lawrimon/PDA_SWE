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
    return str(uuid.uuid4())

def detect_intent_from_text(project_id, session_id, text):

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    intent = response.query_result.intent.display_name

    return intent

@app.route('/get_intent')
def submit_transcript():
    transcript = request.args.get("transcript")
    try:
        intent = detect_intent_from_text("capitan-382017", create_session_id(), transcript)
    except ValueError as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'intent': intent})

if __name__ == '__main__':
    app.run(debug=True, port=8003)


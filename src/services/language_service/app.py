import os
import uuid
from flask import Flask, request
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "capitan-382017-1431f46e0617.json"

session_id = str(uuid.uuid4())

def detect_intent_from_text(text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path("capitan-382017", session_id)

    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    return response.query_result.intent.display_name

app = Flask(__name__)

@app.route('/')
def detect_intent():
    intent = detect_intent_from_text("Tell me about any noteworthy news that happened recently")
    return f'The intent is {intent}'

if __name__ == '__main__':
    app.run(debug=True, port=8002)

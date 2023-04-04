import os
import uuid
from flask import Flask, request, jsonify
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument

# Set environment variable for Google Cloud Platform credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "capitan-382017-1431f46e0617.json"

# Create a unique session ID for each request
def create_session_id():
    return str(uuid.uuid4())

# Create a Dialogflow session and detect intent from text input
def detect_intent_from_text(project_id, session_id, text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code="en")
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    fulfillment_text = response.query_result.fulfillment_text
    intent = response.query_result.intent.display_name
    confidence = response.query_result.intent_detection_confidence
    date_time = response.query_result.parameters.get('date-time')



    return fulfillment_text, intent, confidence, date_time

# Initialize the Flask application
app = Flask(__name__)

# Route for handling transcript submission requests
@app.route('/submit_transcript', methods=['GET', 'POST'])
def submit_transcript():
    data = "Can you give me a rundown of today's news"
    transcript = data 
    try:
        intent = detect_intent_from_text("capitan-382017", create_session_id(), transcript)
    except ValueError as e:
        return jsonify({'error': str(e)}), 500
    fulfillment_text, intent, confidence, date_time = detect_intent_from_text("capitan-382017", create_session_id(), transcript)

    return jsonify({'intent': intent, 'parameters': confidence, 'fulfillment_text': fulfillment_text, 'date_time': date_time})

if __name__ == '__main__':
    app.run(debug=True, port=8003)


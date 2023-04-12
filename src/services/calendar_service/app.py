"""This application is the calendar service.

The calendar service provides an endpoint the get the upcoming events of a user's Google calendar.
The functionality is based in the Google Calendar API.

https://developers.google.com/calendar/api/quickstart/python
https://developers.google.com/identity/protocols/oauth2/web-server#python
https://stackoverflow.com/questions/65586733/integrating-googles-refresh-access-token-offline-with-credentials-in-one-func

Typical endpoint usage:

"""

from __future__ import print_function

import datetime
import os.path

from flask import Flask, jsonify
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

app = Flask(__name__)

@app.route("/calendar/getappointment")
def get_calendar_appointments():
    creds = get_creds()

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return jsonify({"error": "No upcoming events found."}), 404

        # Convert the events to a list of dictionaries
        events_list = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            events_list.append({"start": start, "summary": event['summary']})

        return jsonify(events_list)

    except HttpError as error:
        return jsonify({"error": "An error occurred: %s" % error}), 500

@app.route("/calendar/addappointment")
def add_calendar_appointments():
    creds = get_creds()
    summary = "test event"
    start_time = "2023-04-13T16:00:00+02:00"
    end_time = "2023-04-13T17:00:00+02:00"
    try:
        service = build('calendar', 'v3', credentials=creds)

        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()

        return jsonify({"success": "Event added successfully."}), 200

    except HttpError as error:
        return jsonify({"error": "An error occurred: %s" % error}), 500



@app.route("/calendar/deleteappointment")
def delete_calendar_appointments():
    return 0

def get_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

if __name__ == '__main__':
    app.run()




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

from flask import Flask, jsonify, request
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

app = Flask(__name__)


@app.route("/calendar/getappointments")
def get_calendar_appointments():
    """Get appointment endpoint

    Retrieve a list of upcoming events from the user's primary calendar filtered by user and/or date.

    Args:
        user: A string representing the username of the events to be filtered (optional).
        requested_date: A string representing the date to filter the events by in "yyyy-mm-dd" format (optional).

    Returns:
        A JSON object containing the start time and summary of each upcoming event that matches the specified filter(s).
        If no events are found, returns a 404 error.
        If an error occurs while retrieving the events, returns a 500 error with a JSON object containing the error message.
    """

    creds = get_creds()
    user = request.args.get("user")

    try:
        service = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.utcnow().isoformat()
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return jsonify({"error": "No upcoming events found."}), 404

        events_list = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event["summary"]
            if "@" in summary:
                event_user = summary.split("@")[1]
                if event_user == user:
                    events_list.append({"start": start, "summary": summary})
            else:
                events_list.append({"start": start, "summary": summary})

        if request.args.get("requested_date") is not None:
            filtered_dates = match_date(request.args.get("requested_date")).strftime(
                "%d/%m/%Y"
            )
            filtered_events_list = []
            for event in events_list:
                if filtered_dates == event["start"][:10]:
                    filtered_events_list.append(event)
            events_list = filtered_events_list

        return jsonify(events_list)

    except HttpError as error:
        return jsonify({"error": "An error occurred: %s" % error}), 500


@app.route("/calendar/addappointment")
def add_calendar_appointments():
    """Calendar add appointment endpoint

    Add a new appointment to the user's Google calendar.

    Args:
        summary: A brief summary of the appointment.
        start_time: The start time of the appointment, in ISO format.
        end_time: The end time of the appointment, in ISO format.
        user: The user for whom the appointment is being added.

    Returns:
        A JSON response indicating success or failure.
    """

    creds = get_creds()

    if (
        not request.args.get("summary")
        or not request.args.get("start_time")
        or not request.args.get("end_time")
        or not request.args.get("user")
    ):
        return jsonify({"error": "Missing parameters"}), 400

    summary = request.args.get("summary") + f" @{request.args.get('user')}"
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")

    try:
        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": summary,
            "start": {
                "dateTime": start_time,
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "UTC",
            },
        }

        event = service.events().insert(calendarId="primary", body=event).execute()

        return jsonify({"success": "Event added successfully."}), 200

    except HttpError as error:
        return jsonify({"error": "An error occurred: %s" % error}), 500


@app.route("/calendar/deleteappointment")
def delete_calendar_appointments():
    """Calendar delete appointment endpoint
    Deletes events from the primary calendar with the matching summary.

    Args:
        summary: The summary of the event(s) to be deleted.

    Returns:
        A JSON response containing either an error message or a success message.
    """

    creds = get_creds()

    if not request.args.get("summary"):
        return jsonify({"error": "Missing summary parameter"}), 400

    summary = request.args.get("summary")

    try:
        service = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=50,
                singleEvents=True,
                orderBy="startTime",
                q=summary,
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return jsonify({"error": "No events found with summary %s" % summary}), 404

        for event in events:
            service.events().delete(calendarId="primary", eventId=event["id"]).execute()

        return (
            jsonify(
                {"success": "Events with summary %s deleted successfully." % summary}
            ),
            200,
        )

    except HttpError as error:
        return jsonify({"error": "An error occurred: %s" % error}), 500


def get_creds():
    """Retrieves the user's credentials from the token.json file or generates a new one if necessary.

    Returns:
        Credentials object.
    """

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def match_date(request):
    """
    Matches date based on the user input and returns a list of dates.

    Args:
        request: User input for the date query.

    Returns:
        A list of datetime objects representing the dates matching the user input, or the user input itself if no matches were found.
    """

    today = datetime.date.today()
    if "today" in request.lower():
        return today
    elif "tomorrow" in request.lower():
        return today + datetime.timedelta(days=1)
    elif "this week" in request.lower():
        current_day = today.weekday()
        this_sunday = today + datetime.timedelta(days=(6 - current_day))
        this_week = [
            this_sunday + datetime.timedelta(days=x - current_day) for x in range(7)
        ]
        return this_week
    elif "next week" in request.lower():
        next_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
        return [next_monday + datetime.timedelta(days=x) for x in range(7)]
    elif "this month" in request.lower():
        first_day = today.replace(day=1)
        last_day = first_day.replace(
            month=first_day.month % 12 + 1, day=1
        ) - datetime.timedelta(days=1)
        return [
            first_day + datetime.timedelta(days=x)
            for x in range((last_day - first_day).days + 1)
        ]
    else:
        return request


if __name__ == "__main__":
    app.run()

from flask import Flask, jsonify, request
import requests, flask_cors

app = Flask(__name__)
flask_cors.CORS(app)

#add a event to the calendar (user, description, start time, end time, location)
@app.route("/example_add_event")
def add_event():
    url = "http://127.0.0.1:5000/calendar/addappointment"
    user = "user1"
    summary = "meeting at university"
    start_time = "2023-04-14T15:30:00+01:00"
    end_time = "2023-04-14T16:30:00+01:00"
    location = "Stuttgart"

    response = requests.get(url, params={"user": user, "summary": summary, "start_time": start_time, "end_time": end_time, "location": location})

    data = response.json()
    print(data)

    return data

#list all events for a specific user (description, location, start time, end time)
@app.route("/example_get_event")
def get_event():
    url = "http://127.0.0.1:5000/calendar/getappointments"

    user = "user1"
    response = requests.get(url, params={"user": user})

    data = response.json()
    print(data)

    return data

#delete a event based on the description of the event + @user
@app.route("/example_delete_event")
def delete_event():
    url = "http://127.0.0.1:5000/calendar/deleteappointment"

    user="user1"
    summary="meeting at university"
    response = requests.get(url, params={"summary": summary, "user": user}, verify=False)

    data = response.json()
    print(data)

    return data

if __name__ == '__main__':
    app.run(debug=True, port=5001)


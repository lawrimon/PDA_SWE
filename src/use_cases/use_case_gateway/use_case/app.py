from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify
import json
import requests
import pika
from datetime import datetime, timedelta


app = Flask(__name__)

RABBITMQ_HOST = "rabbitmq"

# Mock users
#users = ["user1", "user2", "user3"]

def get_all_user():
    url = "http://db:5000/allUsers"

    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Error getting books information"}), 500

    users = response.json()

    return users


# to get all users in production have a look at the "/allusers" Endpoint in database app.py
# something like: allUsers = requests.get("http://db/allUsers")

# Rabbitmq: have a look at localhost:1572
# use notification exchange like shown below, just change body and routing_key

ENDPOINT = "http://data_source:5000"


def get_user_location(user_id):
    """
    This function retrieves the location of a user by calling the App1 API.
    """
    response = requests.get(f"{ENDPOINT}/location/{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_user_appointments(user_id):
    """
    This function retrieves the appointments of a user by calling the App1 API.
    """
    response = requests.get(f"{ENDPOINT}/appointments/{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_nearby_events(location):
    """
    This function retrieves the events near a location by calling the App1 API.
    """
    response = requests.get(f"{ENDPOINT}/events/{location}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_scuttlebutt(user):
    """
    This function retrieves the scuttlebutt usecase.
    """
    url = "http://scuttlebutt:5000/scuttlebutt?user="+ user

    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Error getting books information"}), 500

    message = response.json()

    return message

def check_appointment_interference(appointments, event):
    """
    This function checks if an event interferes with any appointments of the user.
    """
    # Define the duration of an appointment
    appointment_duration = timedelta(minutes=30)

    # Convert the event time string to a datetime object
    event_time = datetime.strptime(event["time"], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Loop over the appointments and check for interference
    for appointment in appointments:
        # Convert the appointment time string to a datetime object
        appointment_time = datetime.strptime(
            appointment["time"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )

        # Check if the event and appointment overlap in time
        if (
            appointment_time <= event_time <= appointment_time + appointment_duration
        ) or (
            appointment_time
            <= event_time + appointment_duration
            <= appointment_time + appointment_duration
        ):
            return True

    # If no interference is found, return False
    return False


def notify_users():
    """
    This function retrieves the events near the user's location and checks if they
    interfere with any appointments of the user. If the requirements are met, it
    publishes the event to a RabbitMQ queue.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange="notifications", exchange_type="direct")

    users = get_all_user()

    for user_id in users:
        channel.queue_declare(queue=user_id)
        channel.queue_bind(exchange="notifications", queue=user_id, routing_key=user_id)
        
        '''
        Todo: call the scuttlebutt function and check for problems 
        -> Checking for problems should happen using the calendar service!
        '''
        message = get_scuttlebutt(user_id)

        if(message):
            # convert the event object to a string before publishing
            event_str = json.dumps(message)
            # publish the event to the queue
            channel.basic_publish(
                exchange="notifications", routing_key=user_id, body=event_str
            )

    channel.close()
    connection.close()


# publish every 7 seconds
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=notify_users, trigger="interval", seconds=30)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)

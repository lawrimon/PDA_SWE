from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import json
import requests
import pika
from datetime import datetime, timedelta

app = Flask(__name__)
RABBITMQ_HOST = "rabbitmq"

# Mock users
users = ["user1", "user2", "user3"]


def get_user_location(user_id):
    """
    This function retrieves the location of a user by calling the App1 API.
    """
    response = requests.get(f"http://app1:5000/location/{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_user_appointments(user_id):
    """
    This function retrieves the appointments of a user by calling the App1 API.
    """
    response = requests.get(f"http://app1:5000/appointments/{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_nearby_events(location):
    """
    This function retrieves the events near a location by calling the App1 API.
    """
    response = requests.get(f"http://app1:5000/events/{location}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


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
    channel.queue_declare(queue="notifications")

    for user_id in users:
        location = get_user_location(user_id)
        appointments = get_user_appointments(user_id)
        events = get_nearby_events(location)
        print(events)
        if events:
            for event in events["data"]:
                if not check_appointment_interference(appointments["data"], event):
                    # convert the event object to a string before publishing
                    event_str = json.dumps(event)
                    # publish the event to the queue
                    channel.basic_publish(
                        exchange="", routing_key="notifications", body=event_str
                    )
    connection.close()


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=notify_users, trigger="interval", seconds=7)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)

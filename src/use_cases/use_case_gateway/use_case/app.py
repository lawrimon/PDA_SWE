from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, jsonify
import requests
import json
import pika
from datetime import datetime, timedelta


app = Flask(__name__)


lokal = False

if lokal:
    RABBITMQ_HOST = "localhost"
    SCUTTLEBUTT = "http://localhost:5008"
    LOOKOUT = "http://localhost:5016"
    SHORELEAVE = "http://localhost:5013"
    RACKTIME = "http://localhost:5018"
    DATABASE = "http://localhost:5009"
else:
    RABBITMQ_HOST = "rabbitmq"
    SCUTTLEBUTT = "http://scuttlebutt:5000"
    LOOKOUT = "http://lookoutduty:5000"
    SHORELEAVE = "http://shoreleave:5000"
    RACKTIME = "http://racktime:5000"
    DATABASE = "http://db:5000"


def get_scuttlebutt(user):
    """
    This function retrieves the scuttlebutt usecase.
    """
    with app.app_context():
        url = SCUTTLEBUTT + "/scuttlebutt?user=" + user
        print("inside get_scuttlebutt")
        response = requests.get(url)
        if response.status_code != 200:
            # no error handling ?
            print("Error requesting Scuttlebut: " + str(response.text))
            return ""

        message = response.json()
        return message


def get_lookout(user):
    """
    This function retrieves the lookout usecase.
    """
    with app.app_context():
        url = LOOKOUT + "/lookout?user=" + user
        print("inside get_lookout")
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({"error": "Error getting books information"}), 500

        message = response.json()

        return message


def get_shoreleave(user):
    """
    This function retrieves the shoreleave usecase.
    """
    with app.app_context():
        url = SHORELEAVE + "/shoreleave?user=" + user
        print("inside get_shoreleave")
        response = requests.get(url)
        if response.status_code != 200:
            # no error handling ?
            return ""

        message = response.json()

        return message


def get_racktime(user):
    """
    This function retrieves the scuttlebutt usecase.
    """
    with app.app_context():
        url = RACKTIME + "/racktime?user=" + user
        print("inside get_racktime")
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({"error": "Error getting books information"}), 500

        message = response.json()

        return message


def get_all_user():
    """
    This function retrieves all user IDs from the user service and returns them as a list.

    Returns:
        A list containing all the user IDs.
    """
    with app.app_context():
        url = DATABASE + "/allusers"
        print("inside get_all_user")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error getting user information: {response.text}")
            return []
        else:
            users = response.json()
            return users


def notify_scuttlebutt():
    """
    This function retrieves the events near the user's location and checks if they
    interfere with any appointments of the user. If the requirements are met, it
    publishes the event to a RabbitMQ queue.
    """

    users = get_all_user()

    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange="notifications", exchange_type="direct")

    # check that there is at least one user
    if users:
        for user in users:
            print(user)
            user_id = user

            channel.queue_declare(queue=user_id)
            channel.queue_bind(
                exchange="notifications", queue=user_id, routing_key=user_id
            )

            """
            Todo: call the scuttlebutt function and check for problems 
            -> Checking for problems should happen using the calendar service!
            """

            # no error handling ?
            message = get_scuttlebutt(user)

            if len(message) > 1:
                print("Message from Scuttlebut received: " + str(message))
                # convert the event object to a string before publishing
                event_str = json.dumps(message)
                # publish the event to the queue
                channel.basic_publish(
                    exchange="notifications", routing_key=user_id, body=event_str
                )
    else:
        print("No users found!")

    channel.close()
    connection.close()


def notify_lookout():
    """
    This function retrieves the events near the user's location and checks if they
    interfere with any appointments of the user. If the requirements are met, it
    publishes the event to a RabbitMQ queue.
    """

    users = get_all_user()

    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange="notifications", exchange_type="direct")

    # check that there is at least one user
    if users:
        for user in users:
            print(user)
            user_id = user
            channel.queue_declare(queue=user_id)
            channel.queue_bind(
                exchange="notifications", queue=user_id, routing_key=user_id
            )

            message = get_lookout(user_id)

            if message:
                print("Message from lookout received")
                # convert the event object to a string before publishing
                event_str = json.dumps(message)
                # publish the event to the queue
                channel.basic_publish(
                    exchange="notifications", routing_key=user_id, body=event_str
                )
            else:
                print("No users found!")


def notify_shoreleave():
    """
    This function retrieves the events near the user's location and checks if they
    interfere with any appointments of the user. If the requirements are met, it
    publishes the event to a RabbitMQ queue.
    """

    users = get_all_user()

    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange="notifications", exchange_type="direct")

    # check that there is at least one user
    if users:
        for user in users:
            print(user)
            user_id = user

            channel.queue_declare(queue=user_id)
            channel.queue_bind(
                exchange="notifications", queue=user_id, routing_key=user_id
            )

            message = get_shoreleave(user_id)

            if message:
                print("Message from shoreleave received")
                # convert the event object to a string before publishing
                event_str = json.dumps(message)
                # publish the event to the queue
                channel.basic_publish(
                    exchange="notifications", routing_key=user_id, body=event_str
                )
            else:
                print("No users found!")


def notify_racktime():
    """
    This function retrieves the events near the user's location and checks if they
    interfere with any appointments of the user. If the requirements are met, it
    publishes the event to a RabbitMQ queue.
    """

    users = get_all_user()

    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange="notifications", exchange_type="direct")

    # check that there is at least one user
    if users:
        for user in users:
            print(user)
            user_id = user

            channel.queue_declare(queue=user_id)
            channel.queue_bind(
                exchange="notifications", queue=user_id, routing_key=user_id
            )

            message = get_racktime(user_id)

            if message:
                print("Message from shoreleave received")
                # convert the event object to a string before publishing
                event_str = json.dumps(message)
                # publish the event to the queue
                channel.basic_publish(
                    exchange="notifications", routing_key=user_id, body=event_str
                )
            else:
                print("No users found!")


# publish every 7 seconds
scheduler = BackgroundScheduler(daemon=True)


# schedule every x minutes

scheduler.add_job(func=notify_racktime, trigger="interval", seconds=60)
scheduler.add_job(func=notify_lookout, trigger="interval", minutes=1)
scheduler.add_job(func=notify_shoreleave, trigger="interval", minutes=1)


# schedule on day time (T-2h inside Docker)
trigger = CronTrigger(hour="18", minute="15")

scheduler.add_job(
    func=notify_scuttlebutt,
    trigger=trigger,
)

scheduler.start()


if __name__ == "__main__":
    app.run(host="0.0.0.0")

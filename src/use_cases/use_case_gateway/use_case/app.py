from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify
import requests
import json
import pika
from datetime import datetime, timedelta


app = Flask(__name__)

RABBITMQ_HOST = "localhost"


ENDPOINT = "http://localhost:5008"


def get_scuttlebutt(user):
    """
    This function retrieves the scuttlebutt usecase.
    """
    url = ENDPOINT + "/scuttlebutt?user="+ user
    print("inside get_scuttlebutt")
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
        url = "http://localhost:5009/allusers"
        print("inside get_all_user")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error getting user information: {response.text}")
            return []
        else:
            users = response.json()
            return users

def notify_users():
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
            user_id = user['user_id']

            channel.queue_declare(queue=user_id)
            channel.queue_bind(exchange="notifications", queue=user_id, routing_key=user_id)
            
            '''
            Todo: call the scuttlebutt function and check for problems 
            -> Checking for problems should happen using the calendar service!
            '''
            message = get_scuttlebutt(user_id)

            if(message):
                print("Message from Scuttlebut received")
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


# publish every 7 seconds
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=notify_users, trigger="interval", seconds=7)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)

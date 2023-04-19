from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, jsonify
import requests
import json
import pika
from datetime import datetime, timedelta


app = Flask(__name__)

is_local = False

if is_local:
    hostnames = {
        'RABBITMQ_HOST': 'localhost',
        'SCUTTLEBUTT': 'http://localhost:5008',
        'LOOKOUT': 'http://localhost:5016',
        'SHORELEAVE': 'http://localhost:5013',
        'RACKTIME': 'http://localhost:5018',
        'DATABASE': 'http://localhost:5009'
    }
else:
    hostnames = {
        'RABBITMQ_HOST': 'rabbitmq',
        'SCUTTLEBUTT': 'http://scuttlebutt:5000',
        'LOOKOUT': 'http://lookoutduty:5000',
        'SHORELEAVE': 'http://shoreleave:5000',
        'RACKTIME': 'http://racktime:5000',
        'DATABASE': 'http://db:5000'
    }

def get_response(url):
    with app.app_context():
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return None
        else:
            return response.json()

def get_scuttlebutt(user):
    with app.app_context():
        url = f"{hostnames['SCUTTLEBUTT']}/scuttlebutt?user={user}"
        print("inside get_scuttlebutt")
        return get_response(url)

def get_lookout(user):
    with app.app_context():
        url = f"{hostnames['LOOKOUT']}/lookout?user={user}"
        print("inside get_lookout")
        return get_response(url)

def get_shoreleave(user):
    with app.app_context():
        url = f"{hostnames['SHORELEAVE']}/shoreleave?user={user}"
        print("inside get_shoreleave")
        return get_response(url)

def get_racktime(user):
    with app.app_context():
        url = f"{hostnames['RACKTIME']}/racktime?user={user}"
        print("inside get_racktime")
        return get_response(url)

def get_all_user():
    with app.app_context():
        url = f"{hostnames['DATABASE']}/allusers"
        print("inside get_all_user")
        return get_response(url)
    
def notify_event(event_name):

    users = get_all_user()
    if not users:
        print("No users found!")
        return
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostnames['RABBITMQ_HOST']))
    channel = connection.channel()
    channel.exchange_declare(exchange='notifications', exchange_type='direct')

    for user_id in users:
        print(user_id)
        channel.queue_declare(queue=user_id)
        channel.queue_bind(exchange='notifications', queue=user_id, routing_key=user_id)

        message = None
        if event_name == 'scuttlebutt':
            message = get_scuttlebutt(user_id)
        elif event_name == 'lookout':
            message = get_lookout(user_id)
        elif event_name == 'shoreleave':
            message = get_shoreleave(user_id)
        elif event_name == 'racktime':
            message = get_racktime(user_id)

        if not message or len(message) <= 1:
            continue

        print(f"Message from {event_name.capitalize()} received: {message}")
        event_str = json.dumps(message)
        channel.basic_publish(exchange='notifications', routing_key=user_id, body=event_str)

    channel.close()
    connection.close()

# Schedule Use_Cases
scheduler = BackgroundScheduler(daemon=True)

# schedule on time
scheduler.add_job(func=notify_event, args=["lookout"], trigger="interval", minutes=1)
scheduler.add_job(func=notify_event, args=["racktime"], trigger="interval", minutes=1)
scheduler.add_job(func=notify_event, args=["shoreleave"], trigger="interval", minutes=1)


# schedule on day time (T-2h inside Docker)
trigger = CronTrigger(hour="18", minute="15")
scheduler.add_job(
    func=notify_event, args=["scuttlebutt"],
    trigger=trigger,
)

# start jobs
scheduler.start()


if __name__ == "__main__":
    app.run(host="0.0.0.0")

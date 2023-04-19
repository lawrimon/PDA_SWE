from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room

import json
import pika

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# Set up the RabbitMQ connection and channel
connection = None
channel = None
RABBITMQ_HOST = "rabbitmq"


def setup_rabbitmq():
    global connection, channel
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        channel = connection.channel()
        channel.exchange_declare(exchange="notifications", exchange_type="direct")
        channel.basic_qos(prefetch_count=1)
    except Exception as e:
        print("Exception occurred during RabbitMQ setup: ", e)


def start_consuming_messages(user_id):
    try:
        channel.queue_declare(queue=user_id)
        channel.queue_bind(exchange="notifications", queue=user_id, routing_key=user_id)
        channel.basic_consume(
            queue=user_id,
            on_message_callback=lambda ch, method, properties, body: on_message(
                user_id, body.decode("utf-8"), method.delivery_tag
            ),
            auto_ack=False,
        )
        channel.start_consuming()
    except Exception as e:
        print("Exception occurred during message consumption: ", e)


def on_message(user_id, message, delivery_tag):
    print("Message emitted: " + message + " " + user_id)
    emit(
        "message",
        {
            "user_id": user_id,
            "message": json.loads(message),
            "delivery_tag": delivery_tag,
        },
        room=user_id,
    )
    channel.basic_ack(delivery_tag=delivery_tag)


@socketio.on("connect")
def on_connect():
    print("Connected! " + request.sid)
    setup_rabbitmq()


@socketio.on("start")
def on_start(data):
    try:
        # Declare the queue for the current user
        user_id = data.get("user_id")
        print("user_id: " + user_id)
        room_id = user_id
        join_room(room_id)
        start_consuming_messages(user_id)
    except Exception as e:
        print("Exception occurred: ", e)
        if channel is not None and channel.is_open:
            channel.stop_consuming()
            channel.close()
        if connection is not None and connection.is_open:
            connection.close()


@socketio.on("disconnect")
def on_disconnect():
    try:
        print("Disconnected! " + request.sid)
        if channel is not None and channel.is_open:
            channel.stop_consuming()
            channel.close()
        if connection is not None and connection.is_open:
            connection.close()
    except Exception as e:
        print("Exception occurred: ", e)


@socketio.on("shutdown")
def on_shutdown():
    print("Shutting down...")
    if channel is not None and channel.is_open:
        channel.stop_consuming()
        channel.close()
    if connection is not None and connection.is_open:
        connection.close()


@socketio.on("ack")
def acknowledge_message(data):
    delivery_tag = data.get("delivery_tag")
    if delivery_tag and channel is not None:
        channel.basic_ack(delivery_tag=delivery_tag)
        print("Delivery_tag: " + str(delivery_tag))


if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5010)

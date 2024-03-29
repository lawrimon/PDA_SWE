from flask_socketio import SocketIO, emit, join_room
from flask import Flask, request
from flask_cors import CORS
import eventlet.debug
import eventlet
import json

# Monkey-patch the standard library to work with eventlet
eventlet.monkey_patch()

import pika

# Turn off the multiple-reader check in eventlet's hub (not sure why)
eventlet.debug.hub_prevent_multiple_readers(False)

# Create the Flask app and configure it
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

# Create the SocketIO server and allow CORS requests from any origin
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# Set up the RabbitMQ connection and channel
channel = None
connection = None
RABBITMQ_HOST = "rabbitmq"


# listen for acknowledge from client
@socketio.on("ack")
def acknowledge_message(data):
    delivery_tag = data.get("delivery_tag")

    if delivery_tag:
        # Acknowledge the message processing to RabbitMQ
        global channel
        if channel is not None:
            channel.basic_ack(delivery_tag=delivery_tag)
            print("Delivery_tag: " + str(delivery_tag))
        else:
            print("channel not found for ACK!")


# Define a function to emit a message to a user's SocketIO room
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


# Define a SocketIO event handler for when a user connects
@socketio.on("connect")
def on_connect():
    print("Connected! " + request.sid)
    global connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))


# Define a SocketIO event handler for when a user starts a conversation
@socketio.on("start")
def on_start(data):
    try:
        # Declare the queue for the current user
        user_id = data.get("user_id")
        print("user_id: " + user_id)
        room_id = user_id
        join_room(room_id)
        global channel
        global connection
        if connection is not None:
            channel = connection.channel()
            # Declare the exchange for the notifications
            channel.exchange_declare(exchange="notifications", exchange_type="direct")
            channel.queue_declare(queue=user_id)
            channel.queue_bind(
                exchange="notifications", queue=user_id, routing_key=user_id
            )
            # Set prefetch count to 1 to only consume one message at a time
            channel.basic_qos(prefetch_count=1)

            print("Starts Consuming")
            # Start consuming messages from the user's queue
            channel.basic_consume(
                queue=user_id,
                on_message_callback=lambda ch, method, properties, body: on_message(
                    user_id, body.decode("utf-8"), method.delivery_tag
                ),
                auto_ack=False,
            )
            channel.start_consuming()
        else:
            print("Error: connection not established!")
    except Exception as e:
        print("Exception occurred: ", e)
        if channel is not None and channel.is_open:
            channel.stop_consuming()
            channel.close()
        if connection is not None and connection.is_open:
            connection.close()


# Define a SocketIO event handler for when a user disconnects
@socketio.on("disconnect")
def on_disconnect():
    try:
        print("Disconnected! " + request.sid)
        global channel
        global connection
        if (channel is not None) and channel.is_open:
            channel.stop_consuming()
            channel.close()
        if (connection is not None) and connection.is_open:
            connection.close()
    except Exception as e:
        print("Exception occurred: ", e)


# Define a SocketIO event handler for when the server shuts down
@socketio.on("shutdown")
def on_shutdown():
    print("Shutting down...")
    global channel
    global connection
    if (channel is not None) and channel.is_open:
        channel.stop_consuming()
        channel.close()
    if (connection is not None) and connection.is_open:
        connection.close()


# Run the app
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5010)

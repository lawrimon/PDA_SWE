import pika
import json

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queues for each user
    users = ["user1", "user2", "user3"]
    for user in users:
        location_queue = channel.queue_declare(queue=f'location.{user}', durable=True)
        event_queue = channel.queue_declare(queue=f'event.{user}', durable=True)
        appointment_queue = channel.queue_declare(queue=f'appointment.{user}', durable=True)

        # Bind queues to appropriate exchanges
        channel.queue_bind(exchange='location', queue=location_queue.method.queue, routing_key=user)
        channel.queue_bind(exchange='event', queue=event_queue.method.queue, routing_key=user)
        channel.queue_bind(exchange='appointment', queue=appointment_queue.method.queue, routing_key=user)
except Exception as e:
    print(f"Error occurred while setting up RabbitMQ connection: {str(e)}")

# Declare the queues
channel.queue_declare(queue='notifications', durable=True)

def callback(ch, method, properties, body):
    data = json.loads(body)

    # Fetch user's location from data
    user_location = data['location']

    # Fetch user's appointments from data
    user_appointments = data['appointments']

    # Filter events that are near the user's location and don't interfere with appointments
    filtered_events = []
    for event in data['events']:
        event_location = event['location']
        event_time = event['time']

        # Check if the event is located near the user
        if abs(user_location['latitude'] - event_location['latitude']) <= 0.1 and \
           abs(user_location['longitude'] - event_location['longitude']) <= 0.1:

            # Check if the event time does not interfere with any of the user's appointments
            is_conflict = False
            for appointment in user_appointments:
                appointment_time = appointment['time']

                if appointment_time == event_time:
                    is_conflict = True
                    break

            if not is_conflict:
                filtered_events.append(event)

    # Publish filtered events to user's notification queue
    channel.basic_publish(
        exchange='',
        routing_key='notifications',
        body=json.dumps(filtered_events),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
            content_type='application/json'
        )
    )
    print(f"Filtered events published for user {data['user']}")

if channel:
    # Consume messages from user-specific queues
    users = ['user1', 'user2', 'user3']
    for user in users:
        channel.basic_consume(queue=f'location.{user}', on_message_callback=callback, auto_ack=True)
        channel.basic_consume(queue=f'event.{user}', on_message_callback=callback, auto_ack=True)
        channel.basic_consume(queue=f'appointment.{user}', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
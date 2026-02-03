import pika #type: ignore
import json

def publish_event(event_type: str, payload: dict):
    # Connect to RabbitMQ (local for now)
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Ensure queue exists
    channel.queue_declare(queue="notifications")

    # Build message
    message = {
        "event_type": event_type,
        "payload": payload
    }

    # Publish to queue
    channel.basic_publish(
        exchange="",
        routing_key="notifications",
        body=json.dumps(message)
    )

    print(f" [x] Published {event_type} event")
    connection.close()

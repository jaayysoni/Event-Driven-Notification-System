import pika
import json

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
QUEUE_NAME = "email_queue"


def publish_message(message: dict):
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ),
    )

    connection.close()
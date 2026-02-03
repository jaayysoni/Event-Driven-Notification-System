import pika, json # type: ignore
from app.services.sendgrid_service import send_email
from app.services.logger import log_notification

def callback(ch, method, properties, body):
    message = json.loads(body)
    event_type = message["event_type"]
    payload = message["payload"]

    print(f" [x] Received {event_type} event")

    try:
        send_email(payload["email"], event_type, payload)
        log_notification(payload["email"], event_type, True, "Email sent successfully")
    except Exception as e:
        log_notification(payload["email"], event_type, False, str(e))

def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="notifications")

    channel.basic_consume(queue="notifications", on_message_callback=callback, auto_ack=True)
    print(" [*] Worker started. Waiting for messages...")
    channel.start_consuming()

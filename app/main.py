# app/main.py

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from app.auth import oauth2
from app.config import settings

import threading
import pika
import json
import time
from app.services.sendgrid_service import send_email

app = FastAPI(title="Event-Driven Notification System")

# ------------------------
# RabbitMQ Config
# ------------------------
RABBITMQ_URL = settings.RABBITMQ_URL
QUEUE_NAME = "email_queue"


# ------------------------
# RabbitMQ Callback
# ------------------------
def callback(ch, method, properties, body):
    data = json.loads(body)

    email = data.get("email")
    name = data.get("name")

    print(f"📨 Processing email for {email}")

    try:
        send_email(email, name)
        print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Error sending email:", str(e))

    ch.basic_ack(delivery_tag=method.delivery_tag)


# ------------------------
# Worker with Retry Logic
# ------------------------
def start_worker():
    while True:
        try:
            print("🔄 Connecting to RabbitMQ...")
            connection = pika.BlockingConnection(
                pika.URLParameters(RABBITMQ_URL)
            )
            channel = connection.channel()

            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            channel.basic_qos(prefetch_count=1)

            channel.basic_consume(
                queue=QUEUE_NAME,
                on_message_callback=callback
            )

            print("✅ RabbitMQ Worker started. Waiting for messages...")
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("❌ RabbitMQ not available. Retrying in 5 seconds...")
            time.sleep(5)

        except Exception as e:
            print("❌ Unexpected Worker Error:", str(e))
            time.sleep(5)


# ------------------------
# Startup Event
# ------------------------
@app.on_event("startup")
def startup_event():
    worker_thread = threading.Thread(
        target=start_worker,
        daemon=True
    )
    worker_thread.start()
    print("✅ Worker running in background thread")


# ------------------------
# Middleware
# ------------------------
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    session_cookie="session",
    max_age=None,
    https_only=False  # Set True in production
)


# ------------------------
# Static & Templates
# ------------------------
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")


# ------------------------
# Routers
# ------------------------
app.include_router(oauth2.router)


# ------------------------
# Auth Dependency
# ------------------------
def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

# ------------------------
# Test Publish Endpoint
# ------------------------
@app.post("/test-email")
async def test_email(user: dict = Depends(get_current_user)):
    try:
        connection = pika.BlockingConnection(
            pika.URLParameters(settings.RABBITMQ_URL)
        )
        channel = connection.channel()

        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        message = {
            "email": user["email"],
            "name": user.get("name", "User")
        }

        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            ),
        )

        connection.close()

        return {"message": "Email event published to queue ✅"}

    except Exception as e:
        return {"error": str(e)}
    
# ------------------------
# Routes
# ------------------------
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    user: dict = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "Dashboard.html",
        {"request": request, "user": user}
    )


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")
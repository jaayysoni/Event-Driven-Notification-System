from fastapi import APIRouter # type: ignore
from datetime import datetime
from app.services.rabbitmq import publish_event

router = APIRouter()

@router.post("/register")
async def register(name: str, email: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {"name": name, "email": email, "time": now}
    publish_event("user_registered", payload)
    return {"message": "Registration successful, notification event published."}

@router.post("/login")
async def login(name: str, email: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {"name": name, "email": email, "time": now}
    publish_event("user_logged_in", payload)
    return {"message": "Login successful, notification event published."}

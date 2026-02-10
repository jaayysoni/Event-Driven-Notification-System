# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from app.auth import oauth2  # OAuth2 router
from app.config import settings  # Use your settings instead of os.getenv
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="Event-Driven Notification System")

# ------------------------
# Middleware
# ------------------------
# Use SESSION_SECRET_KEY from your settings for session middleware
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

# ------------------------
# Static & Templates
# ------------------------
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# ------------------------
# Routers
# ------------------------
app.include_router(oauth2.router, prefix="/auth")

# ------------------------
# Routes
# ------------------------
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Render the login page.
    """
    user = request.session.get("user")
    if user:
        # If already logged in, redirect to dashboard
        return RedirectResponse("/dashboard")
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Render the dashboard page for logged-in users.
    """
    user = request.session.get("user")
    if not user:
        # If user session not found, redirect to login
        return RedirectResponse("/")
    return templates.TemplateResponse("Dashboard.html", {"request": request, "user": user})


@app.get("/logout")
async def logout(request: Request):
    """
    Logout the user by clearing session and redirecting to login.
    """
    request.session.clear()
    return RedirectResponse("/")
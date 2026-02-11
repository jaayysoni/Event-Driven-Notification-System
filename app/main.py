# app/main.py
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from app.auth import oauth2  # OAuth2 router
from app.config import settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Event-Driven Notification System")

# ------------------------
# Middleware
# ------------------------
# max_age=None ensures session cookie expires when browser closes
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    session_cookie="session",
    max_age=None,       # None = cookie disappears when browser closes
    https_only=False    # Set True in production with HTTPS
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
    """
    Dependency to get current logged-in user.
    Raises 401 if not authenticated.
    """
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


# ------------------------
# Routes
# ------------------------
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Always render login page.
    Do not redirect automatically to dashboard.
    """
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: dict = Depends(get_current_user)):
    """
    Dashboard page for logged-in users only.
    """
    return templates.TemplateResponse("Dashboard.html", {"request": request, "user": user})


@app.get("/logout")
async def logout(request: Request):
    """
    Logout user by clearing session.
    """
    request.session.clear()
    return RedirectResponse("/")
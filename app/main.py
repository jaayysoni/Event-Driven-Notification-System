from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.auth import oauth2  # Import OAuth2 router

app = FastAPI()

# Mount static files (optional)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="frontend/templates")

# Include OAuth2 router
app.include_router(oauth2.router, prefix="/auth")

# Route to render login page
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Dummy dashboard route
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return HTMLResponse("<h1>Welcome to Dashboard!</h1>")
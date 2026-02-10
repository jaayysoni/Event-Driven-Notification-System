from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

# Route for Google login
@router.get("/google", name="oauth2_login")
async def login():
    # In a real app, redirect to Google's OAuth2 endpoint
    # For now, just redirect to a dummy dashboard
    return RedirectResponse(url="/dashboard")
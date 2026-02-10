# app/auth/oauth2.py
from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
import uuid

from app.config import settings
from app.database import get_db
from app.models import User

router = APIRouter()
oauth = OAuth()

# ------------------------
# Google OAuth2 Configuration
# ------------------------
CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
)

# ------------------------
# Login Route
# ------------------------
@router.get("/login", name="oauth2_login")
async def login(request: Request):
    """
    Redirect user to Google OAuth login page.
    Forces account selection every time.
    """
    redirect_uri = str(request.url_for("callback"))

    # Force Google to show account selection
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        prompt="select_account"  # Forces Gmail account selection
    )

# ------------------------
# Callback Route
# ------------------------
@router.get("/callback", name="callback")
async def callback(request: Request, db: Session = Depends(get_db)):
    """
    Handle Google OAuth2 callback:
    1. Exchange authorization code for access token
    2. Fetch user info from Google UserInfo endpoint
    3. Save new user info in DB (no update)
    4. Save minimal info in session
    5. Redirect to dashboard
    """
    try:
        # Exchange code for access token
        token = await oauth.google.authorize_access_token(request)

        # Fetch user info from Google
        userinfo_endpoint = "https://www.googleapis.com/oauth2/v3/userinfo"
        resp = await oauth.google.get(userinfo_endpoint, token=token)
        user_info = resp.json()

        email = user_info.get("email")
        name = user_info.get("name")
        provider_user_id = user_info.get("sub")  # Google unique ID

        if not email or not provider_user_id:
            return RedirectResponse(url="/?error=invalid_user_info")

        # Check if user already exists
        db_user = db.query(User).filter(User.provider_user_id == provider_user_id).first()

        if not db_user:
            # Save new user in database
            db_user = User(
                id=uuid.uuid4(),
                email=email,
                name=name,
                provider_user_id=provider_user_id
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

        # Save minimal info in session
        request.session["user"] = {"name": db_user.name, "email": db_user.email}

        # Redirect to dashboard
        return RedirectResponse(url="/dashboard")

    except Exception as e:
        # Log error for debugging
        print("OAuth callback error:", e)
        return RedirectResponse(url="/?error=oauth_failed")


# ------------------------
# Logout Route
# ------------------------
@router.get("/logout", name="logout")
async def logout(request: Request):
    """
    Clear session and redirect to login page.
    """
    request.session.pop("user", None)  # Remove user from session
    return RedirectResponse(url="/auth/login")
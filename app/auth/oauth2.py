from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
import uuid

from app.config import settings
from app.database import get_db
from app.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])
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
    client_kwargs={
        "scope": "openid email profile"
    },
)

# ------------------------
# Login Route
# ------------------------
@router.get("/login", name="google_login")
async def login(request: Request):
    """
    Redirect user to Google OAuth login page.
    """
    redirect_uri = settings.GOOGLE_REDIRECT_URI

    # DEBUG (remove later)
    print(">>> GOOGLE REDIRECT URI BEING SENT:", redirect_uri)

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        prompt="select_account"
    )

# ------------------------
# Callback Route
# ------------------------
@router.get("/callback", name="google_callback")
async def callback(request: Request, db: Session = Depends(get_db)):
    """
    Handle Google OAuth2 callback.
    """
    try:
        # Exchange authorization code for access token
        token = await oauth.google.authorize_access_token(request)

        # Fetch user info from Google
        resp = await oauth.google.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            token=token
        )
        user_info = resp.json()

        email = user_info.get("email")
        name = user_info.get("name")
        provider_user_id = user_info.get("sub")

        if not email or not provider_user_id:
            return RedirectResponse(url="/?error=invalid_user_info")

        # Check if user exists
        db_user = (
            db.query(User)
            .filter(User.provider_user_id == provider_user_id)
            .first()
        )

        if not db_user:
            db_user = User(
                id=uuid.uuid4(),
                email=email,
                name=name,
                provider_user_id=provider_user_id,
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

        # Save minimal session data
        request.session["user"] = {
            "id": str(db_user.id),
            "name": db_user.name,
            "email": db_user.email,
        }

        return RedirectResponse(url="/dashboard")

    except Exception as e:
        print("OAuth callback error:", e)
        return RedirectResponse(url="/?error=oauth_failed")

# ------------------------
# Logout Route
# ------------------------
@router.get("/logout", name="logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/auth/login")
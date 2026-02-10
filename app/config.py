# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ------------------------
    # Database
    # ------------------------
    DATABASE_URL: str

    # ------------------------
    # Google OAuth2
    # ------------------------
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str  # Must be full URL, e.g., http://localhost:8000/auth/callback

    # ------------------------
    # Session
    # ------------------------
    SESSION_SECRET_KEY: str  # Used for Starlette/FastAPI session middleware

    class Config:
        env_file = ".env"  # Load environment variables from .env
        env_file_encoding = "utf-8"
        extra = "forbid"  # Disallow any environment variable not declared here


# Instantiate settings object
settings = Settings()
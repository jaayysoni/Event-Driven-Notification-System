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
    GOOGLE_REDIRECT_URI: str  # e.g., http://localhost:8000/auth/callback

    # ------------------------
    # Session
    # ------------------------
    SESSION_SECRET_KEY: str  # Used for session middleware

    # ------------------------
    # SendGrid
    # ------------------------
    SENDGRID_API_KEY: str
    SENDGRID_TEMPLATE_ID: str
    FROM_EMAIL: str

    # ------------------------
    # RabbitMQ
    # ------------------------
    RABBITMQ_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "forbid"  # Strict validation (good practice)


# Instantiate settings object
settings = Settings()
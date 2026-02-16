# app/services/sendgrid_service.py

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()  # Load .env file

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID")
FROM_EMAIL = os.getenv("FROM_EMAIL")

if not SENDGRID_API_KEY:
    raise ValueError("❌ SENDGRID_API_KEY is not set in environment")
if not FROM_EMAIL:
    raise ValueError("❌ FROM_EMAIL is not set in environment")
if not TEMPLATE_ID:
    raise ValueError("❌ SENDGRID_TEMPLATE_ID is not set in environment")


def send_email(to_email: str, name: str):
    """
    Send an email using SendGrid dynamic template.
    """
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
    )
    message.template_id = TEMPLATE_ID
    message.dynamic_template_data = {"name": name}

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"✅ Email sent to {to_email}, Status Code: {response.status_code}")
    except Exception as e:
        print("❌ SendGrid Error:", e)
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID")
FROM_EMAIL = os.getenv("FROM_EMAIL")


def send_email(to_email: str, name: str):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
    )

    message.template_id = TEMPLATE_ID

    message.dynamic_template_data = {
        "name": name
    }

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print("Email sent:", response.status_code)
    except Exception as e:
        print("SendGrid Error:", str(e))
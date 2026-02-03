import os
from sendgrid import SendGridAPIClient # type: ignore
from sendgrid.helpers.mail import Mail # type: ignore

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

def send_email(to_email: str, event_type: str, payload: dict):
    subject = f"{event_type.replace('_', ' ').title()} Notification"
    content = f"""
    Hello {payload.get('name')},

    You have successfully {event_type.replace('_', ' ')} at {payload.get('time')}.
    """

    message = Mail(
        from_email="noreply@yourapp.com",
        to_emails=to_email,
        subject=subject,
        plain_text_content=content
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

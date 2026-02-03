from app.database import SessionLocal
from app.models import NotificationLog

def log_notification(email: str, event_type: str, status: bool, message: str = None):
    db = SessionLocal()
    try:
        log = NotificationLog(
            email=email,
            event_type=event_type,
            status=status,
            message=message
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        print(f"Logged notification for {email}: {event_type}, status={status}")
    except Exception as e:
        print(f"Error logging notification: {e}")
    finally:
        db.close()

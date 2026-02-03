from sqlalchemy import Column, Integer, String, DateTime, Boolean # type: ignore
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    status = Column(Boolean, default=True)  # success/failure
    timestamp = Column(DateTime, default=datetime.utcnow)
    message = Column(String, nullable=True)

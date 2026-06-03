from sqlalchemy import Column, String, Boolean, DateTime
from app.database import Base
from datetime import datetime
import uuid


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    display_name = Column(
        String(100)
    )

    firebase_uid = Column(
        String(128),
        unique=True,
        nullable=False
    )

    phone_verified = Column(
        Boolean,
        default=False
    )

    email_verified = Column(
        Boolean,
        default=False
    )
    role = Column(
    String(20),
    default="USER"
)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
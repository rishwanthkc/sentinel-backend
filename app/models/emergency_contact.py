from sqlalchemy import Column, Integer, String
from app.database import Base

class EmergencyContact(Base):

    __tablename__ = "emergency_contacts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_email = Column(String(255))

    contact_name = Column(String(255))

    contact_phone = Column(String(20))
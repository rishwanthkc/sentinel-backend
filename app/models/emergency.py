from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Double
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base

class Emergency(Base):

    __tablename__ = "emergencies"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_email = Column(
        String(255)
    )

    latitude = Column(
        Double
    )

    longitude = Column(
        Double
    )

    status = Column(
        String(50),
        default="ACTIVE"
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )
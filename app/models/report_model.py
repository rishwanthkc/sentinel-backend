from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Double
from sqlalchemy import Text
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.database import Base

class Report(Base):

    __tablename__ = "reports"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_email = Column(
        String(255)
    )

    report_type = Column(
        String(100)
    )

    severity = Column(
        Integer
    )

    latitude = Column(
        Double
    )

    longitude = Column(
        Double
    )

    description = Column(
        Text
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )
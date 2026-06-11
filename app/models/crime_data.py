from sqlalchemy import Column, Integer, String, Double
from app.database import Base


class CrimeData(Base):
    __tablename__ = "crime_data"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Double)
    longitude = Column(Double)
    severity = Column(Integer)        # 1 = low, 2 = medium, 3 = high
    category = Column(String(100))
    area = Column(String(150))

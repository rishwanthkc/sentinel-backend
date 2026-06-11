"""
Seeds the crime_data table with a sample dataset (Chennai) on first run.
Replace these points with a real crime dataset later — the safety engine
reads from this table plus live user reports.
"""
from sqlalchemy.orm import Session
from app.models.crime_data import CrimeData

# (latitude, longitude, severity, category, area)
SAMPLE_CRIME_POINTS = [
    (13.0674, 80.2376, 3, "Assault", "Kodambakkam"),
    (13.0418, 80.2341, 3, "Robbery", "Saidapet"),
    (13.0524, 80.2508, 2, "Harassment", "T. Nagar"),
    (13.0860, 80.2101, 3, "Theft", "Aminjikarai"),
    (13.1067, 80.2206, 2, "Chain Snatching", "Anna Nagar"),
    (13.0960, 80.2890, 2, "Harassment", "Royapuram"),
    (13.1185, 80.2574, 3, "Assault", "Madhavaram"),
    (13.0118, 80.2200, 2, "Theft", "Guindy"),
    (12.9914, 80.2181, 3, "Robbery", "Velachery"),
    (13.0331, 80.2700, 1, "Eve Teasing", "Mylapore"),
    (13.0569, 80.2425, 2, "Pickpocketing", "Nungambakkam"),
    (13.0780, 80.2600, 1, "Suspicious Activity", "Egmore"),
    (13.0405, 80.2520, 2, "Harassment", "Teynampet"),
    (13.0240, 80.2270, 3, "Assault", "Little Mount"),
    (13.1000, 80.2400, 2, "Theft", "Kilpauk"),
    (13.0890, 80.2480, 1, "Poor Lighting", "Purasawalkam"),
    (13.0600, 80.2150, 2, "Chain Snatching", "Vadapalani"),
    (13.0150, 80.2480, 3, "Robbery", "Adyar"),
    (12.9980, 80.2570, 2, "Harassment", "Thiruvanmiyur"),
    (13.1120, 80.2950, 3, "Assault", "Tondiarpet"),
    (13.0700, 80.2700, 1, "Suspicious Activity", "Chetpet"),
    (13.0480, 80.2680, 2, "Pickpocketing", "Triplicane"),
    (13.0330, 80.2410, 2, "Eve Teasing", "Kotturpuram"),
    (13.0820, 80.2300, 3, "Theft", "Shenoy Nagar"),
    (13.0950, 80.2150, 2, "Harassment", "Koyambedu"),
    (13.0260, 80.2090, 3, "Robbery", "Ekkattuthangal"),
    (13.0560, 80.2620, 1, "Poor Lighting", "Thousand Lights"),
    (13.1050, 80.2700, 2, "Chain Snatching", "Perambur"),
    (13.0440, 80.2460, 2, "Suspicious Activity", "CIT Nagar"),
    (13.0710, 80.2510, 1, "Eve Teasing", "Choolaimedu"),
]


def seed_crime_data(db: Session) -> int:
    """Insert sample points only if the table is empty. Returns rows added."""
    existing = db.query(CrimeData).count()
    if existing > 0:
        return 0
    for lat, lng, sev, cat, area in SAMPLE_CRIME_POINTS:
        db.add(
            CrimeData(
                latitude=lat,
                longitude=lng,
                severity=sev,
                category=cat,
                area=area,
            )
        )
    db.commit()
    return len(SAMPLE_CRIME_POINTS)

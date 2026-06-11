import os
import json
import urllib.parse
import urllib.request

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.crime_data import CrimeData
from app.models.report_model import Report
from app.utils.geo import decode_polyline, score_route, safety_score

router = APIRouter()

GOOGLE_KEY = os.getenv(
    "GOOGLE_MAPS_API_KEY",
    "AIzaSyAw2t6-3ZnOwc40vfrlGpL2F7C3XxKPdsM",
)
DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"


def load_risk_points(db: Session):
    """Combine the seeded crime dataset with live user reports."""
    points = []

    for c in db.query(CrimeData).all():
        points.append({
            "latitude": c.latitude,
            "longitude": c.longitude,
            "severity": c.severity or 1,
            "category": c.category,
            "source": "crime",
        })

    for r in db.query(Report).all():
        points.append({
            "latitude": r.latitude,
            "longitude": r.longitude,
            "severity": r.severity or 1,
            "category": r.report_type,
            "source": "report",
        })

    return points


@router.get("/risk-points")
def risk_points(db: Session = Depends(get_db)):
    return load_risk_points(db)


@router.get("/route")
def safe_route(
    origin: str = Query(..., description="address or 'lat,lng'"),
    destination: str = Query(..., description="address or 'lat,lng'"),
    mode: str = Query("driving"),
    db: Session = Depends(get_db),
):
    # 1. Fetch alternative routes from Google Directions.
    params = urllib.parse.urlencode({
        "origin": origin,
        "destination": destination,
        "alternatives": "true",
        "mode": mode,
        "key": GOOGLE_KEY,
    })
    try:
        with urllib.request.urlopen(
            f"{DIRECTIONS_URL}?{params}", timeout=15
        ) as resp:
            data = json.loads(resp.read().decode())
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Directions request failed: {exc}",
        )

    if data.get("status") != "OK" or not data.get("routes"):
        raise HTTPException(
            status_code=400,
            detail=f"No route found ({data.get('status')})",
        )

    # 2. Risk points = crime dataset + user reports.
    risk = load_risk_points(db)

    # 3. Decode + score each alternative.
    scored = []
    for route in data["routes"]:
        encoded = route["overview_polyline"]["points"]
        pts = decode_polyline(encoded)
        leg = route["legs"][0] if route.get("legs") else {}
        raw = score_route(pts, risk)
        scored.append({
            "polyline": encoded,
            "points": [[la, ln] for la, ln in pts],
            "risk_score": raw,
            "distance": (leg.get("distance") or {}).get("text", ""),
            "duration": (leg.get("duration") or {}).get("text", ""),
        })

    worst = max((s["risk_score"] for s in scored), default=0.0)
    for s in scored:
        s["safety_score"] = safety_score(s["risk_score"], worst)

    # 4. Safest = lowest raw risk.
    safest_index = min(
        range(len(scored)), key=lambda i: scored[i]["risk_score"]
    )
    for i, s in enumerate(scored):
        s["is_safest"] = (i == safest_index)

    return {
        "origin": origin,
        "destination": destination,
        "safest_index": safest_index,
        "routes": scored,
        "risk_points": risk,
    }

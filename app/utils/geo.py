"""Geo helpers for the safe-route engine: haversine, Google polyline
decoding, and risk scoring of a route against a set of risk points."""
import math
from typing import List, Tuple, Dict


def haversine_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Great-circle distance in metres."""
    r = 6371000.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lng2 - lng1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    )
    return 2 * r * math.asin(math.sqrt(a))


def decode_polyline(encoded: str) -> List[Tuple[float, float]]:
    """Decode a Google encoded polyline into [(lat, lng), ...]."""
    points: List[Tuple[float, float]] = []
    index = 0
    lat = 0
    lng = 0
    length = len(encoded)
    while index < length:
        for is_lng in (False, True):
            shift = 0
            result = 0
            while True:
                b = ord(encoded[index]) - 63
                index += 1
                result |= (b & 0x1F) << shift
                shift += 5
                if b < 0x20:
                    break
            delta = ~(result >> 1) if (result & 1) else (result >> 1)
            if is_lng:
                lng += delta
            else:
                lat += delta
        points.append((lat / 1e5, lng / 1e5))
    return points


# Risk points within this distance of a route count against it.
INFLUENCE_RADIUS_M = 250.0


def score_route(
    route: List[Tuple[float, float]],
    risk_points: List[Dict],
) -> float:
    """
    Raw risk score for a route. Each risk point near the route adds
    severity weight, decayed linearly by distance. Higher = more dangerous.
    """
    if not route:
        return 0.0
    total = 0.0
    for rp in risk_points:
        rlat = rp["latitude"]
        rlng = rp["longitude"]
        # nearest distance from this risk point to the route
        nearest = min(
            haversine_m(rlat, rlng, plat, plng) for plat, plng in route
        )
        if nearest <= INFLUENCE_RADIUS_M:
            proximity = 1.0 - (nearest / INFLUENCE_RADIUS_M)
            total += float(rp.get("severity", 1)) * proximity
    return round(total, 3)


def safety_score(raw_risk: float, worst: float) -> int:
    """Map a raw risk into a 0-100 safety score (higher = safer)."""
    if worst <= 0:
        return 100
    ratio = min(raw_risk / worst, 1.0)
    return int(round(100 - ratio * 100))

from fastapi import APIRouter
from contextlib import contextmanager

from app.database import get_connection

router = APIRouter()

@contextmanager
def db_connection():
    connection = get_connection()
    try:
        yield connection
    finally:
        connection.close()


@router.get("/stats")
def get_dashboard_stats():
    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM reports")
            total_reports = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM emergencies WHERE status='ACTIVE'"
            )
            active_emergencies = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM emergency_contacts")
            total_contacts = cursor.fetchone()[0]

            return {
                "total_users": total_users,
                "total_reports": total_reports,
                "active_emergencies": active_emergencies,
                "total_contacts": total_contacts
            }


@router.get("/reports")
def dashboard_reports():
    with db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(
                """
                SELECT *
                FROM reports
                ORDER BY created_at DESC
                """
            )
            return cursor.fetchall()


@router.get("/emergencies")
def dashboard_emergencies():
    with db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(
                """
                SELECT *
                FROM emergencies
                ORDER BY created_at DESC
                """
            )
            return cursor.fetchall()


@router.get("/users")
def dashboard_users():
    with db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(
                """
                SELECT *
                FROM users
                ORDER BY created_at DESC
                """
            )
            return cursor.fetchall()


@router.get("/analytics")
def get_analytics():
    with db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT
                    report_type,
                    COUNT(*) as total
                FROM reports
                GROUP BY report_type
                ORDER BY total DESC
            """)
            incident_types = cursor.fetchall()
            return {
                "incident_types": incident_types
            }


@router.get("/hotspots")
def get_hotspots():
    with db_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT
                    latitude,
                    longitude,
                    severity,
                    report_type
                FROM reports
                ORDER BY severity DESC
            """)
            hotspots = cursor.fetchall()

            for hotspot in hotspots:
                hotspot["risk_score"] = hotspot["severity"] * 30

            return hotspots


@router.post("/resolve/{id}")
def resolve_emergency(id: int):
    with db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE emergencies
                SET status='RESOLVED'
                WHERE id=%s
                """,
                (id,)
            )
            connection.commit()
            return {
                "message": "Emergency Resolved"
            }

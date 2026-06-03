from fastapi import APIRouter
from sqlalchemy import text

from app.database import get_connection

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )
    total_users = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM reports"
    )
    total_reports = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM emergencies

        WHERE status='ACTIVE'
        """
    )
    active_emergencies = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM emergency_contacts
        """
    )
    total_contacts = cursor.fetchone()[0]

    cursor.close()

    connection.close()

    return {

        "total_users":
            total_users,

        "total_reports":
            total_reports,

        "active_emergencies":
            active_emergencies,

        "total_contacts":
            total_contacts
    }

@router.get("/reports")
def dashboard_reports():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *

        FROM reports

        ORDER BY created_at DESC
        """
    )

    reports = cursor.fetchall()

    cursor.close()
    connection.close()

    return reports

@router.get("/emergencies")
def dashboard_emergencies():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *

        FROM emergencies

        ORDER BY created_at DESC
        """
    )

    emergencies = cursor.fetchall()

    cursor.close()
    connection.close()

    return emergencies

@router.get("/users")
def dashboard_users():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *

        FROM users

        ORDER BY created_at DESC
        """
    )

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return users


@router.get("/analytics")
def get_analytics():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            report_type,
            COUNT(*) as total
        FROM reports
        GROUP BY report_type
        ORDER BY total DESC
    """)

    incident_types = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "incident_types": incident_types
    }

@router.get("/hotspots")
def get_hotspots():

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

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

        hotspot["risk" \
        "_score"] = (
            hotspot["severity"] * 30
        )

    cursor.close()
    connection.close()

    return hotspots 


@router.post("/resolve/{id}")
def resolve_emergency(id: int):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE emergencies
        SET status='RESOLVED'
        WHERE id=%s
        """,
        (id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Emergency Resolved"
    }

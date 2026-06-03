from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db


from app.database import get_connection
from app.models.emergency_model import EmergencyRequest



router = APIRouter()

@router.post("/trigger")

def trigger_emergency(
    request: EmergencyRequest
):

    connection = get_connection()

    cursor = connection.cursor()

    query = """
    INSERT INTO emergencies
    (
        user_email,
        latitude,
        longitude,
        status
    )
    VALUES (%s,%s,%s,%s)
    """

    values = (
        request.user_email,
        request.latitude,
        request.longitude,
        "ACTIVE"
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()

    connection.close()

    return {
        "message":
            "Emergency Triggered"
    }


@router.get("/history/{email}")

def get_history(

    email: str,

    db: Session = Depends(get_db)
):

    history = db.execute(

        text("""

        SELECT *

        FROM emergencies

        WHERE user_email = :email

        ORDER BY created_at DESC

        """),

        {
            "email": email
        }

    ).mappings().all()

    return history

@router.post("/resolve/{emergency_id}")
def resolve_emergency(
    emergency_id: int
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE emergencies
        SET status='RESOLVED'
        WHERE id=%s
        """,
        (emergency_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Emergency Resolved"
    }


@router.get("/active")
def get_active_emergencies(
    db: Session = Depends(get_db)
):

    query = text(
        """
        SELECT
            id,
            latitude,
            longitude,
            user_email,
            created_at

        FROM emergencies

        WHERE status='ACTIVE'

        ORDER BY created_at DESC
        """
    )

    result = db.execute(query)

    emergencies = []

    for row in result:

        emergencies.append({
            "id": row[0],
            "latitude": row[1],
            "longitude": row[2],
            "user_email": row[3],
            "created_at": str(row[4])
        })

    return emergencies
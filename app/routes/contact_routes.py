from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.emergency_contact import EmergencyContact
from app.schemas.emergency_contact_schema import EmergencyContactCreate

router = APIRouter()


@router.post("/add")

def add_contact(

    request: EmergencyContactCreate,

    db: Session = Depends(get_db)
):

    new_contact = EmergencyContact(

        user_email =
            request.user_email,

        contact_name =
            request.contact_name,

        contact_phone =
            request.contact_phone
    )

    db.add(new_contact)

    db.commit()

    db.refresh(new_contact)

    return {
        "message": "Contact Added"
    }


@router.get("/{user_email}")

def get_contacts(

    user_email: str,

    db: Session = Depends(get_db)
):

    contacts = db.query(
        EmergencyContact
    ).filter(

        EmergencyContact.user_email
        == user_email

    ).all()

    return contacts
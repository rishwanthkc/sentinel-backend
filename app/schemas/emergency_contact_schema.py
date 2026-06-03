from pydantic import BaseModel

class EmergencyContactCreate(BaseModel):

    user_email: str

    contact_name: str

    contact_phone: str
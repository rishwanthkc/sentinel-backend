from pydantic import BaseModel

class EmergencyRequest(BaseModel):

    user_email: str
    latitude: float
    longitude: float
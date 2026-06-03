from pydantic import BaseModel

class ReportCreate(BaseModel):

    user_email: str

    report_type: str

    severity: int

    latitude: float

    longitude: float

    description: str
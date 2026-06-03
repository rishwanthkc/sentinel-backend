from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    email: str
    display_name: Optional[str] = None
    firebase_uid: str
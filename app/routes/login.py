from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User

router = APIRouter()


class LoginRequest(BaseModel):
    email: str


@router.post("/login")
def login_user(data: LoginRequest, db: Session = Depends(get_db)):

    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "Login successful",
        "user_id": user.user_id,
        "display_name": user.display_name,
        "email": user.email,
        "role": user.role
    }
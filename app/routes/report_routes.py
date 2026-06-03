from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.report_model import Report

from app.schemas.report_schema import ReportCreate

router = APIRouter()


@router.post("/submit")

def submit_report(

    request: ReportCreate,

    db: Session = Depends(get_db)
):

    report = Report(

        user_email =
            request.user_email,

        report_type =
            request.report_type,

        severity =
            request.severity,

        latitude =
            request.latitude,

        longitude =
            request.longitude,

        description =
            request.description
    )

    db.add(report)

    db.commit()

    db.refresh(report)

    return {
        "message": "Report Submitted"
    }


@router.get("/all")

def get_reports(

    db: Session = Depends(get_db)
):

    reports = db.query(
        Report
    ).all()

    return reports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base

# Import every ORM model so Base.metadata.create_all() builds all tables
# (users, reports, emergencies, emergency_contacts) on a fresh database.
from app.models.user import User
from app.models.report_model import Report
from app.models.emergency import Emergency
from app.models.emergency_contact import EmergencyContact

from app.routes.auth import router as auth_router
from app.routes.login import router as login_router
from app.routes.emergency_routes import router as emergency_router
from app.routes.contact_routes import router as contact_router
from app.routes.report_routes import router as report_router
from app.routes.dashboard_routes import router as dashboard_router

app = FastAPI(title="SENTINEL Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all tables on startup.
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "SENTINEL Backend Running"}


@app.get("/health")
def health():
    return {"status": "ok"}


# AUTH ROUTES
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(login_router, prefix="/auth", tags=["Authentication"])

# EMERGENCY ROUTES
app.include_router(emergency_router, prefix="/emergency", tags=["Emergency"])
app.include_router(contact_router, prefix="/contacts", tags=["Emergency Contacts"])

# REPORTS
app.include_router(report_router, prefix="/reports", tags=["Reports"])

# DASHBOARD
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])

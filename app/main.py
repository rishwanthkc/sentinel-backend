from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base, SessionLocal

# Import every ORM model so Base.metadata.create_all() builds all tables.
from app.models.user import User
from app.models.report_model import Report
from app.models.emergency import Emergency
from app.models.emergency_contact import EmergencyContact
from app.models.crime_data import CrimeData

from app.routes.auth import router as auth_router
from app.routes.login import router as login_router
from app.routes.emergency_routes import router as emergency_router
from app.routes.contact_routes import router as contact_router
from app.routes.report_routes import router as report_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.safety_routes import router as safety_router

from app.utils.seed_crime import seed_crime_data

app = FastAPI(title="SENTINEL Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all tables, then seed the sample crime dataset (once).
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def _seed():
    db = SessionLocal()
    try:
        added = seed_crime_data(db)
        if added:
            print(f"[seed] inserted {added} sample crime points")
    except Exception as exc:
        print(f"[seed] skipped: {exc}")
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "SENTINEL Backend Running"}


@app.get("/health")
def health():
    return {"status": "ok"}


# AUTH
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(login_router, prefix="/auth", tags=["Authentication"])

# EMERGENCY
app.include_router(emergency_router, prefix="/emergency", tags=["Emergency"])
app.include_router(contact_router, prefix="/contacts", tags=["Emergency Contacts"])

# REPORTS
app.include_router(report_router, prefix="/reports", tags=["Reports"])

# DASHBOARD
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])

# SAFE ROUTING
app.include_router(safety_router, prefix="/safety", tags=["Safe Routing"])

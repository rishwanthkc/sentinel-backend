from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base

from app.models.user import User

from app.routes.auth import router as auth_router
from app.routes.login import router as login_router
from app.routes.emergency_routes import router as emergency_router
from app.routes.contact_routes import router as contact_router
from app.routes.report_routes import router as report_router
from app.routes.dashboard_routes import router as dashboard_router
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

# AUTH ROUTES
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

# LOGIN ROUTES
app.include_router(
    login_router,
    prefix="/auth",
    tags=["Authentication"]
)

# EMERGENCY ROUTES
app.include_router(
    emergency_router,
    prefix="/emergency",
    tags=["Emergency"]
)

app.include_router(
    contact_router,
    prefix="/contacts",
    tags=["Emergency Contacts"]
)


@app.get("/")
def root():
    return {
        "message": "SENTINEL Backend Running"
    }


app.include_router(
    report_router,
    prefix="/reports",
    tags=["Reports"]
)

app.include_router(

    dashboard_router,

    prefix="/dashboard",

    tags=["Dashboard"]
)
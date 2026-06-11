import os
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv
import mysql.connector

load_dotenv()

# --- Database connection settings (from environment) ---
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Managed providers (e.g. Aiven) require TLS. Paste the provider's CA
# certificate into the DB_CA_CERT env var; we write it to a temp file and
# use it for both SQLAlchemy (PyMySQL) and the raw mysql.connector pool.
# If DB_CA_CERT is empty (e.g. local MySQL), connections stay plain.
DB_CA_CERT = os.getenv("DB_CA_CERT")

_ca_path = None
if DB_CA_CERT:
    _ca_path = os.path.join(tempfile.gettempdir(), "sentinel_db_ca.pem")
    with open(_ca_path, "w") as _f:
        _f.write(DB_CA_CERT.replace("\\n", "\n"))

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# SSL args for SQLAlchemy / PyMySQL.
_engine_connect_args = {}
if _ca_path:
    _engine_connect_args = {"ssl": {"ca": _ca_path}}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args=_engine_connect_args,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_connection():
    kwargs = dict(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    if _ca_path:
        kwargs["ssl_ca"] = _ca_path
    return mysql.connector.connect(**kwargs)

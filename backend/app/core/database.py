"""
Database Engine, Session Management, and Base Declarative Setup
Handles connection pooling, session lifecycle, and cross-database compatibility (PostgreSQL / SQLite).
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.core.config import settings

# Configure SQLite pragmas for foreign keys if using SQLite
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """FastAPI dependency to yield thread-safe database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create all tables defined in ORM models."""
    from backend.app import models # noqa: F401
    Base.metadata.create_all(bind=engine)

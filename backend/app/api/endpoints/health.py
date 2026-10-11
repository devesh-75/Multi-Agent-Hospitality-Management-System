"""
Health & System Status Endpoint
Verifies database connectivity, table counts, and infrastructure components.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any

from backend.app.core.database import get_db
from backend.app.core.config import settings
from backend.app.models.entities import Property, Reservation, Invoice, Expense, Competitor

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    # Test DB
    db_connected = False
    table_counts = {}
    try:
        db.execute(text("SELECT 1"))
        db_connected = True
        table_counts = {
            "properties": db.query(Property).count(),
            "reservations": db.query(Reservation).count(),
            "invoices": db.query(Invoice).count(),
            "expenses": db.query(Expense).count(),
            "competitors": db.query(Competitor).count(),
        }
    except Exception as e:
        db_connected = False

    return {
        "status": "healthy" if db_connected else "degraded",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": {
            "connected": db_connected,
            "engine": settings.DATABASE_URL.split(":")[0],
            "record_counts": table_counts
        },
        "kafka": {
            "enabled": settings.KAFKA_ENABLED,
            "bootstrap_servers": settings.KAFKA_BOOTSTRAP_SERVERS,
            "mode": "Live Cluster" if settings.KAFKA_ENABLED else "Development Mode (Database Event Queue)"
        },
        "qdrant": {
            "enabled": settings.QDRANT_ENABLED,
            "url": settings.QDRANT_URL,
            "mode": "Remote Vector Store" if settings.QDRANT_ENABLED else "Local In-Memory Vector Store"
        }
    }

"""
Occupancy Analytics Endpoints
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List

from backend.app.core.database import get_db
from backend.app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/occupancy", tags=["Occupancy"])

@router.get("", response_model=Dict[str, Any])
def get_occupancy_overview(
    property_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    kpis = AnalyticsService.get_executive_kpis(db, property_id)
    time_series = AnalyticsService.get_occupancy_time_series(db, property_id)

    return {
        "property_id": property_id or "ALL",
        "current_occupancy_rate_pct": kpis["occupancy_rate_pct"],
        "total_rooms": kpis["total_rooms"],
        "time_series": time_series
    }

"""
Revenue Analytics Endpoints
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List

from backend.app.core.database import get_db
from backend.app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/revenue", tags=["Revenue"])

@router.get("", response_model=Dict[str, Any])
def get_revenue_summary(
    property_id: Optional[str] = Query(None, description="Optional property filter"),
    db: Session = Depends(get_db)
):
    kpis = AnalyticsService.get_executive_kpis(db, property_id)
    time_series = AnalyticsService.get_revenue_time_series(db, property_id)
    comparison = AnalyticsService.get_property_comparison(db) if not property_id else []
    forecast = AnalyticsService.get_forecast(db, property_id)

    return {
        "kpis": kpis,
        "time_series": time_series,
        "property_comparison": comparison,
        "forecast": forecast
    }

@router.get("/comparison", response_model=List[Dict[str, Any]])
def get_property_revenue_comparison(db: Session = Depends(get_db)):
    return AnalyticsService.get_property_comparison(db)

@router.get("/forecast", response_model=Dict[str, Any])
def get_revenue_forecast(
    property_id: Optional[str] = Query(None),
    horizon_days: int = Query(14, ge=7, le=60),
    db: Session = Depends(get_db)
):
    return AnalyticsService.get_forecast(db, property_id, horizon_days)

"""
Reporting Endpoints
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List

from backend.app.core.database import get_db
from agents.reporting_agent import ReportingAgent

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("", response_model=List[Dict[str, Any]])
def list_reports(
    property_id: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    agent = ReportingAgent(db)
    return agent.list_reports(property_id=property_id, limit=limit)

@router.post("/generate", response_model=Dict[str, Any])
def generate_report(
    report_type: str = Query("CONSOLIDATED_EXECUTIVE", description="DAILY_OPERATIONS, REVENUE_ANALYSIS, RECONCILIATION_EXCEPTION, CONSOLIDATED_EXECUTIVE"),
    property_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    agent = ReportingAgent(db)
    return agent.generate_report(report_type=report_type, property_id=property_id)

"""
Reconciliation Endpoints
Provides ledger auditing and triggers the Reconciliation Agent.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from backend.app.core.database import get_db
from agents.reconciliation_agent import ReconciliationAgent

router = APIRouter(prefix="/reconciliation", tags=["Reconciliation"])

@router.get("", response_model=Dict[str, Any])
def get_reconciliation_status(
    property_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    agent = ReconciliationAgent(db)
    return agent.run_reconciliation(property_id=property_id)

@router.post("/run", response_model=Dict[str, Any])
def trigger_reconciliation_agent(
    property_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    agent = ReconciliationAgent(db)
    return agent.run_reconciliation(property_id=property_id)

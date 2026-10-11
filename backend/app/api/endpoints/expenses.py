"""
Expense Tracking Endpoints
Audits departmental spend and runs Expense Agent anomaly detection.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List

from backend.app.core.database import get_db
from backend.app.schemas.dto import ExpenseSchema
from backend.app.models.entities import Expense
from agents.expense_agent import ExpenseAgent

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.get("", response_model=Dict[str, Any])
def get_expenses_analysis(
    property_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    agent = ExpenseAgent(db)
    return agent.run_expense_audit(property_id=property_id)

@router.get("/list", response_model=List[ExpenseSchema])
def list_raw_expenses(
    property_id: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Expense)
    if property_id:
        query = query.filter(Expense.property_id == property_id)
    if category:
        query = query.filter(Expense.category == category)
    return query.offset(offset).limit(limit).all()

@router.post("/run", response_model=Dict[str, Any])
def trigger_expense_agent(
    property_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    agent = ExpenseAgent(db)
    return agent.run_expense_audit(property_id=property_id)

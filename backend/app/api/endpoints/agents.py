"""
Agent Orchestration Endpoints
Invokes the LangGraph multi-agent pipeline and retrieves agent execution history.
"""

from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List

from backend.app.core.database import get_db
from backend.app.models.entities import AgentRun
from agents.workflow import HospitalityAgentWorkflow

router = APIRouter(prefix="/agents", tags=["Agent Orchestration"])

@router.post("/run", response_model=Dict[str, Any])
def run_agents(
    property_id: Optional[str] = Query(None, description="Optional property filter"),
    agent: Optional[str] = Query("all", description="Specific agent: reconciliation, expense, revenue, reporting, bde, or all"),
    query: str = Body("Run complete multi-agent hospitality operations and competitive intelligence audit", embed=True),
    db: Session = Depends(get_db)
):
    workflow = HospitalityAgentWorkflow(db)
    result = workflow.run({
        "query": query,
        "property_id": property_id,
        "requested_agent": agent if agent != "all" else None
    })
    return {
        "execution_time_ms": result.get("execution_time_ms", 0),
        "property_id": property_id or "ALL",
        "final_response": result.get("final_response"),
        "reconciliation": result.get("reconciliation_data"),
        "expense": result.get("expense_data"),
        "revenue": result.get("revenue_data"),
        "reporting": result.get("reporting_data"),
        "bde": result.get("bde_data"),
        "audit_trail": result.get("audit_trail", [])
    }

@router.get("/runs", response_model=List[Dict[str, Any]])
def list_agent_runs(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    runs = db.query(AgentRun).order_by(AgentRun.started_at.desc()).limit(limit).all()
    return [{
        "id": r.id,
        "agent_name": r.agent_name,
        "property_id": r.property_id,
        "status": r.status,
        "execution_time_ms": r.execution_time_ms,
        "result_summary": r.result_summary,
        "started_at": r.started_at.isoformat() if r.started_at else None,
        "completed_at": r.completed_at.isoformat() if r.completed_at else None
    } for r in runs]

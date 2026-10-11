"""
Competitor Intelligence & Business Development Executive (BDE) Endpoints
Implements Section 14.10 API specifications.
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List

from backend.app.core.database import get_db
from backend.app.schemas.dto import CompetitorSchema, AskRequest, AskResponse
from backend.app.models.entities import Competitor, Alert
from agents.bde_agent import BDEAgent

router = APIRouter(tags=["Business Development & Competitors"])

@router.get("/competitors", response_model=List[CompetitorSchema])
def list_competitors(
    property_id: Optional[str] = Query(None, description="Target hotel property code (BER, LND, MUC, PAR, VIE)"),
    db: Session = Depends(get_db)
):
    query = db.query(Competitor)
    if property_id:
        query = query.filter(Competitor.target_property_id == property_id)
    return query.all()

@router.get("/competitors/{competitor_id}", response_model=CompetitorSchema)
def get_competitor(competitor_id: str, db: Session = Depends(get_db)):
    c = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return c

@router.get("/competitor-comparison", response_model=Dict[str, Any])
def get_competitor_comparison(
    property_id: str = Query("BER", description="Our property ID for competitive benchmarking"),
    db: Session = Depends(get_db)
):
    agent = BDEAgent(db)
    return agent.compare_property_with_competitors(property_id=property_id)

@router.get("/competitive-gaps", response_model=List[Dict[str, Any]])
def get_competitive_gaps(
    property_id: str = Query("BER", description="Our property ID"),
    db: Session = Depends(get_db)
):
    agent = BDEAgent(db)
    return agent.analyze_feature_gaps(property_id=property_id)

@router.get("/competitive-trends", response_model=Dict[str, Any])
def get_competitive_trends(
    property_id: str = Query("BER", description="Our property ID"),
    db: Session = Depends(get_db)
):
    agent = BDEAgent(db)
    return agent.analyze_price_trends(property_id=property_id)

@router.get("/competitive-alerts", response_model=List[Dict[str, Any]])
def get_competitive_alerts(
    property_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Alert).filter(Alert.alert_type.in_(["COMPETITOR_PRICE_DROP", "AMENITY_GAP", "EXPENSE_ANOMALY"]))
    if property_id:
        query = query.filter(Alert.property_id == property_id)
    alerts = query.all()
    return [{
        "id": a.id,
        "title": a.title,
        "severity": a.severity,
        "message": a.message,
        "evidence": a.evidence,
        "created_at": a.created_at.isoformat()
    } for a in alerts]

@router.get("/business-opportunities", response_model=List[Dict[str, Any]])
def get_business_growth_opportunities(
    property_id: str = Query("BER", description="Target property ID"),
    db: Session = Depends(get_db)
):
    agent = BDEAgent(db)
    return agent.generate_growth_opportunities(property_id=property_id)

@router.get("/swot-analysis", response_model=Dict[str, Any])
def get_swot_analysis(
    property_id: str = Query("BER", description="Target property ID"),
    db: Session = Depends(get_db)
):
    agent = BDEAgent(db)
    return agent.generate_swot_analysis(property_id=property_id)

@router.post("/bde/ask", response_model=Dict[str, Any])
def ask_bde_agent(
    req: AskRequest,
    db: Session = Depends(get_db)
):
    agent = BDEAgent(db)
    return agent.ask_bde(question=req.question, property_id=req.property_id)

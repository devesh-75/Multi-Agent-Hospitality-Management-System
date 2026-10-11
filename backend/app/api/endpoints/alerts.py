"""
Operational Alerts Endpoints
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List

from backend.app.core.database import get_db
from backend.app.models.entities import Alert

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("", response_model=List[Dict[str, Any]])
def list_alerts(
    property_id: Optional[str] = Query(None),
    unresolved_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    query = db.query(Alert)
    if unresolved_only:
        query = query.filter(Alert.is_resolved == False)
    if property_id:
        query = query.filter(Alert.property_id == property_id)
    alerts = query.order_by(Alert.created_at.desc()).all()
    return [{
        "id": a.id,
        "alert_type": a.alert_type,
        "severity": a.severity,
        "property_id": a.property_id,
        "title": a.title,
        "message": a.message,
        "evidence": a.evidence,
        "is_resolved": a.is_resolved,
        "created_at": a.created_at.isoformat()
    } for a in alerts]

@router.post("/{alert_id}/resolve", response_model=Dict[str, Any])
def resolve_alert(alert_id: str, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.is_resolved = True
    db.commit()
    return {"status": "SUCCESS", "alert_id": alert_id, "is_resolved": True}

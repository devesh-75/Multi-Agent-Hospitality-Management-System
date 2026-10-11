"""
Reservations Endpoints
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.core.database import get_db
from backend.app.models.entities import Reservation
from backend.app.schemas.dto import ReservationSchema

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.get("", response_model=List[ReservationSchema])
def list_reservations(
    property_id: Optional[str] = Query(None, description="Filter by property ID (BER, LND, MUC, PAR, VIE)"),
    status: Optional[str] = Query(None, description="Filter by status (Confirmed, InHouse, CheckedOut)"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Reservation)
    if property_id:
        query = query.filter(Reservation.property_id == property_id)
    if status:
        query = query.filter(Reservation.status == status)
    return query.offset(offset).limit(limit).all()

@router.get("/{reservation_id}", response_model=ReservationSchema)
def get_reservation(reservation_id: str, db: Session = Depends(get_db)):
    res = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return res

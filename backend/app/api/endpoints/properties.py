"""
Properties Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.core.database import get_db
from backend.app.models.entities import Property, Room
from backend.app.schemas.dto import PropertySchema

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.get("", response_model=List[PropertySchema])
def list_properties(db: Session = Depends(get_db)):
    return db.query(Property).all()

@router.get("/{property_id}", response_model=PropertySchema)
def get_property(property_id: str, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail=f"Property {property_id} not found")
    return prop

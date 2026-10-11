"""
Invoices & Payments Endpoints
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.core.database import get_db
from backend.app.models.entities import Invoice, Payment
from backend.app.schemas.dto import InvoiceSchema, PaymentSchema

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.get("", response_model=List[InvoiceSchema])
def list_invoices(
    property_id: Optional[str] = Query(None),
    settled: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Invoice)
    if property_id:
        query = query.filter(Invoice.property_id == property_id)
    if settled is not None:
        query = query.filter(Invoice.payment_settled == settled)
    return query.offset(offset).limit(limit).all()

@router.get("/{invoice_id}", response_model=InvoiceSchema)
def get_invoice(invoice_id: str, db: Session = Depends(get_db)):
    inv = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv

@router.get("/payments/list", response_model=List[PaymentSchema])
def list_payments(
    property_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Payment)
    if property_id:
        query = query.filter(Payment.property_id == property_id)
    return query.offset(offset).limit(limit).all()

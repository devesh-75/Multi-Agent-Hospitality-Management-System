"""
Pydantic Data Transfer Objects (Schemas)
Provides strict validation, serialization, and typing across API endpoints and agents.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime

# Property Schemas
class PropertySchema(BaseModel):
    id: str
    code: str
    company_name: str
    name: str
    status: str
    country_code: str
    timezone: str
    currency: str
    created_at: Optional[datetime] = None
    is_synthetic: bool = False

    class Config:
        from_attributes = True

# Reservation Schemas
class ReservationSchema(BaseModel):
    id: str
    booking_id: str
    property_id: str
    room_id: Optional[str] = None
    room_type_id: Optional[str] = None
    guest_id: Optional[str] = None
    status: str
    arrival_date: datetime
    departure_date: datetime
    adults: int
    channel_code: str
    total_gross_amount: float
    balance: float
    guarantee_type: str
    has_city_tax: bool
    is_synthetic: bool = False

    class Config:
        from_attributes = True

# Invoice Schemas
class InvoiceItemSchema(BaseModel):
    id: str
    description: str
    quantity: float
    unit_price: float
    amount: float

    class Config:
        from_attributes = True

class InvoiceSchema(BaseModel):
    id: str
    invoice_number: str
    property_id: str
    reservation_id: Optional[str] = None
    status: str
    payment_settled: bool
    total_amount: float
    outstanding_balance: float
    invoice_date: date
    currency: str
    is_synthetic: bool = False
    items: List[InvoiceItemSchema] = []

    class Config:
        from_attributes = True

# Payment Schemas
class PaymentSchema(BaseModel):
    id: str
    reservation_id: str
    property_id: str
    payment_method: str
    amount: float
    payment_date: date
    currency: str
    transaction_reference: Optional[str] = None
    status: str
    is_synthetic: bool = False

    class Config:
        from_attributes = True

# Expense Schemas
class ExpenseSchema(BaseModel):
    id: str
    property_id: str
    category: str
    vendor_name: str
    description: Optional[str] = None
    amount: float
    currency: str
    expense_date: date
    status: str
    is_synthetic: bool = True

    class Config:
        from_attributes = True

# Reconciliation Schemas
class InvoicePaymentDiscrepancy(BaseModel):
    invoice_id: str
    invoice_number: str
    reservation_id: str
    property_id: str
    invoice_total: float
    payments_total: float
    difference: float
    status: str # FULLY_PAID, PARTIALLY_PAID, UNPAID, OVERPAID
    payment_records_count: int
    recommended_action: str

class OTASettlementDiscrepancy(BaseModel):
    settlement_id: str
    channel_name: str
    ota_reservation_id: str
    reservation_id: str
    property_id: str
    gross_amount: float
    expected_settlement: float
    actual_settlement: Optional[float] = None
    difference: float
    status: str
    scenario: str
    recommended_action: str

class ReconciliationAuditReport(BaseModel):
    timestamp: datetime
    property_id: Optional[str] = None
    total_invoices_audited: int
    fully_paid_count: int
    partially_paid_count: int
    unpaid_count: int
    overpaid_count: int
    total_discrepancy_amount: float
    invoice_exceptions: List[InvoicePaymentDiscrepancy]
    ota_exceptions: List[OTASettlementDiscrepancy]

# Competitor Intelligence Schemas
class CompetitorSchema(BaseModel):
    id: str
    name: str
    brand: Optional[str] = None
    city: str
    country_code: str
    star_rating: float
    distance_km: float
    target_property_id: Optional[str] = None
    is_synthetic: bool = True

    class Config:
        from_attributes = True

class FeatureGapItem(BaseModel):
    feature_name: str
    category: str
    our_property_status: str
    competitors_offering: List[str]
    competitor_count: int
    opportunity_severity: str
    recommended_action: str

class CompetitorPriceComparison(BaseModel):
    competitor_id: str
    competitor_name: str
    city: str
    avg_price: float
    min_price: float
    max_price: float
    our_avg_price: float
    price_difference: float
    price_difference_pct: float

class SWOTReport(BaseModel):
    property_id: str
    property_name: str
    generated_at: datetime
    strengths: List[Dict[str, Any]]
    weaknesses: List[Dict[str, Any]]
    opportunities: List[Dict[str, Any]]
    threats: List[Dict[str, Any]]

class GrowthOpportunity(BaseModel):
    id: str
    title: str
    category: str # PRICING, AMENITY, CHANNEL, OPERATIONAL
    observation: str
    evidence: Dict[str, Any]
    business_opportunity: str
    recommended_action: str
    expected_impact: str
    confidence_level: str # HIGH, MEDIUM, LOW
    data_limitations: str
    human_validation_required: str

# Natural Language Question / Answer
class AskRequest(BaseModel):
    question: str
    property_id: Optional[str] = None

class AskResponse(BaseModel):
    question: str
    answer: str
    sources: List[str] = []
    structured_data: Optional[Dict[str, Any]] = None
    confidence: str = "HIGH"
    data_limitations: Optional[str] = None

"""
SQLAlchemy ORM Entities for Unified Hospitality Data Model
"""

from sqlalchemy import (
    Column, String, Integer, Numeric, Boolean, Date, DateTime, Text, JSON, ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.core.database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(String(16), primary_key=True)
    code = Column(String(16), nullable=False)
    company_name = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    status = Column(String(32), default="Active")
    is_archived = Column(Boolean, default=False)
    country_code = Column(String(2), nullable=False)
    timezone = Column(String(64), nullable=False)
    currency = Column(String(3), default="EUR")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_synthetic = Column(Boolean, default=False)
    source_file = Column(String(64), default="properties.csv")

    rooms = relationship("Room", back_populates="property")
    reservations = relationship("Reservation", back_populates="property")
    invoices = relationship("Invoice", back_populates="property")
    expenses = relationship("Expense", back_populates="property")


class RoomType(Base):
    __tablename__ = "room_types"

    id = Column(String(64), primary_key=True)
    code = Column(String(32), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    category = Column(String(64), default="BedRoom")
    property_id = Column(String(16), ForeignKey("properties.id"))


class Room(Base):
    __tablename__ = "rooms"

    id = Column(String(64), primary_key=True)
    room_number = Column(String(32), nullable=False)
    description = Column(String(255))
    room_type_id = Column(String(64), ForeignKey("room_types.id"))
    property_id = Column(String(16), ForeignKey("properties.id"))

    property = relationship("Property", back_populates="rooms")


class Guest(Base):
    __tablename__ = "guests"

    id = Column(String(64), primary_key=True)
    first_name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(255), index=True)
    phone = Column(String(64))
    address = Column(String(255))
    postal_code = Column(String(32))
    city = Column(String(128))
    country_code = Column(String(2))


class RatePlan(Base):
    __tablename__ = "rate_plans"

    id = Column(String(64), primary_key=True)
    code = Column(String(32), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    property_id = Column(String(16), ForeignKey("properties.id"))


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(String(64), primary_key=True)
    external_id = Column(String(64))
    booking_id = Column(String(32), nullable=False, index=True)
    property_id = Column(String(16), ForeignKey("properties.id"), nullable=False, index=True)
    room_id = Column(String(64), ForeignKey("rooms.id"))
    room_type_id = Column(String(64), ForeignKey("room_types.id"))
    guest_id = Column(String(64), ForeignKey("guests.id"))
    rate_plan_id = Column(String(64), ForeignKey("rate_plans.id"))
    status = Column(String(32), nullable=False, index=True) # InHouse, CheckedOut, Confirmed, Cancelled
    arrival_date = Column(DateTime, nullable=False, index=True)
    departure_date = Column(DateTime, nullable=False, index=True)
    adults = Column(Integer, default=1)
    channel_code = Column(String(32), default="Direct")
    total_gross_amount = Column(Numeric(12, 2), default=0.00)
    balance = Column(Numeric(12, 2), default=0.00)
    guarantee_type = Column(String(32), default="CreditCard")
    has_city_tax = Column(Boolean, default=False)
    is_open_for_charges = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime)
    is_synthetic = Column(Boolean, default=False)
    source_file = Column(String(64), default="reservations.csv")

    property = relationship("Property", back_populates="reservations")


class Folio(Base):
    __tablename__ = "folios"

    id = Column(String(64), primary_key=True)
    external_id = Column(String(64))
    reservation_id = Column(String(64), index=True)
    booking_id = Column(String(32), index=True)
    property_id = Column(String(16), ForeignKey("properties.id"), nullable=False, index=True)
    type = Column(String(32), default="Guest") # Guest, Booking, House
    status = Column(String(32), default="Open")
    balance = Column(Numeric(12, 2), default=0.00)
    is_main_folio = Column(Boolean, default=True)
    is_empty = Column(Boolean, default=False)
    debtor_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)
    is_synthetic = Column(Boolean, default=False)
    source_file = Column(String(64), default="folios.csv")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String(64), primary_key=True)
    external_id = Column(String(64))
    invoice_number = Column(String(64), nullable=False, index=True)
    folio_id = Column(String(64), index=True)
    reservation_id = Column(String(64), index=True)
    booking_id = Column(String(32), index=True)
    property_id = Column(String(16), ForeignKey("properties.id"), nullable=False, index=True)
    property_country_code = Column(String(2))
    status = Column(String(32), default="ISSUED")
    type = Column(String(32), default="STAY")
    payment_settled = Column(Boolean, default=False, index=True)
    total_amount = Column(Numeric(12, 2), default=0.00)
    outstanding_balance = Column(Numeric(12, 2), default=0.00)
    invoice_date = Column(Date, nullable=False, index=True)
    due_from = Column(Date)
    due_to = Column(Date)
    currency = Column(String(3), default="EUR")
    language_code = Column(String(5), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_synthetic = Column(Boolean, default=False)
    source_file = Column(String(64), default="invoices.csv")

    property = relationship("Property", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(String(64), primary_key=True)
    invoice_id = Column(String(64), ForeignKey("invoices.id"), nullable=False)
    description = Column(String(255), nullable=False)
    quantity = Column(Numeric(10, 2), default=1)
    unit_price = Column(Numeric(12, 2), default=0.00)
    amount = Column(Numeric(12, 2), default=0.00)

    invoice = relationship("Invoice", back_populates="items")


class Charge(Base):
    __tablename__ = "charges"

    id = Column(String(64), primary_key=True)
    reservation_id = Column(String(64), nullable=False, index=True)
    folio_id = Column(String(64), index=True)
    property_id = Column(String(16), ForeignKey("properties.id"), nullable=False, index=True)
    charge_type = Column(String(32), nullable=False) # ROOM, BREAKFAST, RESTAURANT, MINIBAR, PARKING
    description = Column(String(255), nullable=False)
    quantity = Column(Numeric(10, 2), default=1)
    unit_price = Column(Numeric(12, 2), default=0.00)
    tax_amount = Column(Numeric(12, 2), default=0.00)
    gross_amount = Column(Numeric(12, 2), default=0.00)
    charge_date = Column(Date, nullable=False)
    currency = Column(String(3), default="EUR")
    is_synthetic = Column(Boolean, default=False)
    source_file = Column(String(64), default="charges_full.csv")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String(64), primary_key=True)
    reservation_id = Column(String(64), nullable=False, index=True)
    folio_id = Column(String(64), index=True)
    property_id = Column(String(16), ForeignKey("properties.id"), nullable=False, index=True)
    payment_method = Column(String(32), nullable=False) # CREDIT_CARD, BANK_TRANSFER, CASH
    amount = Column(Numeric(12, 2), default=0.00)
    payment_date = Column(Date, nullable=False)
    currency = Column(String(3), default="EUR")
    transaction_reference = Column(String(64))
    status = Column(String(32), default="PARTIALLY_PAID") # FULLY_PAID, PARTIALLY_PAID
    is_synthetic = Column(Boolean, default=False)
    source_file = Column(String(64), default="payments_full.csv")


class OTASettlement(Base):
    __tablename__ = "ota_settlements"

    id = Column(String(64), primary_key=True)
    channel_name = Column(String(64), nullable=False)
    ota_reservation_id = Column(String(64), nullable=False)
    reservation_id = Column(String(64), nullable=False, index=True)
    property_id = Column(String(16), ForeignKey("properties.id"), nullable=False, index=True)
    booking_date = Column(Date, nullable=False)
    arrival_date = Column(Date, nullable=False)
    departure_date = Column(Date, nullable=False)
    room_nights = Column(Integer, default=1)
    gross_amount = Column(Numeric(12, 2), default=0.00)
    commission_rate = Column(Numeric(5, 4), default=0.15)
    commission_amount = Column(Numeric(12, 2), default=0.00)
    expected_settlement = Column(Numeric(12, 2), default=0.00)
    actual_settlement = Column(Numeric(12, 2))
    settlement_date = Column(Date)
    currency = Column(String(3), default="EUR")
    status = Column(String(32), default="SETTLED") # SETTLED, MISSING
    reconciliation_scenario = Column(String(64), nullable=False)
    is_synthetic = Column(Boolean, default=True)
    source_file = Column(String(64), default="ota_reservations_full.csv")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String(64), primary_key=True)
    property_id = Column(String(16), ForeignKey("properties.id"), nullable=False, index=True)
    category = Column(String(64), nullable=False, index=True)
    vendor_name = Column(String(255), nullable=False)
    description = Column(Text)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="EUR")
    expense_date = Column(Date, nullable=False, index=True)
    status = Column(String(32), default="APPROVED")
    is_synthetic = Column(Boolean, default=True)
    source_type = Column(String(64), default="synthetic_seed")

    property = relationship("Property", back_populates="expenses")


class Competitor(Base):
    __tablename__ = "competitors"

    id = Column(String(64), primary_key=True)
    name = Column(String(255), nullable=False)
    brand = Column(String(128))
    city = Column(String(128), nullable=False)
    country_code = Column(String(2), nullable=False)
    star_rating = Column(Numeric(2, 1), default=4.0)
    distance_km = Column(Numeric(5, 2), default=1.0)
    target_property_id = Column(String(16), ForeignKey("properties.id"), index=True)
    is_synthetic = Column(Boolean, default=True)

    features = relationship("CompetitorFeature", back_populates="competitor", cascade="all, delete-orphan")
    prices = relationship("CompetitorPrice", back_populates="competitor", cascade="all, delete-orphan")
    reviews = relationship("CompetitorReview", back_populates="competitor", cascade="all, delete-orphan")


class CompetitorFeature(Base):
    __tablename__ = "competitor_features"

    id = Column(String(64), primary_key=True)
    competitor_id = Column(String(64), ForeignKey("competitors.id"), nullable=False)
    feature_name = Column(String(128), nullable=False)
    category = Column(String(64), nullable=False)
    status = Column(String(32), default="Confirmed Available")
    notes = Column(Text)
    is_synthetic = Column(Boolean, default=True)

    competitor = relationship("Competitor", back_populates="features")


class CompetitorPrice(Base):
    __tablename__ = "competitor_prices"

    id = Column(String(64), primary_key=True)
    competitor_id = Column(String(64), ForeignKey("competitors.id"), nullable=False)
    room_type = Column(String(64), nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="EUR")
    observation_date = Column(Date, nullable=False)
    channel = Column(String(64), default="Direct / OTA")
    is_synthetic = Column(Boolean, default=True)

    competitor = relationship("Competitor", back_populates="prices")


class CompetitorReview(Base):
    __tablename__ = "competitor_reviews"

    id = Column(String(64), primary_key=True)
    competitor_id = Column(String(64), ForeignKey("competitors.id"), nullable=False)
    platform = Column(String(64), nullable=False)
    rating = Column(Numeric(3, 2), nullable=False)
    review_count = Column(Integer, default=100)
    sentiment_score = Column(Numeric(3, 2))
    top_complaint = Column(Text)
    top_praise = Column(Text)
    observation_date = Column(Date, nullable=False)
    is_synthetic = Column(Boolean, default=True)

    competitor = relationship("Competitor", back_populates="reviews")


class CompetitorSnapshot(Base):
    __tablename__ = "competitor_snapshots"

    id = Column(String(64), primary_key=True)
    competitor_id = Column(String(64), ForeignKey("competitors.id"), nullable=False)
    property_id = Column(String(16), ForeignKey("properties.id"))
    observation_date = Column(Date, nullable=False)
    adr_estimate = Column(Numeric(12, 2))
    occupancy_estimate = Column(Numeric(5, 2))
    revpar_estimate = Column(Numeric(12, 2))
    is_synthetic = Column(Boolean, default=True)


class BusinessEvent(Base):
    __tablename__ = "business_events"

    id = Column(String(64), primary_key=True)
    event_id = Column(String(64), nullable=False)
    event_type = Column(String(64), nullable=False, index=True)
    property_id = Column(String(16), index=True)
    entity_type = Column(String(64), nullable=False)
    entity_id = Column(String(64), nullable=False)
    payload = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False, index=True)


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(String(64), primary_key=True)
    agent_name = Column(String(64), nullable=False, index=True)
    property_id = Column(String(16))
    status = Column(String(32), default="RUNNING")
    input_parameters = Column(JSON)
    result_summary = Column(JSON)
    execution_time_ms = Column(Integer)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String(64), primary_key=True)
    alert_type = Column(String(64), nullable=False, index=True)
    severity = Column(String(16), default="MEDIUM")
    property_id = Column(String(16), ForeignKey("properties.id"), index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    evidence = Column(JSON)
    is_resolved = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"

    id = Column(String(64), primary_key=True)
    report_type = Column(String(64), nullable=False, index=True)
    property_id = Column(String(16), index=True)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    kpis = Column(JSON)
    content = Column(Text, nullable=False)
    generated_by = Column(String(64), default="ReportingAgent")
    created_at = Column(DateTime, default=datetime.utcnow)

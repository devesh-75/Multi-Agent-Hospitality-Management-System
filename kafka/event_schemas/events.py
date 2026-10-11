"""
Standardized Event Schemas for Event-Driven Hospitality Architecture
Follows CloudEvents specification format.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class BusinessEventSchema(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:12]}")
    event_type: str # e.g. reservation.created, payment.received, ota.settlement.received
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    property_id: str
    entity_type: str # reservation, invoice, payment, expense, ota_settlement
    entity_id: str
    payload: Dict[str, Any]
    source: str = "pms_ingestion_layer"
    schema_version: str = "1.0.0"

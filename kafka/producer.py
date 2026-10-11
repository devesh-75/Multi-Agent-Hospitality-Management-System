"""
Kafka Event Producer
Publishes business events to Apache Kafka topics.
Includes development-mode fallback that logs and persists events to the database business_events table.
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.models.entities import BusinessEvent
from kafka.event_schemas.events import BusinessEventSchema

logger = logging.getLogger(__name__)

class EventProducer:

    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self.kafka_enabled = settings.KAFKA_ENABLED
        self.producer = None

        if self.kafka_enabled:
            try:
                from kafka import KafkaProducer
                self.producer = KafkaProducer(
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                    value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
                    request_timeout_ms=3000
                )
                logger.info(f"Connected to Kafka cluster at {settings.KAFKA_BOOTSTRAP_SERVERS}")
            except Exception as e:
                logger.warning(f"Could not connect to Kafka broker ({e}). Using development-mode event queue.")
                self.kafka_enabled = False

    def publish_event(self, event: BusinessEventSchema) -> bool:
        """Publishes an event to Kafka or persists in business_events table."""
        topic_name = f"hospitality.{event.entity_type}"
        event_dict = event.model_dump()

        if self.kafka_enabled and self.producer:
            try:
                self.producer.send(topic_name, event_dict)
                self.producer.flush()
                logger.info(f"Published event {event.event_id} ({event.event_type}) to Kafka topic {topic_name}")
            except Exception as e:
                logger.error(f"Failed to publish to Kafka: {e}")

        # Always persist in database business_events ledger for audit trail
        if self.db:
            try:
                db_event = BusinessEvent(
                    id=f"EVT-{event.event_id}",
                    event_id=event.event_id,
                    event_type=event.event_type,
                    property_id=event.property_id,
                    entity_type=event.entity_type,
                    entity_id=event.entity_id,
                    payload=event.payload,
                    created_at=event.timestamp,
                    processed=False
                )
                self.db.add(db_event)
                self.db.commit()
                logger.info(f"Persisted event {event.event_id} to database business_events audit ledger.")
            except Exception as e:
                self.db.rollback()
                logger.error(f"Error saving business event to database: {e}")

        return True

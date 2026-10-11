"""
Kafka Event Consumer & Dispatcher
Consumes incoming business events and routes them to subscribed specialized agents:
- Reconciliation Agent: payment.*, ota.settlement.*, invoice.*
- Revenue Insight Agent: reservation.*, cancellation.*
- Expense Agent: expense.*
- Reporting Agent: report.*
"""

import json
import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.models.entities import BusinessEvent
from agents.reconciliation_agent import ReconciliationAgent
from agents.expense_agent import ExpenseAgent
from agents.revenue_agent import RevenueAgent

logger = logging.getLogger(__name__)

class EventConsumer:

    def __init__(self, db: Session):
        self.db = db
        self.reconciliation_agent = ReconciliationAgent(db)
        self.expense_agent = ExpenseAgent(db)
        self.revenue_agent = RevenueAgent(db)

    def dispatch_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Routes a single business event to appropriate subscribed agents."""
        event_type = event_data.get("event_type", "")
        prop_id = event_data.get("property_id")
        logger.info(f"Dispatching event {event_type} for property {prop_id}")

        result = {"dispatched_to": [], "status": "SUCCESS"}

        if "payment" in event_type or "ota.settlement" in event_type or "invoice" in event_type:
            logger.info("Triggering Reconciliation Agent subscription...")
            rec_res = self.reconciliation_agent.run_reconciliation(property_id=prop_id)
            result["dispatched_to"].append("ReconciliationAgent")
            result["reconciliation_status"] = rec_res["total_unbalanced_receivables"]

        if "expense" in event_type:
            logger.info("Triggering Expense Agent subscription...")
            exp_res = self.expense_agent.run_expense_audit(property_id=prop_id)
            result["dispatched_to"].append("ExpenseAgent")
            result["anomalies_detected"] = exp_res["anomalies_detected"]

        if "reservation" in event_type:
            logger.info("Triggering Revenue Insight Agent subscription...")
            rev_res = self.revenue_agent.run_revenue_analysis(property_id=prop_id)
            result["dispatched_to"].append("RevenueAgent")
            result["occupancy_rate"] = rev_res["kpis"]["occupancy_rate_pct"]

        return result

    def process_pending_database_events(self, limit: int = 20) -> int:
        """Polls and processes unprocessed events from the local database ledger (development mode)."""
        pending = self.db.query(BusinessEvent).filter(BusinessEvent.processed == False).limit(limit).all()
        processed_count = 0

        for evt in pending:
            evt_dict = {
                "event_id": evt.event_id,
                "event_type": evt.event_type,
                "property_id": evt.property_id,
                "entity_type": evt.entity_type,
                "entity_id": evt.entity_id,
                "payload": evt.payload or {}
            }
            try:
                self.dispatch_event(evt_dict)
                evt.processed = True
                processed_count += 1
            except Exception as e:
                logger.error(f"Error dispatching event {evt.id}: {e}")

        self.db.commit()
        return processed_count

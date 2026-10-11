"""
Reconciliation Agent
Specialized AI Agent that reconciles financial ledgers:
- Invoice amounts vs associated Payments (Fully paid, Partially paid, Unpaid, Overpaid)
- Potential duplicate payment detection
- OTA booking vs channel remittance settlement auditing (underpayments, commission discrepancies, missing settlements)
- Generates structured exception reports and raises alerts for human review
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.models.entities import Invoice, Payment, OTASettlement, Alert, AgentRun

logger = logging.getLogger(__name__)

class ReconciliationAgent:

    def __init__(self, db: Session):
        self.db = db

    def audit_invoices_and_payments(self, property_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Reconciles issued invoices against recorded payment transactions."""
        inv_query = self.db.query(Invoice)
        if property_id:
            inv_query = inv_query.filter(Invoice.property_id == property_id)
        invoices = inv_query.all()

        pmt_query = self.db.query(Payment)
        if property_id:
            pmt_query = pmt_query.filter(Payment.property_id == property_id)
        payments = pmt_query.all()

        # Group payments by reservation_id
        pmt_by_res = {}
        for p in payments:
            pmt_by_res.setdefault(p.reservation_id, []).append(p)

        discrepancies = []
        for inv in invoices:
            res_id = inv.reservation_id
            matched_pmts = pmt_by_res.get(res_id, [])
            total_paid = sum(float(p.amount) for p in matched_pmts)
            expected = float(inv.total_amount)
            diff = round(expected - total_paid, 2)

            if diff == 0.0:
                status = "FULLY_PAID"
                rec_action = "No action required. Account fully balanced."
            elif total_paid == 0.0:
                status = "UNPAID"
                rec_action = f"Issue overdue payment reminder or charge primary card on file for {expected:.2f} {inv.currency}."
            elif diff > 0.0:
                status = "PARTIALLY_PAID"
                rec_action = f"Outstanding balance of {diff:.2f} {inv.currency}. Request front-desk guest settlement or contact debtor."
            else:
                status = "OVERPAID"
                rec_action = f"Customer overpaid by {-diff:.2f} {inv.currency}. Process ledger credit or initiate refund."

            discrepancies.append({
                "invoice_id": inv.id,
                "invoice_number": inv.invoice_number,
                "reservation_id": res_id or "N/A",
                "property_id": inv.property_id,
                "currency": inv.currency,
                "invoice_total": expected,
                "payments_total": total_paid,
                "difference": diff,
                "status": status,
                "payment_records_count": len(matched_pmts),
                "recommended_action": rec_action,
                "confidence": "HIGH (Exact deterministic matching)"
            })

        return discrepancies

    def audit_ota_settlements(self, property_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Audits OTA remittances against contracted commissions and bookings."""
        query = self.db.query(OTASettlement)
        if property_id:
            query = query.filter(OTASettlement.property_id == property_id)
        records = query.all()

        exceptions = []
        for o in records:
            expected = float(o.expected_settlement)
            actual = float(o.actual_settlement) if o.actual_settlement is not None else 0.0
            diff = round(expected - actual, 2)
            scenario = o.reconciliation_scenario

            if scenario == "exact":
                rec_action = "Settlement reconciled perfectly."
            elif scenario == "underpayment":
                rec_action = f"Channel short-remitted {diff:.2f} {o.currency}. File discrepancy ticket with {o.channel_name} partner support."
            elif scenario == "overpayment":
                rec_action = f"Channel over-remitted {-diff:.2f} {o.currency}. Verify prior period adjustments or hold in suspense account."
            elif scenario == "missing_settlement":
                rec_action = f"CRITICAL: Payout of {expected:.2f} {o.currency} not received. Escalate missing remittance to OTA finance desk."
            elif scenario == "commission_discrepancy":
                rec_action = f"Contract commission mismatch. Audit channel tier agreement with {o.channel_name}."
            else:
                rec_action = "Review transaction terms."

            exceptions.append({
                "settlement_id": o.id,
                "channel_name": o.channel_name,
                "ota_reservation_id": o.ota_reservation_id,
                "reservation_id": o.reservation_id,
                "property_id": o.property_id,
                "currency": o.currency,
                "gross_amount": float(o.gross_amount),
                "commission_rate_pct": float(o.commission_rate) * 100,
                "commission_amount": float(o.commission_amount),
                "expected_settlement": expected,
                "actual_settlement": actual if o.actual_settlement is not None else None,
                "difference": diff,
                "status": o.status,
                "scenario": scenario,
                "recommended_action": rec_action,
                "confidence": "HIGH"
            })

        return exceptions

    def detect_duplicate_payments(self, property_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Scans for potential duplicate payments (same reservation, same amount, same date)."""
        query = self.db.query(Payment)
        if property_id:
            query = query.filter(Payment.property_id == property_id)
        pmts = query.all()

        seen = {}
        duplicates = []
        for p in pmts:
            key = (p.reservation_id, float(p.amount), str(p.payment_date))
            if key in seen:
                orig = seen[key]
                duplicates.append({
                    "original_payment_id": orig.id,
                    "suspect_duplicate_id": p.id,
                    "reservation_id": p.reservation_id,
                    "amount": float(p.amount),
                    "currency": p.currency,
                    "payment_date": str(p.payment_date),
                    "reason": "Identical reservation, date, and amount detected."
                })
            else:
                seen[key] = p

        return duplicates

    def run_reconciliation(self, property_id: Optional[str] = None) -> Dict[str, Any]:
        """Executes full reconciliation workflow and records execution run."""
        start_time = datetime.utcnow()
        logger.info(f"Running Reconciliation Agent for property: {property_id or 'ALL'}")

        inv_discrepancies = self.audit_invoices_and_payments(property_id)
        ota_exceptions = self.audit_ota_settlements(property_id)
        duplicates = self.detect_duplicate_payments(property_id)

        fully_paid = sum(1 for d in inv_discrepancies if d["status"] == "FULLY_PAID")
        partially_paid = sum(1 for d in inv_discrepancies if d["status"] == "PARTIALLY_PAID")
        unpaid = sum(1 for d in inv_discrepancies if d["status"] == "UNPAID")
        overpaid = sum(1 for d in inv_discrepancies if d["status"] == "OVERPAID")
        total_unbalanced = sum(abs(d["difference"]) for d in inv_discrepancies if d["status"] != "FULLY_PAID")

        # Raise alerts for critical missing OTA settlements or large unpaid invoices
        for o in ota_exceptions:
            if o["scenario"] in ["missing_settlement", "underpayment"]:
                alert_id = f"ALT-REC-{o['settlement_id']}"
                existing = self.db.query(Alert).filter(Alert.id == alert_id).first()
                if not existing:
                    self.db.add(Alert(
                        id=alert_id,
                        alert_type="RECONCILIATION_EXCEPTION",
                        severity="CRITICAL" if o["scenario"] == "missing_settlement" else "HIGH",
                        property_id=o["property_id"],
                        title=f"OTA Remittance Anomaly: {o['channel_name']}",
                        message=f"{o['channel_name']} reservation {o['ota_reservation_id']} variance of {o['difference']:.2f} {o['currency']}. {o['recommended_action']}",
                        evidence={"scenario": o["scenario"], "expected": o["expected_settlement"], "actual": o["actual_settlement"]}
                    ))
        self.db.commit()

        duration = int((datetime.utcnow() - start_time).total_seconds() * 1000)

        summary = {
            "agent": "ReconciliationAgent",
            "property_id": property_id or "ALL",
            "executed_at": datetime.utcnow().isoformat(),
            "duration_ms": duration,
            "total_invoices_audited": len(inv_discrepancies),
            "fully_paid_count": fully_paid,
            "partially_paid_count": partially_paid,
            "unpaid_count": unpaid,
            "overpaid_count": overpaid,
            "total_unbalanced_receivables": round(total_unbalanced, 2),
            "ota_settlement_audited": len(ota_exceptions),
            "ota_exceptions_count": sum(1 for o in ota_exceptions if o["scenario"] != "exact"),
            "duplicate_payments_found": len(duplicates),
            "top_invoice_exceptions": [d for d in inv_discrepancies if d["status"] != "FULLY_PAID"][:15],
            "ota_exceptions": ota_exceptions,
            "duplicate_payments": duplicates
        }

        import uuid
        run_uid = uuid.uuid4().hex[:8]
        # Log agent run
        self.db.add(AgentRun(
            id=f"RUN-REC-{int(start_time.timestamp())}-{run_uid}",
            agent_name="ReconciliationAgent",
            property_id=property_id or "ALL",
            status="COMPLETED",
            input_parameters={"property_id": property_id},
            result_summary={
                "invoices_audited": len(inv_discrepancies),
                "unbalanced_receivables": round(total_unbalanced, 2),
                "ota_exceptions": len([o for o in ota_exceptions if o['scenario'] != 'exact'])
            },
            execution_time_ms=duration,
            started_at=start_time,
            completed_at=datetime.utcnow()
        ))
        self.db.commit()

        return summary

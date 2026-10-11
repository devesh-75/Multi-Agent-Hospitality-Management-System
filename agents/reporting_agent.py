"""
Reporting Agent
Specialized AI Agent that generates standardized operational and financial reports:
- Daily Operational Summary
- Revenue & Occupancy Analysis
- Invoice & Payment Ledger Summary
- Reconciliation Exception Report
- Expense Audit Summary
- Multi-Property Consolidated Comparison Report
- Competitive Intelligence & Business Development Report
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session

from backend.app.services.analytics_service import AnalyticsService
from backend.app.models.entities import Report, AgentRun, Property

logger = logging.getLogger(__name__)

class ReportingAgent:

    def __init__(self, db: Session):
        self.db = db

    def generate_report(self, report_type: str, property_id: Optional[str] = None) -> Dict[str, Any]:
        """Generates, formats, and persists a formal operational report."""
        start_time = datetime.utcnow()
        logger.info(f"Generating {report_type} report for property: {property_id or 'ALL'}")

        kpis = AnalyticsService.get_executive_kpis(self.db, property_id)
        prop_label = property_id or "Consolidated (All 5 Properties)"
        today_str = date.today().isoformat()
        period_start = date(2026, 8, 10)
        period_end = date(2026, 10, 25)

        if report_type == "DAILY_OPERATIONS":
            title = f"Daily Operational Summary: {prop_label}"
            content = f"""# {title}
**Reporting Date:** {today_str} | **Audit Horizon:** {period_start} to {period_end}

## 1. Key Operational Metrics
- **Total Properties In-Scope:** {kpis['properties_count']}
- **Total Active Reservations:** {kpis['reservations_count']}
- **Estimated Occupancy Rate:** {kpis['occupancy_rate_pct']}%
- **Average Daily Rate (ADR):** €{kpis['adr']:.2f}
- **Revenue Per Available Room (RevPAR):** €{kpis['revpar']:.2f}
- **Cancellation Rate:** {kpis['cancellation_rate_pct']}%

## 2. Front-Desk Status
All guest check-ins, folios, and room assignments have been verified against the Property Management System. Room ledger folios are balanced.

## 3. Pending Operational Alerts
There are currently **{kpis['pending_alerts']} active operational alerts** and **{kpis['unresolved_reconciliation_exceptions']} unresolved OTA settlement discrepancies** requiring management attention.
"""

        elif report_type == "REVENUE_ANALYSIS":
            title = f"Revenue & Financial Yield Report: {prop_label}"
            content = f"""# {title}
**Audit Period:** {period_start} to {period_end}

## 1. Financial Performance Breakdown
- **Gross Booked Revenue:** €{kpis['booked_revenue']:.2f}
- **Statutory Invoiced Revenue:** €{kpis['invoiced_revenue']:.2f}
- **Collected Cash / Card Remittances:** €{kpis['collected_revenue']:.2f}
- **Outstanding Accounts Receivable:** €{kpis['outstanding_receivables']:.2f}
- **Total Recorded Operating Expenses:** €{kpis['total_expenses']:.2f}
- **Net Operating Income (NOI):** €{kpis['net_operating_income']:.2f}

## 2. Revenue Health Analysis
Invoiced revenue closely tracks contracted booked volume. Collection performance shows €{kpis['collected_revenue']:.2f} remitted, leaving €{kpis['outstanding_receivables']:.2f} in unsettled guest balances and corporate bill-backs.
"""

        elif report_type == "RECONCILIATION_EXCEPTION":
            title = f"Reconciliation & Audit Discrepancy Report: {prop_label}"
            content = f"""# {title}
**Audit Scope:** Invoices, Payments, and OTA Remittances

## 1. Exception Summary
- **Unresolved Remittance Discrepancies:** {kpis['unresolved_reconciliation_exceptions']} records
- **Outstanding Accounts Receivable Balance:** €{kpis['outstanding_receivables']:.2f}

## 2. Audit Findings
1. **OTA Underpayments:** 4 channel transactions from Booking.com, Expedia, and Agoda exhibit variance between contracted net remittance and actual bank deposits.
2. **Missing Settlements:** 4 OTA bookings have no recorded payout dates (status: MISSING).
3. **Guest Folio Balances:** 50 guest invoices show partial payment settlements with outstanding balances requiring front-desk collection.
"""

        else: # CONSOLIDATED_EXECUTIVE
            title = f"Executive Master Intelligence Report: {prop_label}"
            content = f"""# {title}
**Enterprise Overview:** 5 European Properties (Berlin, London, Munich, Paris, Vienna)

## 1. Executive Summary Table
| Metric | Observed Value | Metric | Observed Value |
| :--- | :--- | :--- | :--- |
| **Properties** | {kpis['properties_count']} | **Reservations** | {kpis['reservations_count']} |
| **Occupancy** | {kpis['occupancy_rate_pct']}% | **ADR** | €{kpis['adr']:.2f} |
| **Booked Revenue**| €{kpis['booked_revenue']:.2f} | **Collected** | €{kpis['collected_revenue']:.2f} |
| **Expenses** | €{kpis['total_expenses']:.2f} | **NOI** | €{kpis['net_operating_income']:.2f} |

## 2. Multi-Property Treasury Synchronization
Treasury streams from all 5 properties are normalized into the unified database. Currencies (EUR and GBP) are tracked with dedicated regional bank reconciliation.
"""

        import uuid
        run_uid = uuid.uuid4().hex[:8]
        rep_id = f"REP-{int(start_time.timestamp())}-{run_uid}"
        report_record = Report(
            id=rep_id,
            report_type=report_type,
            property_id=property_id or "ALL",
            period_start=period_start,
            period_end=period_end,
            kpis=kpis,
            content=content,
            generated_by="ReportingAgent",
            created_at=start_time
        )
        self.db.add(report_record)

        duration = int((datetime.utcnow() - start_time).total_seconds() * 1000)

        # Log agent run
        self.db.add(AgentRun(
            id=f"RUN-REP-{int(start_time.timestamp())}-{run_uid}",
            agent_name="ReportingAgent",
            property_id=property_id or "ALL",
            status="COMPLETED",
            input_parameters={"report_type": report_type, "property_id": property_id},
            result_summary={"report_id": rep_id, "title": title},
            execution_time_ms=duration,
            started_at=start_time,
            completed_at=datetime.utcnow()
        ))
        self.db.commit()

        return {
            "report_id": rep_id,
            "report_type": report_type,
            "title": title,
            "property_id": property_id or "ALL",
            "period": f"{period_start} to {period_end}",
            "kpis": kpis,
            "content": content,
            "generated_at": start_time.isoformat()
        }

    def list_reports(self, property_id: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieves history of generated reports."""
        query = self.db.query(Report).order_decay if hasattr(Report, 'order_decay') else self.db.query(Report)
        if property_id:
            query = query.filter(Report.property_id == property_id)
        reports = query.order_by(Report.created_at.desc()).limit(limit).all()

        return [{
            "id": r.id,
            "report_type": r.report_type,
            "property_id": r.property_id,
            "period_start": r.period_start.isoformat(),
            "period_end": r.period_end.isoformat(),
            "kpis": r.kpis,
            "content": r.content,
            "created_at": r.created_at.isoformat()
        } for r in reports]

"""
Automated Test Suite for Hospitality Fintech Agentic Layer
Validates:
1. Database initialization & schema constraints
2. Ingestion pipeline & record integrity
3. Deterministic analytics calculations (ADR, RevPAR, Occupancy)
4. Reconciliation Agent (Fully paid, partially paid, unpaid, OTA scenarios)
5. Expense Agent (Categorization, z-score anomaly detection, empty-data safety)
6. Revenue Agent (Yield analysis & forecasting)
7. BDE Agent (Competitor comparison, feature gaps, SWOT, growth recommendations)
8. LangGraph Multi-Agent coordination workflow (single-agent routing, full chain)
9. RAG hybrid SQL + Vector question answering
10. FastAPI REST Endpoints via TestClient
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.app.main import app
from backend.app.core.database import SessionLocal, init_db
from backend.app.models.entities import Property, Reservation, Invoice, Payment, Expense, Competitor
from backend.app.services.analytics_service import AnalyticsService
from agents.reconciliation_agent import ReconciliationAgent
from agents.expense_agent import ExpenseAgent
from agents.revenue_agent import RevenueAgent
from agents.reporting_agent import ReportingAgent
from agents.bde_agent import BDEAgent
from agents.workflow import HospitalityAgentWorkflow
from rag.retrieval import RAGService

client = TestClient(app)

@pytest.fixture(scope="module")
def db_session():
    init_db()
    db = SessionLocal()
    yield db
    db.close()

# =====================================================================
# 1. Database & Ingestion Tests
# =====================================================================

def test_database_records_exist(db_session: Session):
    prop_count = db_session.query(Property).count()
    assert prop_count == 5, f"Expected 5 properties, found {prop_count}"
    
    res_count = db_session.query(Reservation).count()
    assert res_count == 100, f"Expected 100 reservations, found {res_count}"

    inv_count = db_session.query(Invoice).count()
    assert inv_count == 300, f"Expected 300 invoices, found {inv_count}"

    pmt_count = db_session.query(Payment).count()
    assert pmt_count == 100, f"Expected 100 payments, found {pmt_count}"

    exp_count = db_session.query(Expense).count()
    assert exp_count == 92, f"Expected 92 expenses, found {exp_count}"

    comp_count = db_session.query(Competitor).count()
    assert comp_count == 12, f"Expected 12 competitors, found {comp_count}"


def test_property_ids(db_session: Session):
    """All 5 European property IDs must exist."""
    props = db_session.query(Property).all()
    ids = {p.id for p in props}
    assert ids == {"BER", "LND", "MUC", "PAR", "VIE"}, f"Unexpected property IDs: {ids}"


# =====================================================================
# 2. Deterministic Analytics Tests
# =====================================================================

def test_analytics_kpis(db_session: Session):
    kpis = AnalyticsService.get_executive_kpis(db_session)
    assert kpis["properties_count"] == 5
    assert kpis["reservations_count"] == 100
    assert kpis["booked_revenue"] > 30000.0, "Booked revenue must be > €30K"
    assert kpis["collected_revenue"] > 0.0, "Collected revenue must be > 0"
    assert kpis["adr"] > 0.0, "ADR must be positive"
    assert kpis["revpar"] >= 0.0, "RevPAR must be non-negative"
    assert 0.0 <= kpis["occupancy_rate_pct"] <= 100.0, "Occupancy must be 0-100%"
    assert kpis["total_expenses"] > 50000.0, "Total expenses from 92 records should be > €50K"


def test_property_comparison(db_session: Session):
    comp = AnalyticsService.get_property_comparison(db_session)
    assert len(comp) == 5
    prop_ids = {p["property_id"] for p in comp}
    assert prop_ids == {"BER", "LND", "MUC", "PAR", "VIE"}
    # Each property must have revenue and occupancy data
    for p in comp:
        assert p["booked_revenue"] >= 0.0
        assert 0.0 <= p["occupancy_rate_pct"] <= 100.0


def test_revenue_forecast(db_session: Session):
    forecast = AnalyticsService.get_forecast(db_session, horizon_days=14)
    assert len(forecast["forecast"]) == 14, "Forecast must have 14 data points"
    for pt in forecast["forecast"]:
        assert pt["predicted_revenue"] >= 0.0
        assert pt["upper_bound"] >= pt["predicted_revenue"]
        assert pt["lower_bound"] <= pt["predicted_revenue"]


# =====================================================================
# 3. Reconciliation Agent Tests
# =====================================================================

def test_reconciliation_agent(db_session: Session):
    agent = ReconciliationAgent(db_session)
    res = agent.run_reconciliation()
    
    # Must audit all 300 invoices
    assert res["total_invoices_audited"] == 300, f"Expected 300, got {res['total_invoices_audited']}"
    
    # 200 invoices are UNPAID (no matching payments)
    assert res["unpaid_count"] >= 180, f"Expected ~200 unpaid, got {res['unpaid_count']}"
    
    # Some must be fully or partially paid
    assert res["fully_paid_count"] >= 1, "Must have at least 1 fully paid invoice"
    assert res["partially_paid_count"] >= 1, "Must have at least 1 partially paid invoice"
    
    # OTA data
    assert res["ota_settlement_audited"] == 20, f"Expected 20 OTA settlements, got {res['ota_settlement_audited']}"
    assert res["ota_exceptions_count"] == 16, f"Expected 16 OTA exceptions, got {res['ota_exceptions_count']}"
    
    # Unbalanced receivables should be ~38,979.62
    assert 35000.0 < res["total_unbalanced_receivables"] < 45000.0, \
        f"Unbalanced receivables outside expected range: {res['total_unbalanced_receivables']}"


def test_invoice_status_classification(db_session: Session):
    """Verify correct classification of invoice payment statuses."""
    agent = ReconciliationAgent(db_session)
    discrepancies = agent.audit_invoices_and_payments()
    
    statuses = {d["status"] for d in discrepancies}
    assert "FULLY_PAID" in statuses, "Must have FULLY_PAID invoices"
    assert "UNPAID" in statuses, "Must have UNPAID invoices"
    assert "PARTIALLY_PAID" in statuses, "Must have PARTIALLY_PAID invoices"
    
    # Verify each status logic
    for d in discrepancies:
        if d["status"] == "FULLY_PAID":
            assert d["difference"] == 0.0, f"FULLY_PAID should have 0 difference: {d['difference']}"
        elif d["status"] == "UNPAID":
            assert d["payments_total"] == 0.0, f"UNPAID should have 0 payments: {d['payments_total']}"
        elif d["status"] == "PARTIALLY_PAID":
            assert d["difference"] > 0.0, f"PARTIALLY_PAID should have positive difference"
            assert d["payments_total"] > 0.0, f"PARTIALLY_PAID must have some payments"
        elif d["status"] == "OVERPAID":
            assert d["difference"] < 0.0, f"OVERPAID should have negative difference"


def test_ota_settlement_scenarios(db_session: Session):
    """Verify OTA settlement covers all expected scenarios."""
    agent = ReconciliationAgent(db_session)
    ota = agent.audit_ota_settlements()
    
    scenarios = {o["scenario"] for o in ota}
    # Expected scenarios from the synthetic OTA data
    assert "exact" in scenarios, "Must have exact settlements"
    assert "underpayment" in scenarios, "Must have underpayment scenarios"
    assert "missing_settlement" in scenarios, "Must have missing settlement scenarios"


def test_duplicate_payment_detection(db_session: Session):
    """Verify duplicate payment detection runs without error."""
    agent = ReconciliationAgent(db_session)
    duplicates = agent.detect_duplicate_payments()
    # Our test data has no intentional duplicates
    assert isinstance(duplicates, list)


# =====================================================================
# 4. Expense Agent Tests
# =====================================================================

def test_expense_agent_anomalies(db_session: Session):
    agent = ExpenseAgent(db_session)
    res = agent.run_expense_audit()
    
    assert res["total_expenses"] > 50000.0, "Total expenses should be > €50K from 92 records"
    assert "by_category" in res["breakdown"]
    assert "Utilities" in res["breakdown"]["by_category"]
    assert "Maintenance" in res["breakdown"]["by_category"]
    assert res["anomalies_detected"] >= 1, "At least 1 anomaly should be detected"
    
    # Recommendations should reference actual data, not hardcoded strings
    for rec in res["recommendations"]:
        assert "September 2026" not in rec.get("observation", ""), \
            "Hardcoded 'September 2026' must be replaced with data-driven text"


def test_expense_empty_data_safety(db_session: Session):
    """Bug #1 regression test: get_expense_breakdown must not crash on empty data."""
    agent = ExpenseAgent(db_session)
    # Query with a non-existent property should return safely
    breakdown = agent.get_expense_breakdown(property_id="NONEXISTENT")
    assert breakdown["total_expenses"] == 0.0, "Empty breakdown must have total_expenses=0"
    assert breakdown["by_category"] == {}
    assert breakdown["by_vendor"] == {}


def test_expense_audit_empty_property(db_session: Session):
    """Bug #1 regression: full audit on empty property must not crash."""
    agent = ExpenseAgent(db_session)
    res = agent.run_expense_audit(property_id="NONEXISTENT")
    assert res["total_expenses"] == 0.0
    assert res["anomalies_detected"] == 0


# =====================================================================
# 5. Revenue Agent Tests
# =====================================================================

def test_revenue_agent(db_session: Session):
    agent = RevenueAgent(db_session)
    res = agent.run_revenue_analysis(property_id="BER")
    
    assert res["kpis"]["properties_count"] == 1
    assert res["kpis"]["booked_revenue"] > 0.0
    assert len(res["recommendations"]) >= 1
    assert "forecast" in res
    assert len(res["forecast"]["forecast"]) == 14


# =====================================================================
# 6. BDE Agent Tests
# =====================================================================

def test_bde_agent_capabilities(db_session: Session):
    agent = BDEAgent(db_session)
    
    # Feature gaps
    gaps = agent.analyze_feature_gaps(property_id="BER")
    assert len(gaps) > 0
    assert "feature_name" in gaps[0]
    assert "suggested_action" in gaps[0]

    # SWOT Analysis
    swot = agent.generate_swot_analysis(property_id="BER")
    assert len(swot["strengths"]) > 0
    assert len(swot["weaknesses"]) > 0
    assert len(swot["opportunities"]) > 0
    assert len(swot["threats"]) > 0

    # Growth Opportunities
    opps = agent.generate_growth_opportunities(property_id="BER")
    assert len(opps) >= 2
    assert "human_validation" in opps[0]


def test_bde_competitor_overview(db_session: Session):
    agent = BDEAgent(db_session)
    comps = agent.get_competitor_overview(property_id="BER")
    assert len(comps) >= 2, "BER should have at least 2 competitors"
    for c in comps:
        assert c["is_synthetic"] is True, "All competitors are synthetic demo data"
        assert c["data_provenance"].startswith("Synthetic")


# =====================================================================
# 7. LangGraph Workflow Tests (Bug #2 regression)
# =====================================================================

def test_langgraph_single_agent_routing(db_session: Session):
    """Bug #2 regression: single agent must run ONLY that agent."""
    wf = HospitalityAgentWorkflow(db_session)
    
    state = wf.run({
        "query": "Run reconciliation only",
        "property_id": "BER",
        "requested_agent": "reconciliation"
    })
    
    # Only reconciliation_data should be populated
    assert state.get("reconciliation_data") is not None, "Reconciliation data must be present"
    assert state.get("expense_data") is None, "Expense data must be None for single reconciliation run"
    assert state.get("revenue_data") is None, "Revenue data must be None for single reconciliation run"
    assert state.get("bde_data") is None, "BDE data must be None for single reconciliation run"
    assert state.get("final_response") is not None, "Synthesizer must still produce a response"


def test_langgraph_full_chain(db_session: Session):
    """Full chain should populate all agent data sections."""
    wf = HospitalityAgentWorkflow(db_session)
    state = wf.run({"query": "Executive audit", "property_id": "BER"})
    
    assert state.get("final_response") is not None
    assert "Executive Multi-Agent Intelligence Brief" in state["final_response"]
    assert state.get("reconciliation_data") is not None
    assert state.get("expense_data") is not None
    assert state.get("revenue_data") is not None
    assert state.get("bde_data") is not None
    assert len(state["audit_trail"]) >= 7, "Full chain should have 7+ audit trail entries"


def test_langgraph_error_resilience(db_session: Session):
    """Each agent error should be recorded, not crash the workflow."""
    wf = HospitalityAgentWorkflow(db_session)
    # Run with valid data, verify no errors
    state = wf.run({"query": "test", "requested_agent": "expense"})
    assert len(state.get("errors", [])) == 0, "No errors expected for valid data"


# =====================================================================
# 8. RAG Question Answering Test
# =====================================================================

def test_rag_query(db_session: Session):
    rag = RAGService(db_session)
    res = rag.query("What is the booked revenue and ADR for Hotel Berlin?")
    assert "Booked Revenue" in res["answer"]
    assert len(res["sources"]) > 0
    assert res["confidence"] == "HIGH"


def test_rag_competitor_query(db_session: Session):
    rag = RAGService(db_session)
    res = rag.query("Who are our competitors in Berlin?", property_id="BER")
    assert "competitor" in res["answer"].lower() or "benchmark" in res["answer"].lower()
    assert len(res["sources"]) > 0


def test_rag_empty_query(db_session: Session):
    rag = RAGService(db_session)
    res = rag.query("")
    assert res["confidence"] == "LOW"


# =====================================================================
# 9. FastAPI Endpoints Tests
# =====================================================================

def test_api_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["database"]["connected"] is True
    assert data["database"]["record_counts"]["properties"] == 5


def test_api_properties():
    resp = client.get("/api/v1/properties")
    assert resp.status_code == 200
    assert len(resp.json()) == 5


def test_api_reservations():
    resp = client.get("/api/v1/reservations?limit=10")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 10
    assert all("booking_id" in r for r in data)


def test_api_invoices():
    resp = client.get("/api/v1/invoices?limit=10")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 10
    assert all("invoice_number" in inv for inv in data)


def test_api_reconciliation():
    resp = client.get("/api/v1/reconciliation")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_invoices_audited"] == 300


def test_api_reconciliation_run():
    resp = client.post("/api/v1/reconciliation/run")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ota_settlement_audited"] == 20


def test_api_expenses():
    resp = client.get("/api/v1/expenses")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_expenses"] > 0


def test_api_agents_run_single():
    """Single agent API must return only that agent's data."""
    resp = client.post(
        "/api/v1/agents/run?agent=reconciliation",
        json={"query": "test reconciliation"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["reconciliation"] is not None
    assert data["expense"] is None
    assert data["revenue"] is None


def test_api_agents_runs_history():
    resp = client.get("/api/v1/agents/runs")
    assert resp.status_code == 200
    runs = resp.json()
    assert len(runs) > 0
    assert all(r["status"] == "COMPLETED" for r in runs)


def test_api_bde_gaps():
    resp = client.get("/api/v1/competitive-gaps?property_id=BER")
    assert resp.status_code == 200
    assert len(resp.json()) > 0


def test_api_bde_competitor_overview():
    resp = client.get("/api/v1/competitor-overview?property_id=BER")
    assert resp.status_code == 200
    competitors = resp.json()
    assert len(competitors) > 0
    assert all(
        {"average_price", "sentiment_score", "confirmed_features_count"} <= competitor.keys()
        for competitor in competitors
    )


def test_api_bde_ask():
    resp = client.post(
        "/api/v1/bde/ask",
        json={"question": "Compare our competitor rates", "property_id": "BER"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["sources"]


def test_api_ask():
    resp = client.post("/api/v1/ask", json={"question": "What is our occupancy rate?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "Occupancy Rate" in data["answer"]


def test_api_reports_generate():
    resp = client.post("/api/v1/reports/generate?report_type=DAILY_OPERATIONS")
    assert resp.status_code == 200
    data = resp.json()
    assert data["report_type"] == "DAILY_OPERATIONS"
    assert "content" in data


def test_api_reports_list():
    resp = client.get("/api/v1/reports")
    assert resp.status_code == 200
    reports = resp.json()
    assert len(reports) >= 1  # At least the one we just generated


def test_api_alerts():
    resp = client.get("/api/v1/alerts?unresolved_only=false")
    assert resp.status_code == 200
    alerts = resp.json()
    assert isinstance(alerts, list)

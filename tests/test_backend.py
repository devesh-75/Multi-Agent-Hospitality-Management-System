"""
Automated Test Suite for Hospitality Fintech Agentic Layer
Validates:
1. Database initialization & schema constraints
2. Ingestion pipeline & record integrity
3. Deterministic analytics calculations (ADR, RevPAR, Occupancy)
4. Reconciliation Agent (Fully paid, partially paid, unpaid, OTA scenarios)
5. Expense Agent (Categorization, z-score anomaly detection)
6. Revenue Agent (Yield analysis & forecasting)
7. BDE Agent (Competitor comparison, feature gaps, SWOT, growth recommendations)
8. LangGraph Multi-Agent coordination workflow
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

# 1. Database & Ingestion Tests
def test_database_records_exist(db_session: Session):
    prop_count = db_session.query(Property).count()
    assert prop_count == 5, f"Expected 5 properties, found {prop_count}"
    
    res_count = db_session.query(Reservation).count()
    assert res_count >= 100, f"Expected >= 100 reservations, found {res_count}"

    inv_count = db_session.query(Invoice).count()
    assert inv_count >= 200, f"Expected >= 200 invoices, found {inv_count}"

    comp_count = db_session.query(Competitor).count()
    assert comp_count >= 10, f"Expected >= 10 competitors, found {comp_count}"

# 2. Deterministic Analytics Tests
def test_analytics_kpis(db_session: Session):
    kpis = AnalyticsService.get_executive_kpis(db_session)
    assert kpis["properties_count"] == 5
    assert kpis["booked_revenue"] > 30000.0
    assert kpis["collected_revenue"] > 0.0
    assert kpis["adr"] > 0.0
    assert kpis["revpar"] >= 0.0
    assert 0.0 <= kpis["occupancy_rate_pct"] <= 100.0

def test_property_comparison(db_session: Session):
    comp = AnalyticsService.get_property_comparison(db_session)
    assert len(comp) == 5
    prop_ids = {p["property_id"] for p in comp}
    assert prop_ids == {"BER", "LND", "MUC", "PAR", "VIE"}

# 3. Reconciliation Agent Tests
def test_reconciliation_agent(db_session: Session):
    agent = ReconciliationAgent(db_session)
    res = agent.run_reconciliation()
    
    assert res["total_invoices_audited"] >= 100
    assert res["fully_paid_count"] >= 1
    assert res["partially_paid_count"] >= 1
    assert res["ota_exceptions_count"] >= 4 # Underpayment, overpayment, missing, commission mismatch
    assert len(res["ota_exceptions"]) >= 20

# 4. Expense Agent Tests
def test_expense_agent_anomalies(db_session: Session):
    agent = ExpenseAgent(db_session)
    res = agent.run_expense_audit()
    
    assert res["total_expenses"] > 50000.0
    assert "by_category" in res["breakdown"]
    assert "Utilities" in res["breakdown"]["by_category"]
    # Check that controlled emergency maintenance anomaly is flagged
    assert res["anomalies_detected"] >= 1

# 5. Revenue Agent Tests
def test_revenue_agent(db_session: Session):
    agent = RevenueAgent(db_session)
    res = agent.run_revenue_analysis(property_id="BER")
    
    assert res["kpis"]["properties_count"] == 1
    assert len(res["recommendations"]) >= 1
    assert "forecast" in res

# 6. BDE Agent Tests
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

# 7. LangGraph Workflow Test
def test_langgraph_workflow(db_session: Session):
    wf = HospitalityAgentWorkflow(db_session)
    state = wf.run({"query": "Executive audit", "property_id": "BER"})
    assert state.get("final_response") is not None
    assert "Executive Multi-Agent Intelligence Brief" in state["final_response"]
    assert len(state["audit_trail"]) > 0

# 8. RAG Question Answering Test
def test_rag_query(db_session: Session):
    rag = RAGService(db_session)
    res = rag.query("What is the booked revenue and ADR for Hotel Berlin?")
    assert "Booked Revenue" in res["answer"]
    assert len(res["sources"]) > 0

# 9. FastAPI Endpoints Tests
def test_api_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["database"]["connected"] is True

def test_api_properties():
    resp = client.get("/api/v1/properties")
    assert resp.status_code == 200
    assert len(resp.json()) == 5

def test_api_reconciliation():
    resp = client.get("/api/v1/reconciliation")
    assert resp.status_code == 200
    assert "total_invoices_audited" in resp.json()

def test_api_bde_gaps():
    resp = client.get("/api/v1/competitive-gaps?property_id=BER")
    assert resp.status_code == 200
    assert len(resp.json()) > 0

def test_api_ask():
    resp = client.post("/api/v1/ask", json={"question": "What is our occupancy rate?"})
    assert resp.status_code == 200
    data = resp.json()
    assert "Occupancy Rate" in data["answer"]

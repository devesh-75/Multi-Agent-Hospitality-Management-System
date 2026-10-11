"""
LangGraph Multi-Agent Orchestration Workflow
Coordinates specialized agents into a unified, stateful graph:
- Coordinator / Router Node
- Reconciliation Agent Node
- Expense Tracking Agent Node
- Revenue Insight Agent Node
- Reporting Agent Node
- BDE / Competitive Intelligence Agent Node
- Response Synthesizer Node
"""

import logging
from typing import Dict, Any
from datetime import datetime
from langgraph.graph import StateGraph, END
from sqlalchemy.orm import Session

from agents.state import AgentState
from agents.reconciliation_agent import ReconciliationAgent
from agents.expense_agent import ExpenseAgent
from agents.revenue_agent import RevenueAgent
from agents.reporting_agent import ReportingAgent
from agents.bde_agent import BDEAgent

logger = logging.getLogger(__name__)

class HospitalityAgentWorkflow:

    def __init__(self, db: Session):
        self.db = db
        self.reconciliation_agent = ReconciliationAgent(db)
        self.expense_agent = ExpenseAgent(db)
        self.revenue_agent = RevenueAgent(db)
        self.reporting_agent = ReportingAgent(db)
        self.bde_agent = BDEAgent(db)
        self.graph = self._build_graph()

    def _coordinator_node(self, state: AgentState) -> AgentState:
        """Determines workflow routing based on query intent and requested agent."""
        query = (state.get("query") or "").lower()
        requested = state.get("requested_agent")
        
        audit = state.get("audit_trail", [])
        audit.append({
            "stage": "coordinator",
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "target": requested or "auto-detected"
        })
        state["audit_trail"] = audit
        return state

    def _reconciliation_node(self, state: AgentState) -> AgentState:
        prop_id = state.get("property_id")
        res = self.reconciliation_agent.run_reconciliation(property_id=prop_id)
        state["reconciliation_data"] = res
        return state

    def _expense_node(self, state: AgentState) -> AgentState:
        prop_id = state.get("property_id")
        res = self.expense_agent.run_expense_audit(property_id=prop_id)
        state["expense_data"] = res
        return state

    def _revenue_node(self, state: AgentState) -> AgentState:
        prop_id = state.get("property_id")
        res = self.revenue_agent.run_revenue_analysis(property_id=prop_id)
        state["revenue_data"] = res
        return state

    def _reporting_node(self, state: AgentState) -> AgentState:
        prop_id = state.get("property_id")
        rep = self.reporting_agent.generate_report(report_type="CONSOLIDATED_EXECUTIVE", property_id=prop_id)
        state["reporting_data"] = rep
        return state

    def _bde_node(self, state: AgentState) -> AgentState:
        prop_id = state.get("property_id") or "BER"
        comp_overview = self.bde_agent.get_competitor_overview(prop_id)
        gaps = self.bde_agent.analyze_feature_gaps(prop_id)
        swot = self.bde_agent.generate_swot_analysis(prop_id)
        opps = self.bde_agent.generate_growth_opportunities(prop_id)
        state["bde_data"] = {
            "property_id": prop_id,
            "competitors": comp_overview,
            "feature_gaps": gaps,
            "swot": swot,
            "growth_opportunities": opps
        }
        return state

    def _synthesizer_node(self, state: AgentState) -> AgentState:
        """Synthesizes structured outputs into a clear executive response."""
        parts = []
        prop_label = state.get("property_id") or "Consolidated Network"
        parts.append(f"# Executive Multi-Agent Intelligence Brief: {prop_label}\n")

        if state.get("revenue_data"):
            kpis = state["revenue_data"]["kpis"]
            parts.append(f"### Revenue & Operations\n- **Booked Revenue:** €{kpis['booked_revenue']:,.2f}\n- **Collected Remittances:** €{kpis['collected_revenue']:,.2f}\n- **Occupancy Rate:** {kpis['occupancy_rate_pct']}%\n- **ADR / RevPAR:** €{kpis['adr']:.2f} / €{kpis['revpar']:.2f}\n")

        if state.get("reconciliation_data"):
            rec = state["reconciliation_data"]
            parts.append(f"### Financial Reconciliation\n- **Audited Invoices:** {rec['total_invoices_audited']} ({rec['fully_paid_count']} balanced, {rec['partially_paid_count']} partial, {rec['unpaid_count']} unpaid)\n- **OTA Exceptions:** {rec['ota_exceptions_count']} discrepancy scenarios detected\n- **Unbalanced Receivables:** €{rec['total_unbalanced_receivables']:,.2f}\n")

        if state.get("expense_data"):
            exp = state["expense_data"]
            parts.append(f"### Operating Expenses\n- **Total Recorded Spend:** €{exp['total_expenses']:,.2f}\n- **Statistical Anomalies Detected:** {exp['anomalies_detected']} unexpected spikes\n")

        if state.get("bde_data"):
            bde = state["bde_data"]
            parts.append(f"### Competitive Intelligence & BDE\n- **Tracked Competitors:** {len(bde['competitors'])}\n- **Feature Gaps Identified:** {len(bde['feature_gaps'])}\n- **Top Opportunity:** {bde['growth_opportunities'][0]['title'] if bde['growth_opportunities'] else 'N/A'}\n")

        state["final_response"] = "\n".join(parts)
        return state

    def _build_graph(self):
        builder = StateGraph(AgentState)

        # Register nodes
        builder.add_node("coordinator", self._coordinator_node)
        builder.add_node("reconciliation", self._reconciliation_node)
        builder.add_node("expense", self._expense_node)
        builder.add_node("revenue", self._revenue_node)
        builder.add_node("reporting", self._reporting_node)
        builder.add_node("bde", self._bde_node)
        builder.add_node("synthesizer", self._synthesizer_node)

        # Entry point
        builder.set_entry_point("coordinator")

        # Routing logic
        def route_decision(state: AgentState):
            req = state.get("requested_agent")
            if req == "reconciliation":
                return "reconciliation"
            elif req == "expense":
                return "expense"
            elif req == "revenue":
                return "revenue"
            elif req == "reporting":
                return "reporting"
            elif req == "bde":
                return "bde"
            else:
                return "run_all_reconciliation"

        # Sequential orchestration chain for full audit
        builder.add_conditional_edges(
            "coordinator",
            route_decision,
            {
                "reconciliation": "reconciliation",
                "expense": "expense",
                "revenue": "revenue",
                "reporting": "reporting",
                "bde": "bde",
                "run_all_reconciliation": "reconciliation"
            }
        )

        builder.add_edge("reconciliation", "expense")
        builder.add_edge("expense", "revenue")
        builder.add_edge("revenue", "reporting")
        builder.add_edge("reporting", "bde")
        builder.add_edge("bde", "synthesizer")
        builder.add_edge("synthesizer", END)

        return builder.compile()

    def run(self, state: AgentState) -> AgentState:
        """Executes compiled LangGraph multi-agent pipeline."""
        start_t = datetime.utcnow()
        if "audit_trail" not in state or state["audit_trail"] is None:
            state["audit_trail"] = []
        if "errors" not in state or state["errors"] is None:
            state["errors"] = []

        result = self.graph.invoke(state)
        result["execution_time_ms"] = int((datetime.utcnow() - start_t).total_seconds() * 1000)
        return result

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

Bug #2 Fix: Proper conditional routing — single agent runs only that agent
then goes to synthesizer. Full chain runs all five sequentially.
Each node wrapped in try/except to record errors without crashing.
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
        
        audit = state.get("audit_trail", []) or []
        audit.append({
            "stage": "coordinator",
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "target": requested or "full_chain"
        })
        state["audit_trail"] = audit
        return state

    def _safe_agent_node(self, agent_name: str, run_fn):
        """Wraps an agent execution in try/except, recording errors instead of crashing."""
        def node_fn(state: AgentState) -> AgentState:
            try:
                prop_id = state.get("property_id")
                res = run_fn(prop_id)
                state[f"{agent_name}_data"] = res
                audit = state.get("audit_trail", []) or []
                audit.append({
                    "stage": agent_name,
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "SUCCESS",
                    "summary_keys": list(res.keys()) if isinstance(res, dict) else str(type(res))
                })
                state["audit_trail"] = audit
            except Exception as e:
                logger.error(f"Agent {agent_name} failed: {e}", exc_info=True)
                errors = state.get("errors", []) or []
                errors.append(f"{agent_name}: {type(e).__name__}: {str(e)}")
                state["errors"] = errors
                audit = state.get("audit_trail", []) or []
                audit.append({
                    "stage": agent_name,
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "FAILED",
                    "error": str(e)
                })
                state["audit_trail"] = audit
            return state
        return node_fn

    def _reconciliation_node(self, state: AgentState) -> AgentState:
        return self._safe_agent_node(
            "reconciliation",
            lambda pid: self.reconciliation_agent.run_reconciliation(property_id=pid)
        )(state)

    def _expense_node(self, state: AgentState) -> AgentState:
        return self._safe_agent_node(
            "expense",
            lambda pid: self.expense_agent.run_expense_audit(property_id=pid)
        )(state)

    def _revenue_node(self, state: AgentState) -> AgentState:
        return self._safe_agent_node(
            "revenue",
            lambda pid: self.revenue_agent.run_revenue_analysis(property_id=pid)
        )(state)

    def _reporting_node(self, state: AgentState) -> AgentState:
        return self._safe_agent_node(
            "reporting",
            lambda pid: self.reporting_agent.generate_report(
                report_type="CONSOLIDATED_EXECUTIVE", property_id=pid
            )
        )(state)

    def _bde_node(self, state: AgentState) -> AgentState:
        prop_id = state.get("property_id") or "BER"
        def run_bde(_pid):
            comp_overview = self.bde_agent.get_competitor_overview(prop_id)
            gaps = self.bde_agent.analyze_feature_gaps(prop_id)
            swot = self.bde_agent.generate_swot_analysis(prop_id)
            opps = self.bde_agent.generate_growth_opportunities(prop_id)
            return {
                "property_id": prop_id,
                "competitors": comp_overview,
                "feature_gaps": gaps,
                "swot": swot,
                "growth_opportunities": opps
            }
        return self._safe_agent_node("bde", run_bde)(state)

    def _synthesizer_node(self, state: AgentState) -> AgentState:
        """Synthesizes structured outputs into a clear executive response.
        Tolerates missing or None data for any agent section."""
        parts = []
        prop_label = state.get("property_id") or "Consolidated Network"
        parts.append(f"# Executive Multi-Agent Intelligence Brief: {prop_label}\n")

        revenue_data = state.get("revenue_data")
        if revenue_data and isinstance(revenue_data, dict):
            kpis = revenue_data.get("kpis")
            if kpis:
                try:
                    parts.append(
                        f"### Revenue & Operations\n"
                        f"- **Booked Revenue:** €{kpis.get('booked_revenue', 0):,.2f}\n"
                        f"- **Collected Remittances:** €{kpis.get('collected_revenue', 0):,.2f}\n"
                        f"- **Occupancy Rate:** {kpis.get('occupancy_rate_pct', 0)}%\n"
                        f"- **ADR / RevPAR:** €{kpis.get('adr', 0):.2f} / €{kpis.get('revpar', 0):.2f}\n"
                    )
                except Exception:
                    parts.append("### Revenue & Operations\n- Data formatting error\n")

        rec_data = state.get("reconciliation_data")
        if rec_data and isinstance(rec_data, dict):
            try:
                parts.append(
                    f"### Financial Reconciliation\n"
                    f"- **Audited Invoices:** {rec_data.get('total_invoices_audited', 0)} "
                    f"({rec_data.get('fully_paid_count', 0)} balanced, "
                    f"{rec_data.get('partially_paid_count', 0)} partial, "
                    f"{rec_data.get('unpaid_count', 0)} unpaid)\n"
                    f"- **OTA Exceptions:** {rec_data.get('ota_exceptions_count', 0)} discrepancy scenarios detected\n"
                    f"- **Unbalanced Receivables:** €{rec_data.get('total_unbalanced_receivables', 0):,.2f}\n"
                )
            except Exception:
                parts.append("### Financial Reconciliation\n- Data formatting error\n")

        exp_data = state.get("expense_data")
        if exp_data and isinstance(exp_data, dict):
            try:
                parts.append(
                    f"### Operating Expenses\n"
                    f"- **Total Recorded Spend:** €{exp_data.get('total_expenses', 0):,.2f}\n"
                    f"- **Statistical Anomalies Detected:** {exp_data.get('anomalies_detected', 0)} unexpected spikes\n"
                )
            except Exception:
                parts.append("### Operating Expenses\n- Data formatting error\n")

        bde_data = state.get("bde_data")
        if bde_data and isinstance(bde_data, dict):
            try:
                competitors = bde_data.get("competitors", [])
                gaps = bde_data.get("feature_gaps", [])
                opps = bde_data.get("growth_opportunities", [])
                top_opp = opps[0]["title"] if opps else "N/A"
                parts.append(
                    f"### Competitive Intelligence & BDE\n"
                    f"- **Tracked Competitors:** {len(competitors)}\n"
                    f"- **Feature Gaps Identified:** {len(gaps)}\n"
                    f"- **Top Opportunity:** {top_opp}\n"
                )
            except Exception:
                parts.append("### Competitive Intelligence & BDE\n- Data formatting error\n")

        errors = state.get("errors")
        if errors:
            parts.append(f"\n### ⚠ Agent Errors\n")
            for err in errors:
                parts.append(f"- {err}\n")

        state["final_response"] = "\n".join(parts)
        
        audit = state.get("audit_trail", []) or []
        audit.append({
            "stage": "synthesizer",
            "timestamp": datetime.utcnow().isoformat(),
            "status": "COMPLETED",
            "sections_generated": sum(1 for k in ["revenue_data", "reconciliation_data", "expense_data", "bde_data", "reporting_data"] if state.get(k))
        })
        state["audit_trail"] = audit
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

        # Routing logic: single agent goes directly to that agent then synthesizer
        # "all" or None goes through full chain
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
                return "run_all"

        builder.add_conditional_edges(
            "coordinator",
            route_decision,
            {
                "reconciliation": "reconciliation",
                "expense": "expense",
                "revenue": "revenue",
                "reporting": "reporting",
                "bde": "bde",
                "run_all": "reconciliation"
            }
        )

        # Single-agent paths: each goes directly to synthesizer
        # We need conditional edges from each agent node:
        # If requested_agent is set (single), go to synthesizer
        # If running all (requested_agent is None), continue the chain

        def after_reconciliation(state: AgentState):
            return "synthesizer" if state.get("requested_agent") else "expense"
        
        def after_expense(state: AgentState):
            return "synthesizer" if state.get("requested_agent") else "revenue"

        def after_revenue(state: AgentState):
            return "synthesizer" if state.get("requested_agent") else "reporting"

        def after_reporting(state: AgentState):
            return "synthesizer" if state.get("requested_agent") else "bde"

        def after_bde(state: AgentState):
            return "synthesizer"

        builder.add_conditional_edges("reconciliation", after_reconciliation, {
            "synthesizer": "synthesizer",
            "expense": "expense"
        })
        builder.add_conditional_edges("expense", after_expense, {
            "synthesizer": "synthesizer",
            "revenue": "revenue"
        })
        builder.add_conditional_edges("revenue", after_revenue, {
            "synthesizer": "synthesizer",
            "reporting": "reporting"
        })
        builder.add_conditional_edges("reporting", after_reporting, {
            "synthesizer": "synthesizer",
            "bde": "bde"
        })
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

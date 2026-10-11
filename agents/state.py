"""
LangGraph Typed State Definition for Multi-Agent Hospitality Orchestration
"""

from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime

class AgentState(TypedDict, total=False):
    # Workflow Input Context
    query: str
    property_id: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    requested_agent: Optional[str] # reconciliation, expense, revenue, reporting, bde, or all

    # Specialized Agent Outputs
    reconciliation_data: Optional[Dict[str, Any]]
    expense_data: Optional[Dict[str, Any]]
    revenue_data: Optional[Dict[str, Any]]
    reporting_data: Optional[Dict[str, Any]]
    bde_data: Optional[Dict[str, Any]]

    # Retrieval Context (RAG)
    retrieved_documents: Optional[List[Dict[str, Any]]]

    # Orchestration / Coordination Output
    final_response: Optional[str]
    structured_output: Optional[Dict[str, Any]]
    audit_trail: List[Dict[str, Any]]
    errors: List[str]
    execution_time_ms: int

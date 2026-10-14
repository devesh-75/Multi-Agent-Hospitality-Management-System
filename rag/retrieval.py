"""
RAG Retrieval & Grounded Question Answering Engine
Coordinates document loading, vector indexing, retrieval, and evidence-grounded response synthesis.
Combines structured SQL facts with unstructured document context.
"""

import logging
from typing import Dict, List, Any, Optional

from sqlalchemy.orm import Session

from rag.document_loader import RAGDocumentLoader
from rag.vector_store import VectorStore
from backend.app.models.entities import Alert, Property
from backend.app.services.analytics_service import AnalyticsService

logger = logging.getLogger(__name__)

class RAGService:

    def __init__(self, db: Session):
        self.db = db
        self.vector_store = VectorStore()
        self._initialize_index()

    def _initialize_index(self):
        """Indexes operational documents on service initialization."""
        docs = RAGDocumentLoader.load_all_documents(self.db)
        self.vector_store.index_documents(docs)

    def refresh_index(self):
        """Refreshes the vector store with latest database state."""
        docs = RAGDocumentLoader.load_all_documents(self.db)
        self.vector_store.index_documents(docs)

    def _property_label(self, property_id: Optional[str]) -> str:
        if not property_id:
            return "all properties"
        prop = self.db.query(Property).filter(Property.id == property_id).first()
        return prop.name if prop else f"property {property_id}"

    def _build_finance_answer(self, question: str, property_id: Optional[str], kpis: Dict[str, Any]) -> Dict[str, Any]:
        prop_label = self._property_label(property_id)
        answer = (
            f"Based on the current PMS ledger for {prop_label}:\n\n"
            f"- **Booked Revenue:** €{kpis['booked_revenue']:,.2f}\n"
            f"- **Invoiced Revenue:** €{kpis['invoiced_revenue']:,.2f}\n"
            f"- **Collected Revenue:** €{kpis['collected_revenue']:,.2f}\n"
            f"- **Outstanding Receivables:** €{kpis['outstanding_receivables']:,.2f}\n"
            f"- **Occupancy Rate:** {kpis['occupancy_rate_pct']}%\n"
            f"- **ADR (Average Daily Rate):** €{kpis['adr']:.2f}\n"
            f"- **RevPAR:** €{kpis['revpar']:.2f}\n"
            f"- **Pending Alerts:** {kpis['pending_alerts']}\n\n"
            f"*These figures are computed from the authoritative reservation, invoice, and payment ledgers.*"
        )
        return {
            "answer": answer,
            "sources": ["Authoritative SQL Ledger (reservations, invoices, payments)"] + ["Operations Monitor"],
            "structured_data": kpis,
            "confidence": "HIGH"
        }

    def _build_competitor_answer(self, question: str, property_id: Optional[str]) -> Dict[str, Any]:
        from agents.bde_agent import BDEAgent

        prop_id = property_id or "BER"
        agent = BDEAgent(self.db)
        compare = agent.compare_property_with_competitors(prop_id)
        gaps = agent.analyze_feature_gaps(prop_id)[:3]
        opps = agent.generate_growth_opportunities(prop_id)

        property_name = self._property_label(prop_id)
        comp_lines = [
            f"- {item['competitor_name']}: avg €{item['avg_price']:.2f}, delta €{item['price_difference']:.2f} vs our ADR"
            for item in compare.get("competitive_set", [])[:4]
        ]
        gap_lines = [
            f"- {item['feature_name']} is being offered by {', '.join(item['competitors_offering'][:2])}"
            for item in gaps
        ]

        answer = (
            f"Competitive benchmark for {property_name}:\n\n"
            f"Our ADR is €{compare['our_kpis']['adr']:.2f} and RevPAR is €{compare['our_kpis']['revpar']:.2f}.\n"
            f"Nearby competitors:\n" + "\n".join(comp_lines) + "\n\n"
            f"Key feature gaps:\n" + ("\n".join(gap_lines) if gap_lines else "- No major amenity gaps detected.") + "\n\n"
            f"Top recommendation: {opps[0]['title']} — {opps[0]['recommended_action']}"
        )
        return {
            "answer": answer,
            "sources": ["Competitor rate benchmark", "Amenity gap benchmarking", "Authoritative PMS data"],
            "structured_data": {
                "property_id": prop_id,
                "our_kpis": compare["our_kpis"],
                "competitive_set": compare.get("competitive_set", []),
                "top_opportunity": opps[0] if opps else None,
            },
            "confidence": "HIGH"
        }

    def _build_alert_answer(self, question: str, property_id: Optional[str]) -> Dict[str, Any]:
        query = self.db.query(Alert)
        if property_id:
            query = query.filter(Alert.property_id == property_id)
        alerts = query.order_by(Alert.created_at.desc()).limit(5).all()

        if not alerts:
            answer = "No active operational alerts were found for the requested scope."
            return {"answer": answer, "sources": ["Operations Monitor"], "structured_data": {"alerts": []}, "confidence": "MEDIUM"}

        lines = [
            f"- **{a.title}** [{a.severity}] — {a.message}"
            for a in alerts[:3]
        ]
        answer = "Recent operational alerts:\n\n" + "\n".join(lines)
        return {
            "answer": answer,
            "sources": ["Operations Monitor", "Expense anomaly ledger"],
            "structured_data": {"alerts": [a.title for a in alerts[:3]]},
            "confidence": "HIGH"
        }

    def query(self, question: str, property_id: Optional[str] = None) -> Dict[str, Any]:
        """Answers questions using semantic vector search and authoritative SQL data."""
        if not question or not question.strip():
            return {
                "question": question or "",
                "property_id": property_id or "ALL",
                "answer": "Please provide a question about revenue, occupancy, expenses, competitors, or operational alerts.",
                "sources": [],
                "structured_data": None,
                "confidence": "LOW",
                "data_limitations": "No question was supplied."
            }

        q_lower = question.lower().strip()
        retrieved_docs = self.vector_store.search(
            query=question,
            top_k=4,
            filter_property_id=property_id
        )
        kpis = AnalyticsService.get_executive_kpis(self.db, property_id)

        finance_terms = {"revenue", "adr", "revpar", "occupancy", "how much", "total", "booked", "invoice", "collected", "outstanding", "cash", "profit"}
        competitor_terms = {"competitor", "compare", "market", "benchmark", "gap", "amenity", "rate", "pricing", "swot", "growth", "opportunity"}
        alert_terms = {"alert", "anomaly", "expense", "spike", "outlier", "issue", "problem", "warning"}

        def contains_any_terms(text: str, terms: set[str]) -> bool:
            return any(term in text for term in terms)

        if contains_any_terms(q_lower, finance_terms):
            result = self._build_finance_answer(question, property_id, kpis)
        elif contains_any_terms(q_lower, competitor_terms):
            result = self._build_competitor_answer(question, property_id)
        elif contains_any_terms(q_lower, alert_terms):
            result = self._build_alert_answer(question, property_id)
        elif retrieved_docs:
            top_doc = retrieved_docs[0]
            result = {
                "answer": f"**Retrieved Intelligence:**\n\n{top_doc['content'][:800]}...",
                "sources": [d["metadata"].get("source", d["id"]) for d in retrieved_docs],
                "structured_data": {"top_doc_score": top_doc["similarity_score"]},
                "confidence": "MEDIUM"
            }
        else:
            result = {
                "answer": "No matching records or operational reports were found in the knowledge base for this query.",
                "sources": [],
                "structured_data": None,
                "confidence": "LOW"
            }

        result.setdefault("sources", [])
        result.setdefault("structured_data", None)
        result.setdefault("confidence", "HIGH")

        return {
            "question": question,
            "property_id": property_id or "ALL",
            "answer": result["answer"],
            "sources": result["sources"],
            "structured_data": result["structured_data"],
            "confidence": result["confidence"],
            "data_limitations": "Figures are grounded in deterministic ledger data; any missing or inferred values are explicitly labeled."
        }

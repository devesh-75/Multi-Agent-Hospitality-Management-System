"""
RAG Document Loader
Extracts structured documents from database entities for vector indexing:
- Formal operational & financial reports
- Reconciliation exception summaries
- Expense audit findings
- Competitor intelligence & feature benchmark profiles
"""

import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from backend.app.models.entities import Report, Competitor, CompetitorFeature, Property, Alert

logger = logging.getLogger(__name__)

class RAGDocumentLoader:

    @staticmethod
    def load_all_documents(db: Session) -> List[Dict[str, Any]]:
        """Extracts text documents with rich metadata for vector indexing."""
        documents = []

        # 1. Generated Reports
        reports = db.query(Report).all()
        for r in reports:
            documents.append({
                "id": f"DOC-REP-{r.id}",
                "content": f"REPORT TYPE: {r.report_type}\nPROPERTY: {r.property_id}\nPERIOD: {r.period_start} to {r.period_end}\n\n{r.content}",
                "metadata": {
                    "doc_type": "report",
                    "report_type": r.report_type,
                    "property_id": r.property_id,
                    "created_at": r.created_at.isoformat(),
                    "source": "ReportingAgent"
                }
            })

        # 2. Competitor Intelligence Profiles
        competitors = db.query(Competitor).all()
        for c in competitors:
            feats = db.query(CompetitorFeature).filter(CompetitorFeature.competitor_id == c.id).all()
            feat_list = [f"{f.feature_name} ({f.status})" for f in feats]
            
            comp_text = f"""COMPETITOR INTELLIGENCE PROFILE
Name: {c.name}
Brand: {c.brand or 'Independent'}
City: {c.city}, Country: {c.country_code}
Target Competing Hotel: {c.target_property_id}
Star Rating: {c.star_rating}
Proximity Distance: {c.distance_km} km
Tracked Amenities:
{chr(10).join(['- ' + fl for fl in feat_list])}
"""
            documents.append({
                "id": f"DOC-COMP-{c.id}",
                "content": comp_text,
                "metadata": {
                    "doc_type": "competitor_profile",
                    "competitor_id": c.id,
                    "property_id": c.target_property_id,
                    "city": c.city,
                    "source": "BDEAgent"
                }
            })

        # 3. Operational Alerts
        alerts = db.query(Alert).all()
        for a in alerts:
            documents.append({
                "id": f"DOC-ALT-{a.id}",
                "content": f"OPERATIONAL ALERT: {a.title}\nTYPE: {a.alert_type}\nSEVERITY: {a.severity}\nPROPERTY: {a.property_id}\nMESSAGE: {a.message}",
                "metadata": {
                    "doc_type": "alert",
                    "alert_type": a.alert_type,
                    "severity": a.severity,
                    "property_id": a.property_id or "ALL",
                    "created_at": a.created_at.isoformat(),
                    "source": "OperationsMonitor"
                }
            })

        logger.info(f"Loaded {len(documents)} structured knowledge documents for RAG indexing.")
        return documents

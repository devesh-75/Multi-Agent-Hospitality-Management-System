# System Architecture: Agentic Layer for Fintech Operations in Hospitality

## 1. Architectural Philosophy & Design Principles

The system addresses the disconnect between legacy Property Management Systems (PMS) and modern autonomous financial intelligence. In conventional hotel operations, front-desk staff, night auditors, and revenue managers manually reconcile folios, audit OTA remittance statements, detect expense leaks, and monitor competitor prices across disconnected spreadsheets.

This platform implements an event-driven, multi-agent AI architecture structured across five sequential operational layers:

```
+--------------------------------------------------------------------------------------------------+
|                                    1. DATA INGESTION & NORMALIZATION                             |
|  - Source: C:\Users\deves\Downloads\project (Apaleo Open-PMS CSVs & Audit Suites)                |
|  - Adapters: CSVPMSAdapter (Current) | BookingCenterPMSAdapter (Extensible Interface)            |
|  - Extraction: Unpacks nested JSON (guests, rooms, line_items) -> Third Normal Form (3NF)        |
+--------------------------------------------------------------------------------------------------+
                                                 │
                                                 ▼
+--------------------------------------------------------------------------------------------------+
|                                     2. UNIFIED DATABASE LAYER                                    |
|  - Operational Database: PostgreSQL 15+ / SQLite3 Fallback (sqlite:///./data/hospitality.db)     |
|  - Core Schema: properties, rooms, room_types, guests, reservations, folios, invoices, payments  |
|  - Fintech Schema: charges, ota_settlements, expenses, alerts, reports                           |
|  - BDE Schema: competitors, competitor_features, competitor_prices, competitor_reviews           |
+--------------------------------------------------------------------------------------------------+
                                                 │
                                                 ▼
+--------------------------------------------------------------------------------------------------+
|                                 3. EVENT STREAMING & MESSAGING (KAFKA)                           |
|  - Apache Kafka topics: hospitality.reservation, hospitality.payment, hospitality.ota_settlement |
|  - Development Mode: In-database asynchronous event queue (business_events ledger)              |
|  - Decoupled dispatching to subscribed AI agents without synchronous blocking                    |
+--------------------------------------------------------------------------------------------------+
                                                 │
                                                 ▼
+--------------------------------------------------------------------------------------------------+
|                                  4. SPECIALIZED AGENTIC AI LAYER                                 |
|  - Orchestrator: LangGraph StateGraph with typed AgentState and conditional routing             |
|  - Specialized Agents:                                                                           |
|     * Reconciliation Agent: Invoice vs Payment matching & OTA remittance auditing                |
|     * Expense Agent: Statistical Z-score outlier detection & departmental cost allocation       |
|     * Revenue Agent: ADR, RevPAR, Occupancy decomposition & 14-day trend forecasting             |
|     * Reporting Agent: Automated executive summaries & exception reports                         |
|     * BDE Agent: Competitor rate benchmarking, amenity feature-gap analysis, grounded SWOT       |
+--------------------------------------------------------------------------------------------------+
                                                 │
                                                 ▼
+--------------------------------------------------------------------------------------------------+
|                            5. RETRIEVAL-AUGMENTED GENERATION (RAG) & APIs                        |
|  - Qdrant Vector Database / In-Memory Semantic Index with dense hash embeddings                  |
|  - Deterministic SQL verification for numeric queries; vector context for qualitative synthesis  |
|  - FastAPI REST Backend (Port 8000) -> React.js Modern Fintech Dashboard (Port 3000 / 5173)     |
+--------------------------------------------------------------------------------------------------+
```

---

## 2. Multi-Property Treasury Synchronization

The platform supports 5 European metropolitan properties within a consolidated schema:
1. `BER`: Hotel Berlin (Berlin, Germany | EUR)
2. `LND`: Hotel London (London, United Kingdom | GBP)
3. `MUC`: Hotel Munich (Munich, Germany | EUR)
4. `PAR`: Hotel Paris (Paris, France | EUR)
5. `VIE`: Hotel Vienna (Vienna, Austria | EUR)

Cross-property synchronization maintains local currency integrity (EUR vs GBP) and aggregates group-level treasury performance (consolidated Gross Booked Revenue, Invoiced Revenue, Collected Remittances, and Net Operating Income).

---

## 3. Resilience, Fallbacks & Offline Capability

To ensure zero dependencies on third-party paid subscriptions or complex cloud infrastructure during development and evaluation:
1. **Database Fallback:** Runs on PostgreSQL when configured (`DATABASE_URL`), defaulting to zero-configuration SQLite (`data/hospitality.db`).
2. **Event Streaming Fallback:** Runs with live Apache Kafka brokers when active, falling back to a persistent transactional `business_events` table in SQLite/PostgreSQL.
3. **Embeddings & Vector Fallback:** Connects to Qdrant cluster when reachable, falling back to an in-memory cosine vector store with deterministic 128-dimensional embeddings.
4. **Calculations:** 100% of financial figures, variances, ADR, RevPAR, and occupancy rates are calculated deterministically using Python and SQL. Language models are strictly utilized for synthesis, explanation, and interpretation.

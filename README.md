# Agentic Layer for Fintech Operations in Hospitality Services

[![Tests: 14 Passed](https://img.shields.io/badge/Tests-14%20Passed-success.svg)](docs/TESTING.md)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI: 0.110+](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React: 18](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![LangGraph: Orchestrated](https://img.shields.io/badge/LangGraph-Multi--Agent-orange.svg)](https://langchain.com/)

An integrated, enterprise-grade final-year engineering project combining Property Management System (PMS) operations, autonomous financial reconciliation, specialized AI agents, competitive intelligence, hybrid Retrieval-Augmented Generation (RAG), and a centralized decision-support dashboard.

---

## 1. Project Overview

Hospitality properties generate dense, continuous streams of operational and financial data: room allocations, guest folio postings, municipal tax charges, payment gateway transactions, and Online Travel Agency (OTA) net remittances. In traditional hotel chains, this data is siloed within legacy Property Management Systems (PMS), leaving front-desk clerks, night auditors, and revenue managers dependent on manual spreadsheet reconciliation and static reporting.

This project delivers an autonomous **Agentic Layer for Fintech Operations in Hospitality Services**. It consumes raw PMS data streams, normalizes them into a unified operational database, executes event-driven multi-agent reasoning using **LangGraph**, automates ledger reconciliation, detects operational spending anomalies, benchmarks local market competitors, and provides evidence-grounded decision support through a modern web dashboard.

---

## 2. Business Problem

Hotel financial operations face three critical pain points:
1. **Folio & Remittance Reconciliation Latency:** Mismatches between guest invoice gross amounts, payment gateway settlements, and OTA net payouts (e.g. Booking.com, Expedia commissions) require hours of manual verification, resulting in uncollected balances and commission leakage.
2. **Hidden Operational Cost Spikes:** Departmental expenses (emergency maintenance, utility spikes, linen replacements) are often audited weeks after payment, preventing proactive cost containment.
3. **Siloed Competitive Positioning:** Hotel managers lack real-time visibility into local competitor pricing, amenity gaps, and market review sentiment, leading to mispriced room nights during demand surges.

The application answers three central executive questions:
- *What is happening inside our hospitality business?* (Internal PMS & ledger operations)
- *What is happening around our business and among competitors?* (Market rates & amenity gaps)
- *What actions could improve our financial performance and market position?* (Actionable growth recommendations)

---

## 3. Core Objectives

- **PMS Ingestion & Normalization:** Ingest real PMS exports (`C:\Users\deves\Downloads\project`) without data destruction, extracting nested JSON entities (rooms, guests, line items) into a unified relational database.
- **Automated Ledger Reconciliation:** Multi-way matching across invoices, recorded payments, and OTA remittances with automated exception tagging (underpayments, overpayments, missing payouts).
- **Statistical Expense Auditing:** Categorical cost allocation with $Z \ge 2.0\sigma$ statistical anomaly detection.
- **Empirical Yield Analytics:** Deterministic calculation of Average Daily Rate (ADR), Revenue Per Available Room (RevPAR), Occupancy %, and 14-day trend forecasting.
- **Specialized Multi-Agent Orchestration:** Coordinated **LangGraph** workflow featuring 5 specialized analytical agents.
- **Business Development Executive (BDE) Intelligence:** Competitor rate comparisons, amenity feature-gap analysis, data-grounded SWOT, and 8-part structured growth recommendations.
- **Hybrid RAG Knowledge Layer:** Authoritative deterministic SQL for numerical queries combined with dense vector semantic search over indexed reports.
- **Multi-Property Treasury Consolidation:** Synchronized reporting across 5 European properties (Berlin, London, Munich, Paris, Vienna).

---

## 4. System Architecture

The application is structured into five cohesive tiers:

```
[ Raw CSV Datasets: C:\Users\deves\Downloads\project ]
                        │
                        ▼
[ Ingestion & Normalization Engine (CSVPMSAdapter) ]
                        │
                        ▼
[ Unified Relational Database (PostgreSQL 15+ / SQLite3) ]
                        │
                        ▼
[ Business Event Streaming (Apache Kafka / DB Queue) ]
                        │
                        ▼
[ LangGraph Multi-Agent AI Layer ]
  ├── Reconciliation Agent (Invoice & OTA Remittance Matching)
  ├── Expense Tracking Agent (Z-Score Outlier Detection)
  ├── Revenue Insight Agent (ADR, RevPAR, 14-Day Forecasting)
  ├── Reporting Agent (Automated Executive Summaries)
  └── BDE Competitive Intelligence Agent (Feature Gaps & SWOT)
                        │
                        ▼
[ Hybrid RAG Layer (SQL Ledgers + Qdrant / Vector Index) ]
                        │
                        ▼
[ FastAPI Backend REST Services (Port 8000) ]
                        │
                        ▼
[ React.js Modern Fintech Dashboard (Port 3000 / 5173) ]
```

For full architectural diagrams and specifications, see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

## 5. Technology Stack

- **Primary Backend:** Python 3.10+, FastAPI, Uvicorn, Pydantic v2.10
- **Operational Database:** PostgreSQL 15+ (SQLite3 compatible fallback for instant local evaluation)
- **Object Relational Mapper (ORM):** SQLAlchemy 2.0
- **Data Engineering & Analytics:** Pandas 2.2, NumPy, SciPy
- **Agent Orchestration:** LangGraph 0.0.30+, LangChain Core
- **Vector Database & RAG:** Qdrant Client 1.19+ / Local In-Memory Dense Vector Store
- **Event Streaming:** Apache Kafka (kafka-python-ng) / Transactional Database Event Ledger
- **Frontend Dashboard:** React 18, Vite, Lucide React, Modern Vanilla CSS Design System
- **Testing Framework:** Pytest 8.1+, FastAPI TestClient, HTTPX
- **Containerization:** Docker, Docker Compose

---

## 6. Repository Structure

```text
agentic-hospitality/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI application entrypoint
│   │   ├── api/endpoints/           # Modular REST endpoints (health, revenue, bde, etc.)
│   │   ├── core/                    # Config settings and SQLAlchemy database session
│   │   ├── models/                  # SQLAlchemy ORM unified entities
│   │   ├── schemas/                 # Pydantic DTO request/response schemas
│   │   └── services/                # Deterministic analytics service (ADR, RevPAR, forecasting)
│   ├── requirements.txt             # Pinned Python dependencies
│   └── Dockerfile                   # Production backend container specification
├── agents/
│   ├── state.py                     # LangGraph typed AgentState definition
│   ├── workflow.py                  # LangGraph StateGraph coordinator and routing
│   ├── reconciliation_agent.py      # Invoice, payment & OTA settlement matching agent
│   ├── expense_agent.py             # Departmental spend & z-score anomaly agent
│   ├── revenue_agent.py             # Yield analytics & dynamic pricing agent
│   ├── reporting_agent.py           # Standardized executive report generation agent
│   └── bde_agent.py                 # Competitor intelligence & SWOT agent (Section 14)
├── rag/
│   ├── document_loader.py           # Knowledge extractor for reports and competitor profiles
│   ├── embeddings.py                # Dense vector embedder (OpenAI + local fallback)
│   ├── vector_store.py              # Qdrant interface with local memory index fallback
│   └── retrieval.py                 # Semantic retrieval and grounded question answering
├── ingestion/
│   ├── source_adapters/             # BasePMSAdapter, CSVPMSAdapter, BookingCenterPMSAdapter
│   ├── validate_data.py             # Pre-ingestion schema & referential integrity validator
│   └── load_data.py                 # Idempotent database loader pipeline
├── kafka/
│   ├── event_schemas/               # Standardized CloudEvents payload schemas
│   ├── producer.py                  # Kafka publisher with database ledger fallback
│   └── consumer.py                  # Event consumer and agent subscription dispatcher
├── dashboard/
│   ├── src/
│   │   ├── App.jsx                  # Main dashboard controller and view switcher
│   │   ├── api.js                   # Centralized API service client
│   │   ├── index.css                # Premium hospitality-fintech dark theme
│   │   ├── components/              # Sidebar and Header components
│   │   └── views/                   # 12 interactive dashboard views
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── database/
│   └── schema.sql                   # ANSI SQL unified schema compatible with Postgres & SQLite
├── scripts/
│   ├── inspect_datasets.py          # Automated CSV profiling script
│   └── seed_missing_entities.py     # Deterministic generator for expenses & competitors (seed 42)
├── tests/
│   └── test_backend.py              # 14 automated pytest test cases
├── docs/
│   ├── ARCHITECTURE.md
│   ├── AGENT_WORKFLOWS.md
│   ├── KAFKA_EVENTS.md
│   ├── API_DOCUMENTATION.md
│   ├── RAG_DESIGN.md
│   ├── BDE_COMPETITIVE_INTELLIGENCE.md
│   ├── DATA_INVENTORY.md
│   ├── DATA_DICTIONARY.md
│   ├── DATA_MAPPING.md
│   ├── DATA_QUALITY_REPORT.md
│   ├── TESTING.md
│   └── LIMITATIONS.md
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 7. Dataset Directory & Discovery Process

The primary data source is the user's project directory:

`C:\Users\deves\Downloads\project`

### Discovery Audit Summary
The directory contains **8 primary CSV files** totaling **407.3 KB** and **1,030 total records**:
- `properties.csv`: 5 European properties (`BER`, `LND`, `MUC`, `PAR`, `VIE`).
- `reservations.csv`: 100 reservations with nested JSON entities (rooms, room types, rate plans, guests).
- `folios.csv`: 205 folios (100 guest folios, 100 booking master folios, 5 house accounts).
- `invoices.csv`: 200 statutory invoices with itemized charge lines. Total gross: €34,238.80.
- `charges_full.csv`: 200 itemized guest charges across Room, Breakfast, Restaurant, Minibar, Parking.
- `payments_full.csv`: 100 payment transactions with credit card, bank transfer, and cash references.
- `synthetic_invoices_full.csv`: 100 benchmark invoices for reconciliation auditing.
- `ota_reservations_full.csv`: 20 OTA bookings covering 5 audit scenarios (`exact`, `underpayment`, `overpayment`, `missing_settlement`, `commission_discrepancy`).

Detailed audit findings are documented in [`docs/DATA_INVENTORY.md`](docs/DATA_INVENTORY.md) and [`docs/DATA_QUALITY_REPORT.md`](docs/DATA_QUALITY_REPORT.md).

---

## 8. Data Dictionary & Unified Mappings

Source data columns and JSON sub-fields are mapped into 3NF normalized tables:
- `reservations.csv -> unit_data` $\rightarrow$ `rooms` table (99 physical units).
- `reservations.csv -> unit_group_data` $\rightarrow$ `room_types` table (5 categories).
- `reservations.csv -> primary_guest` $\rightarrow$ `guests` table (91 unique guest profiles).
- `invoices.csv -> line_items` $\rightarrow$ `invoice_items` table (400 charge lines).

Refer to [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md) and [`docs/DATA_MAPPING.md`](docs/DATA_MAPPING.md).

---

## 9. Database Setup

The unified schema is defined in [`database/schema.sql`](database/schema.sql).

### PostgreSQL Setup (Docker / Local Service)
```sql
CREATE DATABASE hospitality_db;
-- Schema initializes automatically on application startup via SQLAlchemy Base.metadata.create_all()
```

### SQLite Fallback (Zero Setup)
By default, the application runs on `sqlite:///./data/hospitality.db`. The SQLite database initializes automatically when running `ingestion/load_data.py`.

---

## 10. Environment Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Key environment variables:
```ini
ENVIRONMENT=development
DEBUG=true

# Database Connection (PostgreSQL or SQLite)
DATABASE_URL=sqlite:///./data/hospitality.db

# Source Datasets Directory
SOURCE_DATA_DIR=C:\Users\deves\Downloads\project

# Apache Kafka (Optional)
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_ENABLED=false

# Qdrant Vector Store (Optional)
QDRANT_URL=http://localhost:6333
QDRANT_ENABLED=false

# OpenAI (Optional - System operates deterministically without keys)
OPENAI_API_KEY=
LLM_MODEL=gpt-4o-mini
```

---

## 11. Backend Setup & Ingestion

### Step 1: Create and Activate Virtual Environment
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 3: Run Ingestion Pipeline
Ingests all 8 CSV files from `C:\Users\deves\Downloads\project` and seeds missing domains:
```bash
python ingestion/load_data.py
```

### Step 4: Start FastAPI Backend Server
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be live at `http://localhost:8000/docs`.

---

## 12. Frontend Setup

### Step 1: Install Node.js Dependencies
```bash
cd dashboard
npm install
```

### Step 2: Start Development Server
```bash
npm run dev
```
The dashboard interface will be accessible at `http://localhost:5173`.

---

## 13. Kafka Event Streaming

The event pipeline is documented in [`docs/KAFKA_EVENTS.md`](docs/KAFKA_EVENTS.md).
- When a Kafka broker is running at `localhost:9092` with `KAFKA_ENABLED=true`, the `EventProducer` publishes CloudEvents to topics such as `hospitality.reservation` and `hospitality.payment`.
- In development mode (`KAFKA_ENABLED=false`), events are recorded in the transactional `business_events` table and consumed by `kafka/consumer.py`.

---

## 14. Qdrant & RAG Setup

The hybrid RAG system is detailed in [`docs/RAG_DESIGN.md`](docs/RAG_DESIGN.md).
- Connects to Qdrant at `http://localhost:6333` when `QDRANT_ENABLED=true`.
- Falls back to an in-memory dense vector store with 128-dimensional deterministic hash embeddings when offline.
- Indexes formal operational reports, alerts, and competitor intelligence profiles.

---

## 15. Specialized AI Agents

Implemented via **LangGraph** in [`agents/workflow.py`](agents/workflow.py):
1. **Reconciliation Agent:** Audits 300 invoices and 20 OTA payouts, detecting underpayments, overpayments, missing payouts, and commission mismatches.
2. **Expense Tracking Agent:** Audits 92 operating expenses, identifying a $Z \ge 2.0\sigma$ emergency HVAC maintenance spike in September (€7,850.00).
3. **Revenue Insight Agent:** Computes ADR (€117.69), RevPAR, Occupancy rate, and 14-day trend forecast.
4. **Reporting Agent:** Generates formal executive briefs and archives them in the database.
5. **BDE Agent:** Evaluates market competitors, amenity gaps, SWOT, and strategic opportunities.

See [`docs/AGENT_WORKFLOWS.md`](docs/AGENT_WORKFLOWS.md).

---

## 16. Business Development Executive (BDE) Workflow

Full details are documented in [`docs/BDE_COMPETITIVE_INTELLIGENCE.md`](docs/BDE_COMPETITIVE_INTELLIGENCE.md):
- **12 Tracked Competitors:** Benchmarking against Motel One, CitizenM, The Hoxton, Mama Shelter, and 25hours across 5 capital cities.
- **Amenity Feature-Gap Analysis:** Identifies amenities offered by competitors (e.g. Keyless Mobile Check-In, Rooftop Bar) that our property lacks.
- **Empirical SWOT Analysis:** Cites actual revenue figures, receivables balances, and competitor distances.
- **Actionable Growth Opportunities:** 8-part structured recommendations with expected impact and human validation requirements.
- **Ask BDE AI:** Dedicated natural-language query assistant for competitive intelligence.

---

## 17. REST API Endpoints Summary

- `GET /health`: Health and infrastructure status.
- `GET /api/v1/properties`: List of properties.
- `GET /api/v1/reservations`: Searchable reservation ledger.
- `GET /api/v1/revenue`: Executive KPIs, revenue waterfall, and 14-day forecast.
- `GET /api/v1/revenue/comparison`: Multi-property consolidation matrix.
- `GET /api/v1/invoices`: Invoices and line items.
- `GET /api/v1/reconciliation`: Ledger reconciliation and OTA exceptions.
- `POST /api/v1/reconciliation/run`: Trigger Reconciliation Agent.
- `GET /api/v1/expenses`: Departmental spend and statistical anomalies.
- `GET /api/v1/competitors`: Competitor profiles.
- `GET /api/v1/competitor-comparison`: ADR comparison vs local competitors.
- `GET /api/v1/competitive-gaps`: Amenity feature-gap analysis.
- `GET /api/v1/swot-analysis`: Grounded SWOT analysis.
- `GET /api/v1/business-opportunities`: Evidence-based growth recommendations.
- `POST /api/v1/bde/ask`: Natural-language competitive intelligence queries.
- `POST /api/v1/agents/run`: Trigger LangGraph multi-agent pipeline.
- `POST /api/v1/ask`: Hybrid SQL + RAG question answering endpoint.

Full reference in [`docs/API_DOCUMENTATION.md`](docs/API_DOCUMENTATION.md).

---

## 18. Automated Testing Instructions

Execute the automated test suite verifying all 14 core business capabilities:

```bash
.\venv\Scripts\pytest.exe -v tests\test_backend.py
```

Results: **14 Passed in 1.62s**. Details in [`docs/TESTING.md`](docs/TESTING.md).

To validate the frontend build:
```bash
cd dashboard
npm run build
```

---

## 19. Docker & Container Deployment

To launch the full enterprise stack via Docker Compose:

```bash
docker compose up --build
```

Services initialized:
- PostgreSQL 15 (`5432`)
- Qdrant Vector DB (`6333`)
- Apache Kafka Kraft (`9092`)
- FastAPI Backend (`8000`)
- React Dashboard (`3000`)

---

## 20. Known Limitations

Documented in [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md):
- Operating expenses and competitor records were absent in the raw CSV folder and are generated via controlled synthetic seeds (`is_synthetic = TRUE`, seed `42`).
- Live BookingCenter PMS network integration is defined in `BookingCenterPMSAdapter` with calls mocked pending client production credentials.
- Financial transactions are audited and reconciled; irreversible fund transfers require authorized human sign-off in compliance with banking regulations.

---

## 21. Future Enhancements

- Live bi-directional webhook listeners for Apaleo and BookingCenter.
- Automated dispute filing via Booking.com Partner Hub APIs.
- European Open Banking (PSD2) live bank statement feeds for three-way cash matching.
- Authorized channel manager room price dispatch.

---

## 22. Troubleshooting

| Symptom | Cause | Solution |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'backend'` | Working directory not in Python path | Run tests using `.\venv\Scripts\pytest.exe -v tests\test_backend.py` (handled by `conftest.py`). |
| `Port 8000 in use` | Existing server process running | Terminate old uvicorn process or specify `--port 8001`. |
| `TypeError: ForwardRef.__init__() got unexpected keyword argument 'is_class'` | Pydantic 2.14 bug on Python 3.10.0 | Pinned to `pydantic>=2.10.0,<2.11.0` in `requirements.txt`. |
| `Cannot connect to Kafka / Qdrant` | Containers not running locally | System automatically runs in fallback mode (SQLite event ledger & local in-memory vector store). |

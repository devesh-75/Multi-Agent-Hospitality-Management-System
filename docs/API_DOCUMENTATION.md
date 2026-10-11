# REST API Documentation: Hospitality Fintech Agentic Layer

**Base URL:** `http://localhost:8000/api/v1`  
**OpenAPI Interactive Docs:** `http://localhost:8000/docs`  
**Protocol:** REST over HTTP / JSON  

---

## 1. System Health & Infrastructure

### `GET /health`
Verifies backend connectivity, database status, and streaming services.
- **Response:**
  ```json
  {
    "status": "healthy",
    "service": "Agentic Layer for Fintech Operations in Hospitality Services",
    "version": "1.0.0",
    "database": {
      "connected": true,
      "engine": "sqlite",
      "record_counts": {
        "properties": 5,
        "reservations": 100,
        "invoices": 300,
        "expenses": 92,
        "competitors": 12
      }
    },
    "kafka": { "enabled": false, "mode": "Development Mode (Database Event Queue)" },
    "qdrant": { "enabled": false, "mode": "Local In-Memory Vector Store" }
  }
  ```

---

## 2. Properties & Reservations

### `GET /properties`
Retrieves all synchronized properties.

### `GET /reservations`
- **Query Params:**
  - `property_id` (string, optional): Filter by property code (`BER`, `LND`, `MUC`, `PAR`, `VIE`).
  - `status` (string, optional): Filter by stay state (`InHouse`, `Confirmed`, `CheckedOut`).
  - `limit` (int, default: 50)
  - `offset` (int, default: 0)

---

## 3. Financial Analytics & Yield

### `GET /revenue`
Retrieves consolidated or property-filtered revenue metrics, ADR, RevPAR, and 14-day forecast.
- **Query Params:** `property_id` (optional)

### `GET /revenue/comparison`
Consolidated multi-property performance comparison matrix across all 5 properties.

### `GET /revenue/forecast`
- **Query Params:** `property_id` (optional), `horizon_days` (int, default: 14)

### `GET /occupancy`
Retrieves historical daily capacity utilization curves.

---

## 4. Invoices, Payments & Reconciliation

### `GET /invoices`
- **Query Params:** `property_id` (optional), `settled` (boolean, optional), `limit`, `offset`

### `GET /reconciliation`
Returns current financial reconciliation state: audited invoices, unbalanced receivables, duplicate payments, and OTA remittance discrepancy scenarios.

### `POST /reconciliation/run`
Explicitly invokes the Reconciliation Agent to recalculate matching ledgers and raise database alerts.

---

## 5. Operating Expenses

### `GET /expenses`
Returns departmental spending breakdown, categorical percentages, and statistical Z-score outliers.

### `POST /expenses/run`
Triggers the Expense Tracking Agent audit workflow.

---

## 6. Business Development & Competitor Intelligence (BDE)

### `GET /competitors`
List of cataloged competitors in the hotel's metropolitan market.

### `GET /competitor-comparison`
- **Query Params:** `property_id` (default: `BER`)
- Compares property ADR against competitor rates, distance, and star ratings.

### `GET /competitive-gaps`
- **Query Params:** `property_id` (default: `BER`)
- Identifies amenities offered by competitors that are absent or unconfirmed for the hotel.

### `GET /competitive-trends`
Historical price trend timeline across competing hotels.

### `GET /swot-analysis`
- **Query Params:** `property_id` (default: `BER`)
- Grounded SWOT analysis with empirical PMS citations.

### `GET /business-opportunities`
Evidence-based growth recommendations with expected business impact and human validation requirements.

### `POST /bde/ask`
Interactive natural-language query endpoint for strategic competitive intelligence.
- **Request Body:** `{"question": "Who are our main competitors?", "property_id": "BER"}`

---

## 7. Reports & Alerts

### `GET /reports`
Historical archives of formal operational reports.

### `POST /reports/generate`
- **Query Params:**
  - `report_type`: `CONSOLIDATED_EXECUTIVE`, `DAILY_OPERATIONS`, `REVENUE_ANALYSIS`, `RECONCILIATION_EXCEPTION`
  - `property_id` (optional)

### `GET /alerts`
List of unresolved operational and financial alerts.

### `POST /alerts/{alert_id}/resolve`
Acknowledges and resolves an alert.

---

## 8. Multi-Agent Orchestration & RAG

### `POST /agents/run`
Invokes the LangGraph StateGraph coordinator across all 5 specialized agents.
- **Request Body:** `{"query": "Run full operations audit"}`

### `POST /ask`
Natural-language question answering combining deterministic SQL execution with semantic RAG document retrieval.
- **Request Body:** `{"question": "What is our ADR and RevPAR in Berlin?", "property_id": "BER"}`

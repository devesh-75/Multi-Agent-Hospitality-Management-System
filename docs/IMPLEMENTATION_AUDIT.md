# Implementation Audit — Agentic Layer for Fintech Operations in Hospitality Services

> Generated: 2026-10-15 | Branch: `feature/functional-platform`

---

## Phase 1: Codebase Audit Checklist

### Known Issues (Confirmed by Reproduction)

| # | Bug | File | Status |
|---|-----|------|--------|
| 1 | `get_expense_breakdown()` returns `total_amount` in empty case, but `run_expense_audit()` reads `breakdown["total_expenses"]` → KeyError | `agents/expense_agent.py:35,170` | 🔴 Fix in Phase 2 |
| 2 | LangGraph workflow has fixed edges; single-agent runs all 5 agents; one failure kills entire chain | `agents/workflow.py:163-168` | 🔴 Fix in Phase 2 |
| 3 | `fetchData` silently swallows rejected promises; `handleRunAudit` uses `alert()` not toast | `dashboard/src/App.jsx:78-95,133` | 🔴 Fix in Phase 4 |
| 4 | Global exception handler hides error cause | `backend/app/main.py:62-68` | 🔴 Fix in Phase 2 |

### Feature Classification Matrix

#### Agents (5 specialized + workflow)

| Feature | Classification | Notes |
|---------|---------------|-------|
| ReconciliationAgent | ✅ Fully implemented | Real SQL queries, alert creation, AgentRun logging |
| ExpenseAgent | ⚠️ Partially implemented | Bug #1 (KeyError on empty), hardcoded narrative on line 161 |
| RevenueAgent | ✅ Fully implemented | Uses AnalyticsService, forecasting, recommendations |
| ReportingAgent | ✅ Fully implemented | Persists reports, generates markdown content |
| BDEAgent | ✅ Fully implemented | Competitor comparison, SWOT, feature gaps, ask_bde |
| LangGraph Workflow | ⚠️ Partially implemented / Broken | Bug #2: fixed edges, no conditional routing, no error handling |

#### API Endpoints (13 routers)

| Endpoint Group | Classification | Notes |
|----------------|---------------|-------|
| `/health` | ✅ Fully implemented | Returns DB status and record counts |
| `/properties` | ✅ Fully implemented | CRUD with Pydantic schema |
| `/reservations` | ✅ Fully implemented | Filterable, paginated |
| `/revenue` | ✅ Fully implemented | KPIs, comparison, forecast, time series |
| `/occupancy` | ✅ Fully implemented | Time series occupancy data |
| `/invoices` | ✅ Fully implemented | List, detail, payments list |
| `/reconciliation` | ✅ Fully implemented | GET and POST both trigger real agent |
| `/expenses` | ✅ Fully implemented | Analysis, list, run audit |
| `/competitors` + BDE | ✅ Fully implemented | Overview, comparison, gaps, trends, SWOT, opps, ask |
| `/reports` | ✅ Fully implemented | Generate and list persisted reports |
| `/alerts` | ✅ Fully implemented | List, resolve with persistence |
| `/agents` | ⚠️ Partially implemented | Run works but Bug #2 affects routing |
| `/ask` (RAG) | ✅ Fully implemented | Deterministic SQL + keyword routing, no LLM required |

#### Dashboard Views (12)

| View | Classification | Notes |
|------|---------------|-------|
| Executive Overview | ✅ Fully implemented | Connected to `/revenue` API |
| Properties | ✅ Fully implemented | Lists real properties |
| Reservations | ✅ Fully implemented | Real reservation data table |
| Revenue Analytics | ✅ Fully implemented | KPIs + charts from API |
| Invoices & Payments | ✅ Fully implemented | Real invoice/payment tables |
| Reconciliation | ✅ Fully implemented | Run button, summary cards, exceptions table |
| Expenses | ✅ Fully implemented | Category breakdown, anomalies, run audit |
| AI Agents | ✅ Fully implemented | Agent cards, run buttons, history |
| Business Development | ✅ Fully implemented | Competitors, SWOT, gaps, ask BDE |
| Reports | ✅ Fully implemented | Generate and view reports |
| Data Quality | ⚠️ UI-only / Mocked | Hardcoded counts, not querying real DB health |
| Ask AI | ✅ Fully implemented | Chat interface calling /ask endpoint |

#### Infrastructure

| Component | Classification | Notes |
|-----------|---------------|-------|
| Ingestion Pipeline | ✅ Fully implemented | Idempotent CSV→SQLite loading |
| SQLite Database | ✅ Fully implemented | Full ORM schema with relationships |
| Kafka Producer | ✅ Fully implemented | DB fallback when KAFKA_ENABLED=false |
| Kafka Consumer | ✅ Fully implemented | Event dispatch + DB polling mode |
| RAG/Vector Store | ✅ Fully implemented | In-memory TF-IDF vector store, no Qdrant needed |
| Docker Compose | ⚠️ Partially implemented | Config exists but not focus of this work |
| Tests | ⚠️ Partially implemented | Exist but need data loaded first; some assertions weak |

### Specific Issues Found in Codebase Scan

| Issue | Location | Severity |
|-------|----------|----------|
| Hardcoded maintenance narrative: "Emergency maintenance charges detected in September 2026" | `agents/expense_agent.py:161` | MEDIUM |
| `reporting_agent.py:153` has `hasattr` check on nonexistent `order_decay` attribute | `agents/reporting_agent.py:153` | LOW (no-op) |
| `bde_agent.py:381` references `opp['expected_impact']` but key is `expected_business_impact` | `agents/bde_agent.py:381` | MEDIUM |
| DataQualityView is entirely hardcoded with static counts | `dashboard/src/views/DataQualityView.jsx` | HIGH |
| No recharts dependency for charts (views reference chart components inline with CSS/divs) | `dashboard/package.json` | MEDIUM |
| Global error handler hides exception details | `backend/app/main.py:67` | HIGH |
| Dashboard `App.jsx` `fetchData` silently ignores rejected API calls | `dashboard/src/App.jsx:78-95` | HIGH |
| No light theme toggle | Dashboard CSS | LOW |
| Missing `__init__.py` in `agents/` and `kafka/` dirs (works due to sys.path manipulation) | Structural | LOW |
| `reservations.py:33` missing `HTTPException` import | `backend/app/api/endpoints/reservations.py` | MEDIUM |

---

## Verification Log

### Phase 1 Verification
- [x] Project inspected recursively
- [x] Git branch `feature/functional-platform` created
- [x] All 8 raw CSV data files present in `data/raw/`
- [x] Audit document created with prioritized checklist

*(Phases 2-5 verification logs will be appended below as work progresses)*

---

## Phase 2 Verification Log

*(To be filled after Phase 2 completion)*


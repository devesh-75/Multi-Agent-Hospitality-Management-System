# Testing & Quality Assurance Guide

## 1. Automated Testing Strategy

The test suite (`tests/test_backend.py`) verifies the entire pipeline from raw CSV ingestion to multi-agent LangGraph execution and REST API responses:

```
+----------------------------------------------------------------------------------+
|                            AUTOMATED TEST SUITE (pytest)                         |
+----------------------------------------------------------------------------------+
  [1] test_database_records_exist        -> Verifies 5 properties, 100+ reservations
  [2] test_analytics_kpis                -> Validates ADR, RevPAR, Occupancy bounds
  [3] test_property_comparison           -> Checks multi-property matrix (BER..VIE)
  [4] test_reconciliation_agent          -> Verifies fully/partially/unpaid & OTA cases
  [5] test_expense_agent_anomalies       -> Detects Z-Score >= 2.0 emergency repairs
  [6] test_revenue_agent                 -> Verifies yield decomposition & forecast
  [7] test_bde_agent_capabilities        -> Validates feature gaps, SWOT, growth opps
  [8] test_langgraph_workflow            -> Runs end-to-end multi-agent StateGraph
  [9] test_rag_query                     -> Tests hybrid SQL + Vector answer grounding
 [10] test_api_health                    -> Tests GET /health endpoint
 [11] test_api_properties                -> Tests GET /api/v1/properties
 [12] test_api_reconciliation            -> Tests GET /api/v1/reconciliation
 [13] test_api_bde_gaps                  -> Tests GET /api/v1/competitive-gaps
 [14] test_api_ask                       -> Tests POST /api/v1/ask query endpoint
```

---

## 2. Executing Automated Tests

To run the automated test suite locally:

```bash
# Using Python Virtual Environment
.\venv\Scripts\pytest.exe -v tests\test_backend.py
```

### Verified Test Run Output:
```text
tests/test_backend.py::test_database_records_exist PASSED                [  7%]
tests/test_backend.py::test_analytics_kpis PASSED                        [ 14%]
tests/test_backend.py::test_property_comparison PASSED                   [ 21%]
tests/test_backend.py::test_reconciliation_agent PASSED                  [ 28%]
tests/test_backend.py::test_expense_agent_anomalies PASSED               [ 35%]
tests/test_backend.py::test_revenue_agent PASSED                         [ 42%]
tests/test_backend.py::test_bde_agent_capabilities PASSED                [ 50%]
tests/test_backend.py::test_langgraph_workflow PASSED                    [ 57%]
tests/test_backend.py::test_rag_query PASSED                             [ 64%]
tests/test_backend.py::test_api_health PASSED                            [ 71%]
tests/test_backend.py::test_api_properties PASSED                        [ 78%]
tests/test_backend.py::test_api_reconciliation PASSED                    [ 85%]
tests/test_backend.py::test_api_bde_gaps PASSED                          [ 92%]
tests/test_backend.py::test_api_ask PASSED                               [100%]

======================= 14 passed in 1.62s =======================
```

---

## 3. Frontend Build Validation

To verify that the React dashboard compiles cleanly without syntax or bundling errors:

```bash
cd dashboard
npm run build
```

Output:
```text
✓ 1922 modules transformed.
dist/index.html                   0.45 kB
dist/assets/index-DSzpaCAg.css    3.38 kB
dist/assets/index-BsCHFGn7.js   316.48 kB
✓ built in 421ms
```

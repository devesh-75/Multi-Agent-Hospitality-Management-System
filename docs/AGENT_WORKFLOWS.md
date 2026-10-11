# Agent Workflows & LangGraph Orchestration

## 1. Overview & Orchestration Graph

The multi-agent framework is implemented using **LangGraph** (`langgraph.graph.StateGraph`), coordinating 5 specialized analytical agents into a deterministic, stateful workflow. Rather than using an unconstrained chatbot, each agent has a strictly bounded responsibility, direct access to repository services, and typed output contracts.

```
                  ┌────────────────────────┐
                  │    START WORKFLOW      │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │    Coordinator Node    │
                  └───────────┬────────────┘
                              │ (Conditional Routing)
        ┌─────────────────────┼─────────────────────┬──────────────────┐
        ▼                     ▼                     ▼                  ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐    ┌──────────────┐
│Reconciliation│      │Expense Agent │      │Revenue Agent │    │  BDE Agent   │
│    Agent     │      │  (Z-Scores)  │      │ (ADR/RevPAR) │    │(Competitors) │
└───────┬──────┘      └───────┬──────┘      └───────┬──────┘    └──────┬───────┘
        │                     │                     │                  │
        └─────────────────────┼─────────────────────┴──────────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Reporting Agent Node   │
                  │  (Executive Synthesis) │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Response Synthesizer   │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │      END WORKFLOW      │
                  └────────────────────────┘
```

---

## 2. Specialized Agent Profiles

### 2.1 Reconciliation Agent (`agents/reconciliation_agent.py`)
- **Objective:** Detect financial discrepancies across invoices, payment transactions, and OTA channel remittances.
- **Rules & Logic:**
  - `diff = total_invoice_gross - sum(payments)`
  - Classification: `FULLY_PAID` (`diff == 0.0`), `PARTIALLY_PAID` (`diff > 0.0`), `UNPAID` (`payments == 0`), `OVERPAID` (`diff < 0.0`).
  - OTA Payout Auditing: Compares contracted net remittance (`gross * (1 - commission_rate)`) against actual bank deposit received.
  - Detects duplicate payment candidates (identical reservation, identical date, identical amount).
  - Automatically raises actionable `RECONCILIATION_EXCEPTION` alerts in the database.

### 2.2 Expense Tracking Agent (`agents/expense_agent.py`)
- **Objective:** Audit operating expenditures, calculate departmental allocations, and flag statistical anomalies.
- **Anomaly Detection Formula:**
  $$\mu = \frac{1}{N} \sum_{i=1}^N x_i, \quad \sigma = \sqrt{\frac{1}{N} \sum_{i=1}^N (x_i - \mu)^2}$$
  $$Z = \frac{x - \mu}{\sigma}$$
  Charges with $Z \ge 2.0$ trigger an `EXPENSE_ANOMALY` alert (e.g., September chiller compressor emergency overhaul of €7,850.00).

### 2.3 Revenue Insight Agent (`agents/revenue_agent.py`)
- **Objective:** Deconstruct revenue performance and calculate empirical hospitality yield metrics:
  - $\text{Occupancy Rate} = \frac{\text{Total Occupied Room Nights}}{\text{Total Available Room Nights}} \times 100$
  - $\text{Average Daily Rate (ADR)} = \frac{\text{Total Room Revenue}}{\text{Occupied Room Nights}}$
  - $\text{RevPAR} = \frac{\text{Total Room Revenue}}{\text{Total Available Room Nights}} = \text{ADR} \times \text{Occupancy Rate}$
- **Forecasting:** Evaluates 14-day forward projections using a 5-day rolling average with polynomial linear drift and weekend demand seasonality weighting.

### 2.4 Reporting Agent (`agents/reporting_agent.py`)
- **Objective:** Formulate consistent executive summaries, daily operational logs, and exception briefs.
- **Report Types:** `DAILY_OPERATIONS`, `REVENUE_ANALYSIS`, `RECONCILIATION_EXCEPTION`, `CONSOLIDATED_EXECUTIVE`.
- Reports are persisted to the `reports` database table for historical auditing.

### 2.5 Business Development Executive (BDE) Agent (`agents/bde_agent.py`)
- **Objective:** Synthesize internal PMS metrics with market competitive benchmarks to drive strategic expansion.
- **Core Functions:**
  1. Competitor rate and distance benchmarking.
  2. Competitive amenity feature-gap analysis.
  3. Grounded SWOT analysis with verified empirical citations.
  4. Business growth recommendations with mandatory human validation safeguards.

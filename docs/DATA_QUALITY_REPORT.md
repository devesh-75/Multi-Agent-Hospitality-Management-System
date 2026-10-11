# Data Quality Report: Source Dataset Audit & Anomaly Assessment

**Project:** Agentic Layer for Fintech Operations in Hospitality Services  
**Source Directory:** `C:\Users\deves\Downloads\project`  
**Evaluation Standard:** DAMA-DMBOK Data Quality Dimensions  
**Date of Audit:** October 2026  

---

## 1. Executive Summary

A comprehensive automated data quality audit was conducted on all 8 source CSV files located at `C:\Users\deves\Downloads\project`. 

The source datasets provide a solid and authentic foundation of PMS operations and structured reconciliation test scenarios. Key operational entities (properties, rooms, rate plans, guest profiles, reservations, folios, invoices, charges) demonstrate high schema consistency and referential validity across the 5 European property domains (`BER`, `LND`, `MUC`, `PAR`, `VIE`). 

However, critical data quality gaps, intentional test discrepancies, and absent business domains were identified and are documented below.

---

## 2. Quantitative Quality Dimension Analysis

### 2.1 Completeness Audit

| Dataset | Total Rows | Total Columns | Total Cells | Null Cells | Completeness Rate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `properties.csv` | 5 | 11 | 55 | 5 (`updated_at`) | **90.91%** |
| `reservations.csv` | 100 | 25 | 2,500 | 400 (4 unused optional cols) | **84.00%** |
| `folios.csv` | 205 | 21 | 4,305 | 925 (charges, payments, AR) | **78.51%** |
| `invoices.csv` | 200 | 23 | 4,600 | 0 | **100.00%** |
| `charges_full.csv` | 200 | 13 | 2,600 | 0 | **100.00%** |
| `payments_full.csv` | 100 | 11 | 1,100 | 0 | **100.00%** |
| `synthetic_invoices_full.csv` | 100 | 9 | 900 | 0 | **100.00%** |
| `ota_reservations_full.csv` | 20 | 19 | 380 | 8 (4 missing settlement payouts) | **97.89%** |
| **Aggregated Total** | **1,030** | **132** | **16,440** | **1,338** | **91.86%** |

---

### 2.2 Detailed Null & Sparsity Analysis

1. **`reservations.csv`:**
   - `block_id`: 100 nulls (100%). All reservations are individual bookings rather than group blocks.
   - `children_ages`: 100 nulls (100%). No children registered in this sample.
   - `external_code`: 100 nulls (100%). Channel distribution is listed as `Direct`, so no external GDS/OTA locator code was assigned.
   - `validation_messages`: 100 nulls (100%). PMS rules passed without constraint warnings.
2. **`folios.csv`:**
   - `reservation_id`: 105 nulls (51.2%). As designed in hospitality PMS architectures, 100 folios are group booking master folios (`type = Booking`) and 5 are property house accounts (`HOUSE-BER`, `HOUSE-LND`, etc.), which do not have individual guest reservation IDs.
   - `company_data`, `charges`, `payments`: 205 nulls (100%). Charges and payments are recorded in separate transaction ledgers rather than embedded in the folio master record.
   - `closing_date`: 205 nulls (100%). All folios are currently in active `Open` or standard lifecycle states.
3. **`ota_reservations_full.csv`:**
   - `actual_settlement` & `settlement_date`: 4 nulls (20%). Represents the `missing_settlement` audit test scenario where the OTA failed to remit funds for booked stays.

---

## 3. Consistency & Referential Integrity Findings

### 3.1 Property Referential Integrity: **100% Valid**
All foreign keys referencing properties across all 8 datasets strictly belong to the set of 5 canonical properties:
- `BER` (Hotel Berlin, Germany)
- `LND` (Hotel London, United Kingdom)
- `MUC` (Hotel Munich, Germany)
- `PAR` (Hotel Paris, France)
- `VIE` (Hotel Vienna, Austria)

### 3.2 Dual-Cohort Reservation Linkage
The audit revealed two distinct reservation cohorts in the data:
1. **PMS Operational Cohort:** 
   - `reservations.csv` (100 reservations, e.g., `LNIGSXXC-98-1`)
   - `invoices.csv` (200 invoices, 100% matched to `reservations.csv`)
   - `folios.csv` (200 folios, 100% matched to `reservations.csv` via reservation or booking ID)
2. **Fintech Audit & Reconciliation Cohort:**
   - `synthetic_invoices_full.csv` (100 invoices, e.g., `SYN-QHMMYUKY-1`)
   - `charges_full.csv` (200 charges, 100% matched to `synthetic_invoices_full.csv`)
   - `payments_full.csv` (100 payments, 100% matched to `synthetic_invoices_full.csv`)
   - `ota_reservations_full.csv` (20 bookings with specific reconciliation scenarios)

**Resolution:** The ingestion engine handles both cohorts seamlessly. In the unified database, all records link into the common property and reservation tables, preserving provenance tags (`is_synthetic` flag).

---

## 4. Controlled Discrepancy & Reconciliation Anomaly Catalog

The dataset contains intentional financial discrepancy scenarios designed to rigorously test the AI agents:

### 4.1 Payment vs. Invoice Discrepancies (`payments_full.csv` vs `synthetic_invoices_full.csv`)
- **Exact Settlements (25 records):** `diff = 0.00`. Payment matches invoice total exactly.
- **Minor Fee Underpayment (25 records):** `diff = 10.00`. Exactly €10.00 / £10.00 underpaid (e.g., unpaid resort/city fee or unbilled minibar charge).
- **Substantial Underpayments (50 records):** `diff > 50.00` (e.g., €50.50, €76.00, €96.00, €117.70). Customer paid a 50% deposit or partial installment, leaving an outstanding accounts receivable balance.

### 4.2 OTA Remittance Anomalies (`ota_reservations_full.csv`)
- **`exact` (4 records):** Expected net payout equals bank remittance received.
- **`underpayment` (4 records):** OTA withheld more funds than contracted (e.g., €10.00 - €20.00 variance).
- **`overpayment` (4 records):** OTA remitted more than expected due to adjustments.
- **`missing_settlement` (4 records):** Payout status `MISSING`, remittance date null, funds not received.
- **`commission_discrepancy` (4 records):** Applied commission deviates from contracted tier (e.g., 18% applied instead of 15%).

---

## 5. Missing Business Entities & Remediation Policy

The raw dataset lacks:
1. **Departmental Expenses:** Required by the Expense Tracking Agent.
2. **Competitor Intelligence & Market Benchmarks:** Required by the Business Development Executive (BDE) Agent.

**Policy:**
- As required by the project specifications, synthetic records will be generated with a deterministic fixed seed (`42`).
- All synthetic records will carry `is_synthetic = TRUE` and `source_type = 'synthetic_seed'`.
- The frontend and reporting agents will explicitly label and visually distinguish real PMS records from synthetic benchmarks.

# Data Inventory: Hospitality Fintech Agentic Layer

**Date of Inspection:** October 2026  
**Source Directory:** `C:\Users\deves\Downloads\project`  
**Inspected By:** Technical Lead & Data Architecture Agent  
**Environment:** Windows, Python 3.10, PostgreSQL Unified Target Model  

---

## 1. Executive Summary

A comprehensive, non-destructive automated inspection was conducted on the source data directory `C:\Users\deves\Downloads\project`. 

The directory contains **8 primary CSV datasets** totaling **407.3 KB** across **1,030 total records**. No subdirectories, Excel files, JSON dumps, Parquet archives, or SQL scripts were present in the source root.

The source files represent a dual-layer hospitality architecture:
1. **Authoritative PMS Core Datasets (Apaleo Open-PMS format):** 
   - `properties.csv` (5 properties)
   - `reservations.csv` (100 reservations with rich embedded JSON entities)
   - `folios.csv` (205 folios including master booking folios and house accounts)
   - `invoices.csv` (200 finalized guest invoices)
2. **Specialized Financial & Reconciliation Datasets:**
   - `charges_full.csv` (200 itemized guest charges with tax breakdown)
   - `payments_full.csv` (100 payment transactions with settlement references)
   - `synthetic_invoices_full.csv` (100 benchmark invoices mapped to charges & payments)
   - `ota_reservations_full.csv` (20 OTA channel bookings with controlled audit scenarios)

---

## 2. File Inventory Matrix

| Filename | File Size | Row Count | Column Count | Primary Domain | Data Provenance | Primary Key / Natural Key |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `properties.csv` | 673 B | 5 | 11 | Property Master | Real PMS Export | `id` (`BER`, `LND`, `MUC`, `PAR`, `VIE`) |
| `reservations.csv` | 95.2 KB | 100 | 25 | PMS Reservations | Real PMS Export | `id` (e.g., `LNIGSXXC-98-1`) |
| `folios.csv` | 90.8 KB | 205 | 21 | Billing Folios | Real PMS Export | `id` (e.g., `LNIGSXXC-98-1-1`, `*-BOOK`) |
| `invoices.csv` | 160.6 KB | 200 | 23 | Invoices & Line Items | Real PMS Export | `id` (e.g., `LNIGSXXC-98-1-INV-1`) |
| `charges_full.csv` | 24.8 KB | 200 | 13 | Itemized Charges | Synthetic Test Suite | `id` |
| `payments_full.csv` | 12.1 KB | 100 | 11 | Payment Transactions | Synthetic Test Suite | `id` (e.g., `*-payment`) |
| `synthetic_invoices_full.csv` | 9.6 KB | 100 | 9 | Invoice Reconciliation | Synthetic Test Suite | `id` (e.g., `*-invoice`) |
| `ota_reservations_full.csv` | 3.6 KB | 20 | 19 | OTA Channel Settlements | Synthetic Audit Suite | `id` (e.g., `ota-*-1`) |

---

## 3. Detailed Dataset Breakdown

### 3.1 `properties.csv`
- **Description:** Multi-property master records for 5 European city hotels.
- **Properties:**
  1. `BER`: Hotel Berlin GmbH (Berlin, Germany | EUR | `Europe/Berlin`)
  2. `LND`: London Calling Ltd. (London, United Kingdom | GBP | `Europe/London`)
  3. `MUC`: Hotel Munich (Munich, Germany | EUR | `Europe/Berlin`)
  4. `PAR`: Hotel Paris (Paris, France | EUR | `Europe/Paris`)
  5. `VIE`: Hotel Vienna (Vienna, Austria | EUR | `Europe/Vienna`)
- **Key Fields:** `id`, `code`, `company_name`, `name` (JSON i18n), `country_code`, `timezone`, `created_at`.

### 3.2 `reservations.csv`
- **Description:** Complete guest reservation lifecycle records across the 5 properties.
- **Status Breakdown:** `InHouse` (36), `CheckedOut` (32), `Confirmed` (32).
- **Date Horizon:** Arrivals from `2026-08-11` to `2026-10-08`.
- **Financial Volume:** Total gross reservation volume: €34,238.80 (Range: €112.40 - €980.36 per booking).
- **Embedded JSON Sub-Entities:**
  - `unit_data`: 99 unique guest rooms (e.g., Room `2.207`, `1.221`).
  - `unit_group_data`: 5 distinct room types (`DBL`, `SGL`, etc.).
  - `primary_guest`: 91 unique guest profiles with contact details, email addresses, and home addresses.
  - `rate_plan_data`: 5 rate plans (e.g., `Include breakfast`, standard).

### 3.3 `folios.csv`
- **Description:** PMS Guest folios and billing accounts.
- **Folio Classification:**
  - 100 Guest Folios linked directly to individual reservations.
  - 100 Master Booking Folios linked to `booking_id` with type `Booking`.
  - 5 House Account Folios (`HOUSE-BER`, `HOUSE-LND`, `HOUSE-MUC`, `HOUSE-PAR`, `HOUSE-VIE`) for internal property postings.
- **Quality Observation:** The raw `charges` and `payments` columns in this export are empty arrays/NaN, as charges and payments are maintained in dedicated financial ledgers.

### 3.4 `invoices.csv`
- **Description:** Official PMS tax invoices generated upon checkout or interim stay billing.
- **Status & Type:** 200 invoices, all status `ISSUED` and type `STAY`.
- **Settlement Status in PMS:** 92 marked `payment_settled = True`, 108 marked `payment_settled = False`.
- **Line Items:** Contains complete JSON array of invoice line items, room nights, and city tax lines. Total invoice sum: €34,238.80.

### 3.5 `charges_full.csv`
- **Description:** Granular guest charge postings across all 5 properties.
- **Categories:** `ROOM` (100 charges), `BREAKFAST` (25 charges), `RESTAURANT` (25 charges), `MINIBAR` (25 charges), `PARKING` (25 charges).
- **Currencies:** EUR (146 charges), GBP (54 charges).
- **Integrity Validation:** When summed by reservation, charges match corresponding invoice totals exactly to the cent.

### 3.6 `payments_full.csv`
- **Description:** Financial payment records for front-desk settlement testing.
- **Payment Methods:** `CREDIT_CARD` (34), `BANK_TRANSFER` (33), `CASH` (33).
- **Recorded Statuses:** `PARTIALLY_PAID` (75), `FULLY_PAID` (25).
- **Reconciliation Scope:** Contains controlled variances (partial payments, underpayments, unpaid balances) designed for automated reconciliation engine auditing.

### 3.7 `synthetic_invoices_full.csv`
- **Description:** Matched invoice baseline records for the reconciliation testing suite.
- **Linkage:** 100% matched against `payments_full.csv` and `charges_full.csv`.

### 3.8 `ota_reservations_full.csv`
- **Description:** Online Travel Agency (OTA) bookings and settlement audit data.
- **OTA Channels:** Booking.com (8), Expedia (4), Agoda (4), Airbnb (4).
- **Reconciliation Test Scenarios:**
  - `exact` (4 bookings): Expected settlement matches actual settlement exactly.
  - `underpayment` (4 bookings): OTA settled less than contracted net payout.
  - `overpayment` (4 bookings): OTA settled more than expected.
  - `missing_settlement` (4 bookings): Status `MISSING`, no payout received.
  - `commission_discrepancy` (4 bookings): Commission rate applied incorrectly by channel.

---

## 4. Missing Business Entities Identified

The source directory does **NOT** contain files for the following business entities required for the comprehensive fintech and BDE system:

1. **Operational Expenses:** Hotel departmental operating expenses (Payroll, Utilities, Food & Beverage Supplies, Linen & Laundry, Software/SaaS, Maintenance, Property Insurance, Marketing).
2. **Competitor Intelligence & BDE Data:** Competitor property names, star ratings, competitor room prices, amenity comparisons, review sentiment scores, and historical competitor rate snapshots.
3. **Housekeeping Task Logs:** Front-desk room turnover, inspection statuses, and task durations.

### Handling Strategy:
- **Zero Silent Fabrication:** In accordance with Section 2 of the project specification, missing entities are documented explicitly.
- **Controlled Seed Generation:** A deterministic, reproducible synthetic generator (`scripts/seed_missing_entities.py`) with a fixed seed will generate operational expenses and competitor records.
- **Explicit Provenance:** All generated records will be tagged with `is_synthetic = TRUE` and `source_type = 'synthetic_seed'` in the database and visually marked in the UI.

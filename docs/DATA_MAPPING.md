# Data Mapping Specification: Source CSVs to Unified PostgreSQL Schema

**Project:** Agentic Layer for Fintech Operations in Hospitality Services  
**Source Directory:** `C:\Users\deves\Downloads\project`  
**Target Storage Engine:** PostgreSQL 15+ / SQLite compatible fallback  

---

## 1. Architectural Overview & Normalization Strategy

The source datasets consist of raw PMS exports containing denormalized and nested JSON structures alongside specialized financial audit files. To power multi-agent workflows, SQL analytics, and vector search, data is ingested into a **Third Normal Form (3NF) relational database** with strict foreign-key constraints.

```
+---------------------------------------------------------------------------------+
|                              RAW CSV INGESTION LAYER                            |
| properties.csv  reservations.csv  folios.csv  invoices.csv  charges_full.csv    |
| payments_full.csv  synthetic_invoices_full.csv  ota_reservations_full.csv       |
+---------------------------------------------------------------------------------+
                                       │
                                       ▼
+---------------------------------------------------------------------------------+
|                        NORMALIZATION & EXTRACTION ENGINE                        |
|  - JSON Extraction: primary_guest -> guests, unit_data -> rooms, etc.           |
|  - Timestamp Normalization: ISO-8601 with timezone offsets to UTC TIMESTAMPTZ  |
|  - Currency & Decimal Precision: NUMERIC(12,2) with ISO-4217 currency codes     |
|  - Lineage & Provenance Tracking: source_file, source_type, is_synthetic        |
+---------------------------------------------------------------------------------+
                                       │
                                       ▼
+---------------------------------------------------------------------------------+
|                             UNIFIED DATABASE MODEL                              |
|  Core PMS: properties, rooms, room_types, guests, rate_plans, reservations      |
|  Accounting: folios, invoices, invoice_items, charges, payments                 |
|  Distribution: ota_channels, ota_bookings, ota_settlements                      |
|  Fintech Operations: expenses (synthetic seed), expense_categories             |
|  Competitor Intelligence: competitors, competitor_properties,                   |
|                           competitor_features, competitor_prices,               |
|                           competitor_reviews, competitor_snapshots              |
|  Agent Orchestration: business_events, agent_runs, alerts, reports              |
+---------------------------------------------------------------------------------+
```

---

## 2. Table-by-Table Mapping Specifications

### 2.1 Table: `properties`
*Source: `properties.csv`*

| Source Column | Target Column | Data Type | Transformation / Logic |
| :--- | :--- | :--- | :--- |
| `id` | `id` | `VARCHAR(16) PK` | Direct mapping (`BER`, `LND`, `MUC`, `PAR`, `VIE`) |
| `code` | `code` | `VARCHAR(16)` | Direct mapping |
| `company_name` | `company_name` | `VARCHAR(255)` | Direct mapping |
| `name` | `name` | `VARCHAR(255)` | Parse JSON `{"en": "Hotel Berlin"}` -> `'Hotel Berlin'` |
| `status` | `status` | `VARCHAR(32)` | Direct mapping |
| `country_code` | `country_code` | `VARCHAR(2)` | Direct mapping (`DE`, `GB`, `FR`, `AT`) |
| `timezone` | `timezone` | `VARCHAR(64)` | Direct mapping |
| Derived | `currency` | `VARCHAR(3)` | Default by country: GB -> `'GBP'`, DE/FR/AT -> `'EUR'` |
| `created_at` | `created_at` | `TIMESTAMPTZ` | Parse ISO-8601 to UTC |
| N/A | `is_synthetic` | `BOOLEAN` | `FALSE` (real PMS export) |
| N/A | `source_file` | `VARCHAR(64)` | `'properties.csv'` |

---

### 2.2 Table: `rooms` & `room_types`
*Source: Extracted from nested JSON in `reservations.csv`*

**`room_types` extraction from `reservations.csv -> unit_group_data`:**
- `id` -> `id` (e.g., `BER-DBL`)
- `code` -> `code` (`DBL`)
- `name` -> `name` (`Double`)
- `property_id` -> Extracted from prefix or reservation record
- `type` -> `category` (`BedRoom`)

**`rooms` extraction from `reservations.csv -> unit_data`:**
- `id` -> `id` (e.g., `BER-ROOM987`)
- `name` -> `room_number` (`2.207`)
- `description` -> `description` (`Room 910`)
- `unitGroupId` -> `room_type_id` (`BER-DBL`)
- `property_id` -> FK to `properties`

---

### 2.3 Table: `guests`
*Source: Extracted from nested JSON in `reservations.csv -> primary_guest`*

| JSON Field | Target Column | Data Type | Transformation / Logic |
| :--- | :--- | :--- | :--- |
| Composite | `id` | `VARCHAR(64) PK` | MD5 hash of `email` or synthetic sequence `GST-001` |
| `firstName` | `first_name` | `VARCHAR(128)` | Direct mapping |
| `lastName` | `last_name` | `VARCHAR(128)` | Direct mapping |
| `email` | `email` | `VARCHAR(255)` | Unique identifier for guest entity deduplication |
| `phone` | `phone` | `VARCHAR(64)` | E.164 phone string |
| `address.addressLine1`| `address` | `VARCHAR(255)` | Street address |
| `address.postalCode` | `postal_code` | `VARCHAR(32)` | Postal code |
| `address.city` | `city` | `VARCHAR(128)` | City name |
| `address.countryCode` | `country_code` | `VARCHAR(2)` | Country code |

---

### 2.4 Table: `reservations`
*Source: `reservations.csv`*

| Source Column | Target Column | Data Type | Transformation / Logic |
| :--- | :--- | :--- | :--- |
| `id` | `id` | `VARCHAR(64) PK` | Direct mapping (`LNIGSXXC-98-1`) |
| `booking_id` | `booking_id` | `VARCHAR(32)` | Direct mapping (`LNIGSXXC`) |
| `property_id` | `property_id` | `VARCHAR(16) FK` | References `properties(id)` |
| `unit_data.id` | `room_id` | `VARCHAR(64) FK` | References `rooms(id)` |
| `unit_group_data.id`| `room_type_id` | `VARCHAR(64) FK`| References `room_types(id)` |
| `primary_guest.email`| `guest_id` | `VARCHAR(64) FK` | References `guests(id)` |
| `status` | `status` | `VARCHAR(32)` | Direct mapping (`InHouse`, `CheckedOut`, `Confirmed`) |
| `arrival` | `arrival_date` | `TIMESTAMPTZ` | Parse ISO-8601 to UTC |
| `departure` | `departure_date` | `TIMESTAMPTZ` | Parse ISO-8601 to UTC |
| `adults` | `adults` | `INTEGER` | Integer count |
| `channel_code` | `channel_code` | `VARCHAR(32)` | Direct mapping (`Direct`) |
| `total_gross_amount` | `total_gross_amount`| `NUMERIC(12,2)` | Monetary value |
| `balance` | `balance` | `NUMERIC(12,2)` | Outstanding guest balance |
| `guarantee_type` | `guarantee_type` | `VARCHAR(32)` | Guarantee method |
| `created_at` | `created_at` | `TIMESTAMPTZ` | Booking creation timestamp |
| N/A | `is_synthetic` | `BOOLEAN` | `FALSE` |
| N/A | `source_file` | `VARCHAR(64)` | `'reservations.csv'` |

---

### 2.5 Table: `invoices` & `invoice_items`
*Sources: `invoices.csv` (Real PMS) & `synthetic_invoices_full.csv` (Reconciliation Test Suite)*

| Source Column | Target Column | Data Type | Transformation / Logic |
| :--- | :--- | :--- | :--- |
| `id` | `id` | `VARCHAR(64) PK` | Direct mapping |
| `invoice_number` | `invoice_number` | `VARCHAR(64)` | Tax invoice number |
| `property_id` | `property_id` | `VARCHAR(16) FK` | References `properties(id)` |
| `reservation_id` | `reservation_id` | `VARCHAR(64)` | Associated reservation reference |
| `folio_id` | `folio_id` | `VARCHAR(64)` | Associated folio reference |
| `status` | `status` | `VARCHAR(32)` | `'ISSUED'` |
| `total` | `total_amount` | `NUMERIC(12,2)` | Invoice gross total |
| `outstanding_payment` | `outstanding_balance`| `NUMERIC(12,2)` | Unsettled receivable |
| `invoice_date` | `invoice_date` | `DATE` | Fiscal tax date |
| `due_to` | `due_date` | `DATE` | Payment maturity date |
| `data_source` / provenance | `is_synthetic` | `BOOLEAN` | `TRUE` if from `synthetic_invoices_full.csv`, else `FALSE` |

*Invoice Line Items are parsed from `invoices.csv -> line_items` JSON array and inserted into `invoice_items` (`invoice_id`, `description`, `quantity`, `unit_price`, `amount`).*

---

### 2.6 Table: `payments`
*Source: `payments_full.csv`*

| Source Column | Target Column | Data Type | Transformation / Logic |
| :--- | :--- | :--- | :--- |
| `id` | `id` | `VARCHAR(64) PK` | Direct mapping |
| `reservation_id` | `reservation_id` | `VARCHAR(64)` | Linked reservation ID |
| `folio_id` | `folio_id` | `VARCHAR(64)` | Linked folio ID |
| `property_id` | `property_id` | `VARCHAR(16) FK` | References `properties(id)` |
| `payment_method` | `payment_method` | `VARCHAR(32)` | `CREDIT_CARD`, `BANK_TRANSFER`, `CASH` |
| `amount` | `amount` | `NUMERIC(12,2)` | Monetary value |
| `currency` | `currency` | `VARCHAR(3)` | `EUR`, `GBP` |
| `payment_date` | `payment_date` | `DATE` | Payment posting date |
| `transaction_reference`| `transaction_reference`| `VARCHAR(64)` | Gateway / authorization reference |
| `status` | `status` | `VARCHAR(32)` | `PARTIALLY_PAID`, `FULLY_PAID` |
| `data_source` | `is_synthetic` | `BOOLEAN` | `TRUE` |

---

### 2.7 Table: `ota_settlements`
*Source: `ota_reservations_full.csv`*

| Source Column | Target Column | Data Type | Transformation / Logic |
| :--- | :--- | :--- | :--- |
| `id` | `id` | `VARCHAR(64) PK` | Direct mapping |
| `ota_name` | `channel_name` | `VARCHAR(64)` | Channel name |
| `ota_reservation_id` | `ota_reservation_id` | `VARCHAR(64)` | External OTA booking ID |
| `pms_reservation_id` | `reservation_id` | `VARCHAR(64)` | Internal reservation ID |
| `property_id` | `property_id` | `VARCHAR(16) FK` | References `properties(id)` |
| `gross_amount` | `gross_amount` | `NUMERIC(12,2)` | Gross reservation charge |
| `commission_rate` | `commission_rate` | `NUMERIC(5,4)` | Commission rate |
| `commission_amount` | `commission_amount` | `NUMERIC(12,2)` | Commission deducted |
| `expected_settlement`| `expected_settlement`| `NUMERIC(12,2)` | Contracted net remittance |
| `actual_settlement` | `actual_settlement` | `NUMERIC(12,2)` | Actual payout received |
| `settlement_date` | `settlement_date` | `DATE` | Bank credit date |
| `reconciliation_scenario`| `audit_scenario` | `VARCHAR(64)` | Scenario category |
| `status` | `status` | `VARCHAR(32)` | `SETTLED` or `MISSING` |
| `data_source` | `is_synthetic` | `BOOLEAN` | `TRUE` |

---

## 3. Missing Business Entities: Target Models & Synthetic Seed Design

To power the Expense Tracking Agent and BDE / Competitive Intelligence Agent without silent fabrication, the following schemas are added and populated via a reproducible generator with fixed seed `42`:

### 3.1 `expenses` (Departmental Operational Expenses)
- `id` (PK, e.g., `EXP-BER-2026-001`)
- `property_id` (FK to `properties`)
- `category` (`Payroll`, `Utilities`, `F&B Supplies`, `Linen & Laundry`, `SaaS & PMS`, `Maintenance`, `Marketing`)
- `vendor_name` (e.g., `Berliner Stadtwerke`, `CleanLinen Solutions GmbH`)
- `amount` (`NUMERIC(12,2)`)
- `currency` (`EUR` / `GBP`)
- `expense_date` (`DATE`)
- `status` (`APPROVED`, `PAID`, `PENDING_REVIEW`)
- `is_synthetic` (`TRUE`)
- `source_type` (`'synthetic_seed'`)

### 3.2 Competitor Intelligence Schema (`competitors`, `competitor_properties`, `competitor_features`, `competitor_prices`, `competitor_reviews`)
- **`competitors`**: Competitor brand/chain master (e.g., `CitizenM Berlin`, `The Hoxton London`, `Motel One Munich`, `Mama Shelter Paris`, `25hours Vienna`).
- **`competitor_properties`**: Property details, address, star rating, total room count.
- **`competitor_features`**: Amenity catalog with confirmation status (`Confirmed Available`, `Confirmed Unavailable`, `Unknown`) for feature-gap analysis (e.g., `Rooftop Bar`, `Co-Working Space`, `Digital Keycard`, `Free High-Speed WiFi`, `EV Charging`).
- **`competitor_prices`**: Historical daily room price snapshots across room types.
- **`competitor_reviews`**: Aggregated review ratings, sentiment breakdown, and review counts.
- **All competitor records are tagged with `is_synthetic = TRUE` and displayed with clear synthetic disclaimer tags in the UI.**

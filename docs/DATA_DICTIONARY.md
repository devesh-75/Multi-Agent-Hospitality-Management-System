# Data Dictionary: Source Datasets & Normalized Schema

**Project:** Agentic Layer for Fintech Operations in Hospitality Services  
**Source Directory:** `C:\Users\deves\Downloads\project`  

---

## 1. `properties.csv` (Property Master)

| Column Name | Source Type | Target SQL Type | Nullable | Unique | Sample Value | Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | string | `VARCHAR(16) PRIMARY KEY` | No | 5 | `BER`, `LND`, `MUC` | Unique property identifier code |
| `external_id` | string | `VARCHAR(64)` | No | 5 | `BER` | External system PMS reference code |
| `code` | string | `VARCHAR(16)` | No | 5 | `BER` | Property operational code |
| `company_name` | string | `VARCHAR(255)` | No | 5 | `Hotel Berlin GmbH` | Legal operating corporate entity name |
| `name` | string (JSON) | `JSONB` / `VARCHAR(255)` | No | 5 | `{"en": "Hotel Berlin"}` | Multilingual hotel commercial name |
| `status` | string | `VARCHAR(32)` | No | 1 | `Test` | Operational status of the property |
| `is_archived` | bool | `BOOLEAN` | No | 1 | `False` | Soft deletion archive flag |
| `country_code` | string | `VARCHAR(2)` | No | 4 | `DE`, `GB`, `FR`, `AT` | ISO 3166-1 alpha-2 country code |
| `timezone` | string | `VARCHAR(64)` | No | 3 | `Europe/Berlin` | IANA timezone identifier |
| `created_at` | string (ISO) | `TIMESTAMPTZ` | No | 1 | `2026-08-10T17:03:11+02:00` | Property creation timestamp |
| `updated_at` | float64 | `TIMESTAMPTZ` | Yes | 0 | `NULL` | Last update timestamp (all null in source) |

---

## 2. `reservations.csv` (Guest Reservations)

| Column Name | Source Type | Target SQL Type | Nullable | Unique | Sample Value | Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | string | `VARCHAR(64) PRIMARY KEY` | No | 100 | `LNIGSXXC-98-1` | Unique PMS reservation record ID |
| `external_id` | string | `VARCHAR(64)` | No | 100 | `LNIGSXXC-98-1` | External PMS reservation identifier |
| `booking_id` | string | `VARCHAR(32)` | No | 100 | `LNIGSXXC` | Group / Master booking identifier |
| `property_id` | string | `VARCHAR(16) REFERENCES properties(id)` | No | 5 | `BER`, `LND`, `PAR` | Foreign key to property |
| `block_id` | float64 | `VARCHAR(64)` | Yes (100%) | 0 | `NULL` | Room block group ID if group booking |
| `status` | string | `VARCHAR(32)` | No | 3 | `InHouse`, `CheckedOut`, `Confirmed` | Lifecycle status of the stay |
| `arrival` | string (ISO) | `TIMESTAMPTZ` | No | 52 | `2026-09-17T00:00:00+02:00` | Scheduled / actual arrival timestamp |
| `departure` | string (ISO) | `TIMESTAMPTZ` | No | 53 | `2026-09-19T00:00:00+02:00` | Scheduled / actual departure timestamp |
| `created_at` | string (ISO) | `TIMESTAMPTZ` | No | 98 | `2026-08-10T17:04:37+02:00` | Reservation booking creation time |
| `modified_at` | string (ISO) | `TIMESTAMPTZ` | No | 52 | `2026-09-19T00:00:00+02:00` | Last state transition timestamp |
| `adults` | int64 | `INTEGER` | No | 2 | `1`, `2` | Number of adult occupants |
| `children_ages` | float64 | `JSONB` / `INTEGER[]` | Yes (100%) | 0 | `NULL` | Ages of accompanying children |
| `channel_code` | string | `VARCHAR(32)` | No | 1 | `Direct` | Distribution booking channel |
| `external_code` | float64 | `VARCHAR(64)` | Yes (100%) | 0 | `NULL` | Channel manager external reference |
| `balance` | float64 | `NUMERIC(12,2)` | No | 66 | `-253.40`, `0.00` | Outstanding guest ledger balance |
| `total_gross_amount` | float64 | `NUMERIC(12,2)` | No | 67 | `253.40`, `130.59` | Total contracted stay amount incl. tax |
| `guarantee_type` | string | `VARCHAR(32)` | No | 3 | `CreditCard`, `Prepayment`, `Company` | Payment guarantee method |
| `has_city_tax` | bool | `BOOLEAN` | No | 2 | `False`, `True` | Indicator if local municipal tax applies |
| `is_open_for_charges` | bool | `BOOLEAN` | No | 1 | `True` | Flag indicating if folio accepts charges |
| `property_data` | JSON string | `JSONB` | No | 5 | `{"id": "BER", ...}` | Embedded property snapshot |
| `rate_plan_data` | JSON string | `JSONB` | No | 5 | `{"id": "BER-IBRKF-DBL", ...}` | Rate plan details (pricing model) |
| `unit_group_data` | JSON string | `JSONB` | No | 5 | `{"id": "BER-DBL", ...}` | Room category (Single, Double, Suite) |
| `unit_data` | JSON string | `JSONB` | No | 99 | `{"id": "BER-ROOM987", ...}` | Assigned physical room metadata |
| `primary_guest` | JSON string | `JSONB` | No | 91 | `{"firstName": "Abigail", ...}` | Guest personal and contact profile |
| `validation_messages` | float64 | `JSONB` | Yes (100%) | 0 | `NULL` | Validation notes from PMS engine |

---

## 3. `folios.csv` (Billing Folios)

| Column Name | Source Type | Target SQL Type | Nullable | Unique | Sample Value | Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | string | `VARCHAR(64) PRIMARY KEY` | No | 205 | `LNIGSXXC-98-1-1`, `*-BOOK` | Unique folio record identifier |
| `external_id` | string | `VARCHAR(64)` | No | 205 | `LNIGSXXC-98-1-1` | External PMS folio identifier |
| `reservation_id` | string | `VARCHAR(64) REFERENCES reservations(id)` | Yes (51.2%) | 100 | `LNIGSXXC-98-1` | Linked reservation ID (null for Booking/House) |
| `booking_id` | string | `VARCHAR(32)` | Yes (2.4%) | 100 | `LNIGSXXC` | Linked group booking (null for House folios) |
| `property_id` | string | `VARCHAR(16) REFERENCES properties(id)` | No | 5 | `BER`, `LND`, `VIE` | Linked property identifier |
| `type` | string | `VARCHAR(32)` | No | 3 | `Guest`, `Booking`, `House` | Classification of billing account |
| `status` | string | `VARCHAR(32)` | No | 2 | `Open`, `Closed` | Lifecycle state of folio |
| `balance` | float64 | `NUMERIC(12,2)` | No | 1 | `0.0` | Current folio unbilled balance |
| `created_at` | string (ISO) | `TIMESTAMPTZ` | No | 105 | `2026-08-10T17:04:37+02:00` | Folio creation timestamp |
| `updated_at` | string (ISO) | `TIMESTAMPTZ` | No | 105 | `2026-08-10T17:04:37+02:00` | Last folio modification timestamp |
| `closing_date` | string | `TIMESTAMPTZ` | Yes (100%) | 0 | `NULL` | Formal folio close timestamp |
| `is_main_folio` | bool | `BOOLEAN` | No | 2 | `True`, `False` | True if default routing folio |
| `is_empty` | bool | `BOOLEAN` | No | 2 | `True`, `False` | True if no line items posted |
| `checked_out_on_ar` | bool | `BOOLEAN` | No | 1 | `False` | Accounts Receivable checkout flag |
| `debtor_data` | string (JSON) | `JSONB` | Yes | 91 | `{"title": ...}` | Debtor / billing entity profile |
| `company_data` | float64 | `JSONB` | Yes (100%) | 0 | `NULL` | Corporate bill-back entity |
| `charges` | float64 | `JSONB` | Yes (100%) | 0 | `NULL` | Folio charge array (managed in charges ledger) |
| `payments` | float64 | `JSONB` | Yes (100%) | 0 | `NULL` | Folio payment array (managed in payments ledger)|

---

## 4. `invoices.csv` (Invoices & Settlements)

| Column Name | Source Type | Target SQL Type | Nullable | Unique | Sample Value | Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | string | `VARCHAR(64) PRIMARY KEY` | No | 200 | `LNIGSXXC-98-1-INV-1` | Unique invoice identifier |
| `external_id` | string | `VARCHAR(64)` | No | 200 | `LNIGSXXC-98-1-INV-1` | External PMS invoice reference |
| `invoice_number` | string | `VARCHAR(64)` | No | 200 | `INV-BER-2026-0001` | Official statutory tax invoice number |
| `folio_id` | string | `VARCHAR(64)` | No | 200 | `LNIGSXXC-98-1-1` | Folio from which invoice was generated |
| `reservation_id` | string | `VARCHAR(64) REFERENCES reservations(id)` | No | 100 | `LNIGSXXC-98-1` | Linked reservation |
| `booking_id` | string | `VARCHAR(32)` | No | 100 | `LNIGSXXC` | Linked group booking |
| `property_id` | string | `VARCHAR(16) REFERENCES properties(id)` | No | 5 | `BER`, `LND`, `VIE` | Associated property |
| `property_country_code`| string | `VARCHAR(2)` | No | 4 | `DE`, `GB`, `FR`, `AT` | Country jurisdiction for tax |
| `status` | string | `VARCHAR(32)` | No | 1 | `ISSUED` | Invoice lifecycle state |
| `type` | string | `VARCHAR(32)` | No | 1 | `STAY` | Invoice type |
| `payment_settled` | bool | `BOOLEAN` | No | 2 | `True`, `False` | Whether payment was fully settled in PMS |
| `total` | float64 | `NUMERIC(12,2)` | No | 77 | `240.00`, `130.59` | Total invoice gross payable |
| `created_at` | string (ISO) | `TIMESTAMPTZ` | No | 196 | `2026-09-19T00:00:00+02:00` | Generation timestamp |
| `invoice_date` | string | `DATE` | No | 49 | `2026-09-19` | Statutory fiscal tax date |
| `due_from` | string | `DATE` | No | 49 | `2026-09-19` | Payment term start date |
| `due_to` | string | `DATE` | No | 49 | `2026-09-19` | Payment maturity date |
| `language_code` | string | `VARCHAR(5)` | No | 1 | `en` | Invoice document language |
| `line_items` | string (JSON) | `JSONB` | No | 180 | `[{"description": "Room", ...}]` | Granular itemized billing lines |
| `payments` | string (JSON) | `JSONB` | No | 1 | `[]` | Embedded payment list (empty in export) |
| `outstanding_payment` | float64 | `NUMERIC(12,2)` | No | 2 | `0.0`, `130.59` | Unsettled invoice receivable balance |
| `stay_info` | string (JSON) | `JSONB` | No | 100 | `{"arrival": ..., "room": ...}` | Guest stay summary metadata |

---

## 5. `charges_full.csv` (Itemized Charges)

| Column Name | Source Type | Target SQL Type | Nullable | Unique | Sample Value | Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | string | `VARCHAR(64) PRIMARY KEY` | No | 200 | `chg-001` | Unique charge record ID |
| `reservation_id` | string | `VARCHAR(64)` | No | 100 | `QHMMYUKY-1` | Linked reservation ID |
| `folio_id` | string | `VARCHAR(64)` | No | 100 | `QHMMYUKY-1-1` | Linked folio ID |
| `property_id` | string | `VARCHAR(16) REFERENCES properties(id)` | No | 5 | `BER`, `LND`, `PAR` | Property ID |
| `charge_type` | string | `VARCHAR(32)` | No | 5 | `ROOM`, `BREAKFAST`, `PARKING` | Department / revenue center |
| `description` | string | `VARCHAR(255)` | No | 5 | `Room Night Charge`, `Breakfast` | Description of billed item |
| `quantity` | int64 / float | `INTEGER` | No | 4 | `1`, `2`, `3` | Number of units consumed |
| `unit_price` | float64 | `NUMERIC(12,2)` | No | 68 | `85.00`, `15.00` | Pre-tax unit price |
| `tax_amount` | float64 | `NUMERIC(12,2)` | No | 68 | `17.00`, `3.00` | Calculated VAT / sales tax |
| `gross_amount` | float64 | `NUMERIC(12,2)` | No | 72 | `102.00`, `18.00` | Net payable (`quantity * unit_price + tax`)|
| `charge_date` | string | `DATE` | No | 55 | `2026-09-08` | Posting date |
| `currency` | string | `VARCHAR(3)` | No | 2 | `EUR`, `GBP` | ISO 4217 Currency code |
| `data_source` | string | `VARCHAR(32)` | No | 1 | `synthetic` | Lineage provenance tag |

---

## 6. `payments_full.csv` (Payments & Transactions)

| Column Name | Source Type | Target SQL Type | Nullable | Unique | Sample Value | Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | string | `VARCHAR(64) PRIMARY KEY` | No | 100 | `QHMMYUKY-1-payment` | Payment record identifier |
| `reservation_id` | string | `VARCHAR(64)` | No | 100 | `QHMMYUKY-1` | Linked reservation ID |
| `folio_id` | string | `VARCHAR(64)` | No | 100 | `QHMMYUKY-1-1` | Linked folio ID |
| `property_id` | string | `VARCHAR(16) REFERENCES properties(id)` | No | 5 | `BER`, `LND`, `MUC` | Property ID |
| `payment_method` | string | `VARCHAR(32)` | No | 3 | `CREDIT_CARD`, `BANK_TRANSFER`, `CASH`| Settlement rail |
| `amount` | float64 | `NUMERIC(12,2)` | No | 75 | `327.65`, `154.52` | Settlement monetary amount |
| `payment_date` | string | `DATE` | No | 55 | `2026-09-11` | Transaction settlement date |
| `currency` | string | `VARCHAR(3)` | No | 2 | `EUR`, `GBP` | ISO 4217 Currency |
| `transaction_reference`| string | `VARCHAR(64)` | No | 100 | `SYN-QHMMYUKY-1-PAY` | Gateway / bank authorization code |
| `status` | string | `VARCHAR(32)` | No | 2 | `PARTIALLY_PAID`, `FULLY_PAID` | Reconciliation state |
| `data_source` | string | `VARCHAR(32)` | No | 1 | `synthetic` | Lineage provenance tag |

---

## 7. `synthetic_invoices_full.csv` (Reconciliation Invoices)

| Column Name | Source Type | Target SQL Type | Nullable | Unique | Sample Value | Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | string | `VARCHAR(64) PRIMARY KEY` | No | 100 | `QHMMYUKY-1-invoice` | Invoice identifier |
| `invoice_number` | string | `VARCHAR(64)` | No | 100 | `SYN-QHMMYUKY-1` | Synthetic invoice audit number |
| `folio_id` | string | `VARCHAR(64)` | No | 100 | `QHMMYUKY-1-1` | Linked folio ID |
| `reservation_id` | string | `VARCHAR(64)` | No | 100 | `QHMMYUKY-1` | Linked reservation ID |
| `property_id` | string | `VARCHAR(16) REFERENCES properties(id)` | No | 5 | `BER`, `LND`, `VIE` | Property ID |
| `total` | float64 | `NUMERIC(12,2)` | No | 75 | `337.65`, `164.52` | Expected invoice gross total |
| `invoice_date` | string | `DATE` | No | 50 | `2026-09-08` | Billing date |
| `status` | string | `VARCHAR(32)` | No | 1 | `ISSUED` | Invoice state |
| `data_source` | string | `VARCHAR(32)` | No | 1 | `synthetic` | Lineage provenance tag |

---

## 8. `ota_reservations_full.csv` (OTA Settlements)

| Column Name | Source Type | Target SQL Type | Nullable | Unique | Sample Value | Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | string | `VARCHAR(64) PRIMARY KEY` | No | 20 | `ota-AEBWEDVV-1` | Record ID |
| `ota_name` | string | `VARCHAR(64)` | No | 4 | `Booking.com`, `Expedia`, `Agoda` | Distribution channel name |
| `ota_reservation_id` | string | `VARCHAR(64)` | No | 20 | `SYN-OTA-AEBWEDVV-1` | Channel partner booking ID |
| `pms_reservation_id` | string | `VARCHAR(64)` | No | 20 | `AEBWEDVV-1` | Internal PMS reservation match ID |
| `property_id` | string | `VARCHAR(16) REFERENCES properties(id)` | No | 5 | `PAR`, `BER`, `LND` | Property ID |
| `booking_date` | string | `DATE` | No | 1 | `2026-08-10` | Channel booking capture date |
| `arrival` | string | `DATE` | No | 18 | `2026-08-23` | Check-in date |
| `departure` | string | `DATE` | No | 18 | `2026-08-28` | Check-out date |
| `room_nights` | int64 | `INTEGER` | No | 6 | `5`, `6`, `2` | Total room nights |
| `gross_amount` | float64 | `NUMERIC(12,2)` | No | 20 | `107.44`, `150.18` | Total guest charge on OTA portal |
| `commission_rate` | float64 | `NUMERIC(5,4)` | No | 2 | `0.1500`, `0.1800` | Contracted OTA commission rate |
| `commission_amount` | float64 | `NUMERIC(12,2)` | No | 20 | `16.12`, `22.53` | Contracted commission deducted |
| `expected_settlement`| float64 | `NUMERIC(12,2)` | No | 20 | `91.32`, `127.65` | Contracted net remittance payout |
| `actual_settlement` | float64 | `NUMERIC(12,2)` | Yes (20%) | 16 | `91.32`, `117.65` | Actual bank transfer received |
| `settlement_date` | string | `DATE` | Yes (20%) | 16 | `2026-08-28` | Date funds credited to hotel account |
| `currency` | string | `VARCHAR(3)` | No | 2 | `EUR`, `GBP` | Remittance currency |
| `status` | string | `VARCHAR(32)` | No | 2 | `SETTLED`, `MISSING` | Payout status |
| `reconciliation_scenario`| string | `VARCHAR(64)` | No | 5 | `exact`, `underpayment`, `overpayment`, `missing_settlement`, `commission_discrepancy` | Controlled discrepancy scenario |
| `data_source` | string | `VARCHAR(32)` | No | 1 | `synthetic` | Lineage provenance tag |

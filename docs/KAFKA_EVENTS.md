# Kafka Event-Driven Processing Specification

## 1. Overview

The platform uses an event-driven architecture to decouple real-time Property Management System operational events from analytical agent computations. When a front-desk transaction occurs (e.g. guest check-in, invoice generation, payment received, OTA settlement), an immutable business event is published to Apache Kafka.

When running in local development mode without an active Kafka cluster, events are automatically persisted to the transactional `business_events` table in PostgreSQL / SQLite, where the `EventConsumer` processes them without loss.

---

## 2. Event Topics & Schemas

All event payloads adhere to the CloudEvents specification:

```json
{
  "event_id": "evt_98f12a34b5c6",
  "event_type": "reservation.created",
  "timestamp": "2026-10-11T12:00:00Z",
  "property_id": "BER",
  "entity_type": "reservation",
  "entity_id": "LNIGSXXC-98-1",
  "payload": {
    "total_gross_amount": 253.40,
    "status": "InHouse",
    "adults": 2,
    "arrival": "2026-09-17",
    "departure": "2026-09-19"
  },
  "source": "pms_ingestion_layer",
  "schema_version": "1.0.0"
}
```

### Supported Topics & Events:

| Topic Name | Event Types | Producing Source | Subscribed Agent |
| :--- | :--- | :--- | :--- |
| `hospitality.reservation` | `reservation.created`, `reservation.updated`, `reservation.cancelled` | PMS Guest Ledger | Revenue Insight Agent |
| `hospitality.invoice` | `invoice.generated`, `invoice.updated` | PMS Billing Engine | Reconciliation Agent |
| `hospitality.payment` | `payment.received`, `payment.failed` | Payment Gateway / Reception | Reconciliation Agent |
| `hospitality.ota_settlement` | `ota.settlement.received`, `ota.settlement.discrepancy` | Channel Manager Batch Remittance | Reconciliation Agent |
| `hospitality.expense` | `expense.recorded`, `expense.anomaly_flagged` | Accounting Ledger / ERP | Expense Tracking Agent |

---

## 3. Agent Subscription Flow

```
+----------------------------------------------------------------------------------+
|                            KAFKA EVENT CONSUMER                                  |
|               (or Background Database Poller in Dev Mode)                        |
+----------------------------------------------------------------------------------+
                                        │
             ┌──────────────────────────┼──────────────────────────┐
             ▼                          ▼                          ▼
    Payment / Settlement           Reservation Event          Expense Event
             │                          │                          │
             ▼                          ▼                          ▼
+──────────────────────────+ +──────────────────────────+ +──────────────────────────+
|  Reconciliation Agent    | |   Revenue Insight Agent  | |      Expense Agent       |
|  - Invoices vs Payments  | |   - Recalculates ADR     | |   - Computes Z-Score     |
|  - Flags OTA variances   | |   - Updates Occupancy    | |   - Raises Spikes Alert  |
+──────────────────────────+ +──────────────────────────+ +──────────────────────────+
```

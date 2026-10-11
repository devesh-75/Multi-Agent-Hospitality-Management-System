"""
Data Loader Pipeline
Loads validated, normalized records from CSV adapter and synthetic generators into the unified database.
Supports safe repeated execution (idempotency).
"""

import os
import sys
import logging
from typing import Dict, Any

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath("."))

from backend.app.core.database import SessionLocal, init_db, engine, Base
from backend.app.models.entities import (
    Property, RoomType, Room, Guest, RatePlan, Reservation, Folio,
    Invoice, InvoiceItem, Charge, Payment, OTASettlement,
    Expense, Competitor, CompetitorFeature, CompetitorPrice,
    CompetitorReview, CompetitorSnapshot, BusinessEvent
)
from ingestion.source_adapters.csv_adapter import CSVPMSAdapter
from scripts.seed_missing_entities import generate_synthetic_expenses, generate_synthetic_competitors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_all_data(data_dir: str = r"C:\Users\deves\Downloads\project") -> Dict[str, int]:
    logger.info("Initializing database schema...")
    init_db()
    
    db = SessionLocal()
    adapter = CSVPMSAdapter(data_dir=data_dir)
    stats = {}

    try:
        # Wipe and reload for clean idempotent state during setup
        logger.info("Clearing previous records to ensure idempotent reload...")
        for model in [
            BusinessEvent, CompetitorSnapshot, CompetitorReview, CompetitorPrice, CompetitorFeature, Competitor,
            Expense, OTASettlement, Payment, Charge, InvoiceItem, Invoice, Folio,
            Reservation, Room, RoomType, RatePlan, Guest, Property
        ]:
            db.query(model).delete()
        db.commit()

        # 1. Properties
        logger.info("Loading properties...")
        props_data = adapter.fetch_properties()
        for p in props_data:
            db.add(Property(**p))
        db.commit()
        stats["properties"] = len(props_data)

        # 2. Rooms, Room Types, Rate Plans, Guests
        logger.info("Loading rooms, room types, rate plans, and guests...")
        aux = adapter.fetch_rooms_and_types()
        for rt in aux["room_types"]:
            db.add(RoomType(**rt))
        db.commit()
        stats["room_types"] = len(aux["room_types"])

        for r in aux["rooms"]:
            db.add(Room(**r))
        db.commit()
        stats["rooms"] = len(aux["rooms"])

        for rp in aux["rate_plans"]:
            db.add(RatePlan(**rp))
        db.commit()
        stats["rate_plans"] = len(aux["rate_plans"])

        for g in aux["guests"]:
            db.add(Guest(**g))
        db.commit()
        stats["guests"] = len(aux["guests"])

        # 3. Reservations
        logger.info("Loading reservations...")
        res_data = adapter.fetch_reservations()
        for res in res_data:
            db.add(Reservation(**res))
        db.commit()
        stats["reservations"] = len(res_data)

        # 4. Folios
        logger.info("Loading folios...")
        folios_data = adapter.fetch_folios()
        for fol in folios_data:
            db.add(Folio(**fol))
        db.commit()
        stats["folios"] = len(folios_data)

        # 5. Invoices & Line Items
        logger.info("Loading invoices and line items...")
        inv_data = adapter.fetch_invoices()
        items_count = 0
        for inv in inv_data:
            items = inv.pop("items", [])
            inv_obj = Invoice(**inv)
            db.add(inv_obj)
            db.flush()
            for it in items:
                db.add(InvoiceItem(
                    id=f"ITM-{inv_obj.id}-{items_count+1}",
                    invoice_id=inv_obj.id,
                    **it
                ))
                items_count += 1
        db.commit()
        stats["invoices"] = len(inv_data)
        stats["invoice_items"] = items_count

        # 6. Charges
        logger.info("Loading charges...")
        chg_data = adapter.fetch_charges()
        for chg in chg_data:
            db.add(Charge(**chg))
        db.commit()
        stats["charges"] = len(chg_data)

        # 7. Payments
        logger.info("Loading payments...")
        pmt_data = adapter.fetch_payments()
        for pmt in pmt_data:
            db.add(Payment(**pmt))
        db.commit()
        stats["payments"] = len(pmt_data)

        # 8. OTA Settlements
        logger.info("Loading OTA settlements...")
        ota_data = adapter.fetch_ota_settlements()
        for ota in ota_data:
            db.add(OTASettlement(**ota))
        db.commit()
        stats["ota_settlements"] = len(ota_data)

        # 9. Synthetic Operational Expenses
        logger.info("Seeding operational expenses...")
        exp_data = generate_synthetic_expenses()
        for exp in exp_data:
            db.add(Expense(**exp))
        db.commit()
        stats["expenses"] = len(exp_data)

        # 10. Synthetic Competitors & Intelligence
        logger.info("Seeding competitor intelligence...")
        comp_bundle = generate_synthetic_competitors()
        for c in comp_bundle["competitors"]:
            db.add(Competitor(**c))
        db.commit()
        stats["competitors"] = len(comp_bundle["competitors"])

        for f in comp_bundle["features"]:
            db.add(CompetitorFeature(**f))
        for p in comp_bundle["prices"]:
            db.add(CompetitorPrice(**p))
        for r in comp_bundle["reviews"]:
            db.add(CompetitorReview(**r))
        for s in comp_bundle["snapshots"]:
            db.add(CompetitorSnapshot(**s))
        db.commit()
        stats["competitor_features"] = len(comp_bundle["features"])
        stats["competitor_prices"] = len(comp_bundle["prices"])
        stats["competitor_reviews"] = len(comp_bundle["reviews"])
        stats["competitor_snapshots"] = len(comp_bundle["snapshots"])

        # 11. Initial Business Events
        logger.info("Publishing initial business events...")
        event_count = 0
        for r in res_data[:10]:
            evt = BusinessEvent(
                id=f"EVT-RES-{r['id']}",
                event_id=f"evt_{r['id']}",
                event_type="reservation.created",
                property_id=r["property_id"],
                entity_type="reservation",
                entity_id=r["id"],
                payload={"total_gross_amount": r["total_gross_amount"], "status": r["status"]},
                processed=True
            )
            db.add(evt)
            event_count += 1

        for o in ota_data[:5]:
            evt = BusinessEvent(
                id=f"EVT-OTA-{o['id']}",
                event_id=f"evt_{o['id']}",
                event_type="ota.settlement.received",
                property_id=o["property_id"],
                entity_type="ota_settlement",
                entity_id=o["id"],
                payload={"gross_amount": o["gross_amount"], "reconciliation_scenario": o["reconciliation_scenario"]},
                processed=True
            )
            db.add(evt)
            event_count += 1
        db.commit()
        stats["business_events"] = event_count

        logger.info("Data loading completed successfully!")
        return stats

    except Exception as e:
        db.rollback()
        logger.error(f"Error during data loading: {e}", exc_info=True)
        raise
    finally:
        db.close()

if __name__ == "__main__":
    loaded_stats = load_all_data()
    print("\n--- INGESTION SUMMARY ---")
    for k, v in loaded_stats.items():
        print(f"{k:<25}: {v}")

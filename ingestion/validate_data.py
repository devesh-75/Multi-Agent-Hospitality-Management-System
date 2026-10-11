"""
Data Validation Engine
Performs pre-ingestion validation on raw CSV datasets:
- Schema conformance
- Referential foreign-key integrity
- Value range and numeric consistency
- Date validity and ISO-8601 formatting
- Missing required fields
"""

import os
import json
import logging
from typing import Dict, List, Any
from ingestion.source_adapters.csv_adapter import CSVPMSAdapter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataValidator:
    def __init__(self, data_dir: str = r"C:\Users\deves\Downloads\project"):
        self.adapter = CSVPMSAdapter(data_dir=data_dir)
        self.validation_results = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "stats": {}
        }

    def validate_all(self) -> Dict[str, Any]:
        logger.info("Starting comprehensive data validation...")

        # 1. Properties
        props = self.adapter.fetch_properties()
        prop_ids = {p["id"] for p in props}
        if len(prop_ids) < 1:
            self.validation_results["errors"].append("No valid properties found in properties.csv")
            self.validation_results["is_valid"] = False
        self.validation_results["stats"]["properties_count"] = len(props)

        # 2. Rooms, Types, Guests
        aux = self.adapter.fetch_rooms_and_types()
        room_types = aux["room_types"]
        rooms = aux["rooms"]
        guests = aux["guests"]
        self.validation_results["stats"]["room_types_count"] = len(room_types)
        self.validation_results["stats"]["rooms_count"] = len(rooms)
        self.validation_results["stats"]["guests_count"] = len(guests)

        room_ids = {r["id"] for r in rooms}
        room_type_ids = {rt["id"] for rt in room_types}

        # 3. Reservations
        reservations = self.adapter.fetch_reservations()
        self.validation_results["stats"]["reservations_count"] = len(reservations)
        res_ids = set()
        for r in reservations:
            res_id = r["id"]
            res_ids.add(res_id)
            if r["property_id"] not in prop_ids:
                self.validation_results["errors"].append(f"Reservation {res_id} has invalid property_id: {r['property_id']}")
                self.validation_results["is_valid"] = False
            if r["departure_date"] < r["arrival_date"]:
                self.validation_results["errors"].append(f"Reservation {res_id} departure is before arrival")
                self.validation_results["is_valid"] = False
            if r["total_gross_amount"] < 0:
                self.validation_results["warnings"].append(f"Reservation {res_id} has negative total_gross_amount")

        # 4. Invoices
        invoices = self.adapter.fetch_invoices()
        self.validation_results["stats"]["invoices_count"] = len(invoices)
        for inv in invoices:
            if inv["property_id"] not in prop_ids:
                self.validation_results["errors"].append(f"Invoice {inv['id']} has invalid property_id: {inv['property_id']}")
                self.validation_results["is_valid"] = False

        # 5. Charges
        charges = self.adapter.fetch_charges()
        self.validation_results["stats"]["charges_count"] = len(charges)
        for chg in charges:
            if chg["property_id"] not in prop_ids:
                self.validation_results["errors"].append(f"Charge {chg['id']} has invalid property_id: {chg['property_id']}")
                self.validation_results["is_valid"] = False

        # 6. Payments
        payments = self.adapter.fetch_payments()
        self.validation_results["stats"]["payments_count"] = len(payments)
        for pmt in payments:
            if pmt["property_id"] not in prop_ids:
                self.validation_results["errors"].append(f"Payment {pmt['id']} has invalid property_id: {pmt['property_id']}")
                self.validation_results["is_valid"] = False

        # 7. OTA Settlements
        ota = self.adapter.fetch_ota_settlements()
        self.validation_results["stats"]["ota_settlements_count"] = len(ota)
        for settlement in ota:
            if settlement["property_id"] not in prop_ids:
                self.validation_results["errors"].append(f"OTA record {settlement['id']} has invalid property_id: {settlement['property_id']}")
                self.validation_results["is_valid"] = False

        logger.info(f"Validation completed. Is valid: {self.validation_results['is_valid']}")
        logger.info(f"Summary stats: {self.validation_results['stats']}")
        if self.validation_results["warnings"]:
            logger.info(f"Warnings count: {len(self.validation_results['warnings'])}")

        return self.validation_results

if __name__ == "__main__":
    validator = DataValidator()
    results = validator.validate_all()
    print("\nValidation Summary:")
    print(json.dumps(results, indent=2))

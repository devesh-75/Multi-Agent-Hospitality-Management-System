"""
CSV PMS Adapter
Reads local CSV exports from C:\\Users\\deves\\Downloads\\project and converts them to unified dictionaries.
Strictly non-destructive: Original CSV files are opened in read-only mode and never modified.
"""

import os
import json
import logging
import pandas as pd
from typing import Dict, List, Any
from backend.app.core.config import settings
from ingestion.source_adapters.base_adapter import BasePMSAdapter

logger = logging.getLogger(__name__)

class CSVPMSAdapter(BasePMSAdapter):
    """Adapter for importing datasets from local CSV files."""

    def __init__(self, data_dir: str = settings.SOURCE_DATA_DIR):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            raise FileNotFoundError(f"Source data directory does not exist: {self.data_dir}")

    def _read_csv(self, filename: str) -> pd.DataFrame:
        fpath = os.path.join(self.data_dir, filename)
        if not os.path.exists(fpath):
            raise FileNotFoundError(f"Missing required CSV file: {fpath}")
        return pd.read_csv(fpath)

    def fetch_properties(self) -> List[Dict[str, Any]]:
        df = self._read_csv("properties.csv")
        records = []
        for _, row in df.iterrows():
            name_val = row["name"]
            try:
                name_json = json.loads(name_val)
                name_str = name_json.get("en", list(name_json.values())[0]) if isinstance(name_json, dict) else str(name_val)
            except Exception:
                name_str = str(name_val)
                
            currency = "GBP" if row["country_code"] == "GB" else "EUR"
            records.append({
                "id": str(row["id"]),
                "code": str(row["code"]),
                "company_name": str(row["company_name"]),
                "name": name_str,
                "status": str(row.get("status", "Active")),
                "is_archived": bool(row.get("is_archived", False)),
                "country_code": str(row["country_code"]),
                "timezone": str(row["timezone"]),
                "currency": currency,
                "created_at": pd.to_datetime(row["created_at"]).to_pydatetime() if pd.notnull(row.get("created_at")) else None,
                "is_synthetic": False,
                "source_file": "properties.csv"
            })
        return records

    def fetch_rooms_and_types(self) -> Dict[str, List[Dict[str, Any]]]:
        res_df = self._read_csv("reservations.csv")
        room_types_map = {}
        rooms_map = {}
        guests_map = {}
        rate_plans_map = {}

        for _, row in res_df.iterrows():
            prop_id = str(row["property_id"])

            # Room Type
            if pd.notnull(row.get("unit_group_data")):
                try:
                    ug = json.loads(row["unit_group_data"])
                    ug_id = str(ug.get("id"))
                    if ug_id not in room_types_map:
                        room_types_map[ug_id] = {
                            "id": ug_id,
                            "code": str(ug.get("code", "")),
                            "name": str(ug.get("name", "")),
                            "description": str(ug.get("description", "")),
                            "category": str(ug.get("type", "BedRoom")),
                            "property_id": prop_id
                        }
                except Exception as e:
                    logger.debug(f"Error parsing unit_group_data: {e}")

            # Room
            if pd.notnull(row.get("unit_data")):
                try:
                    u = json.loads(row["unit_data"])
                    u_id = str(u.get("id"))
                    if u_id not in rooms_map:
                        rooms_map[u_id] = {
                            "id": u_id,
                            "room_number": str(u.get("name", "")),
                            "description": str(u.get("description", "")),
                            "room_type_id": str(u.get("unitGroupId", "")),
                            "property_id": prop_id
                        }
                except Exception as e:
                    logger.debug(f"Error parsing unit_data: {e}")

            # Rate Plan
            if pd.notnull(row.get("rate_plan_data")):
                try:
                    rp = json.loads(row["rate_plan_data"])
                    rp_id = str(rp.get("id"))
                    if rp_id not in rate_plans_map:
                        rate_plans_map[rp_id] = {
                            "id": rp_id,
                            "code": str(rp.get("code", "")),
                            "name": str(rp.get("name", "")),
                            "description": str(rp.get("description", "")),
                            "property_id": prop_id
                        }
                except Exception as e:
                    logger.debug(f"Error parsing rate_plan_data: {e}")

            # Guest
            if pd.notnull(row.get("primary_guest")):
                try:
                    g = json.loads(row["primary_guest"])
                    g_email = g.get("email")
                    if g_email and g_email not in guests_map:
                        addr = g.get("address", {}) or {}
                        guests_map[g_email] = {
                            "id": f"GST-{len(guests_map)+1:04d}",
                            "first_name": str(g.get("firstName", "")),
                            "last_name": str(g.get("lastName", "")),
                            "email": str(g_email),
                            "phone": str(g.get("phone", "")),
                            "address": str(addr.get("addressLine1", "")),
                            "postal_code": str(addr.get("postalCode", "")),
                            "city": str(addr.get("city", "")),
                            "country_code": str(addr.get("countryCode", ""))
                        }
                except Exception as e:
                    logger.debug(f"Error parsing primary_guest: {e}")

        return {
            "room_types": list(room_types_map.values()),
            "rooms": list(rooms_map.values()),
            "rate_plans": list(rate_plans_map.values()),
            "guests": list(guests_map.values()),
            "guests_email_to_id": {g["email"]: g["id"] for g in guests_map.values()}
        }

    def fetch_reservations(self, property_id: str = None) -> List[Dict[str, Any]]:
        res_df = self._read_csv("reservations.csv")
        aux = self.fetch_rooms_and_types()
        email_to_id = aux["guests_email_to_id"]

        records = []
        for _, row in res_df.iterrows():
            if property_id and str(row["property_id"]) != property_id:
                continue

            guest_id = None
            if pd.notnull(row.get("primary_guest")):
                try:
                    g = json.loads(row["primary_guest"])
                    guest_id = email_to_id.get(g.get("email"))
                except Exception:
                    pass

            room_id = None
            if pd.notnull(row.get("unit_data")):
                try:
                    u = json.loads(row["unit_data"])
                    room_id = u.get("id")
                except Exception:
                    pass

            room_type_id = None
            if pd.notnull(row.get("unit_group_data")):
                try:
                    ug = json.loads(row["unit_group_data"])
                    room_type_id = ug.get("id")
                except Exception:
                    pass

            rate_plan_id = None
            if pd.notnull(row.get("rate_plan_data")):
                try:
                    rp = json.loads(row["rate_plan_data"])
                    rate_plan_id = rp.get("id")
                except Exception:
                    pass

            records.append({
                "id": str(row["id"]),
                "external_id": str(row.get("external_id", row["id"])),
                "booking_id": str(row["booking_id"]),
                "property_id": str(row["property_id"]),
                "room_id": room_id,
                "room_type_id": room_type_id,
                "guest_id": guest_id,
                "rate_plan_id": rate_plan_id,
                "status": str(row["status"]),
                "arrival_date": pd.to_datetime(row["arrival"]).to_pydatetime(),
                "departure_date": pd.to_datetime(row["departure"]).to_pydatetime(),
                "adults": int(row.get("adults", 1)),
                "channel_code": str(row.get("channel_code", "Direct")),
                "total_gross_amount": float(row.get("total_gross_amount", 0.0)),
                "balance": float(row.get("balance", 0.0)),
                "guarantee_type": str(row.get("guarantee_type", "CreditCard")),
                "has_city_tax": bool(row.get("has_city_tax", False)),
                "is_open_for_charges": bool(row.get("is_open_for_charges", True)),
                "created_at": pd.to_datetime(row["created_at"]).to_pydatetime() if pd.notnull(row.get("created_at")) else None,
                "modified_at": pd.to_datetime(row["modified_at"]).to_pydatetime() if pd.notnull(row.get("modified_at")) else None,
                "is_synthetic": False,
                "source_file": "reservations.csv"
            })
        return records

    def fetch_folios(self, property_id: str = None) -> List[Dict[str, Any]]:
        df = self._read_csv("folios.csv")
        records = []
        for _, row in df.iterrows():
            if property_id and str(row["property_id"]) != property_id:
                continue

            debtor_name = None
            if pd.notnull(row.get("debtor_data")):
                try:
                    d = json.loads(row["debtor_data"])
                    first = d.get("firstName", "")
                    last = d.get("lastName", "")
                    debtor_name = f"{first} {last}".strip() or None
                except Exception:
                    debtor_name = str(row["debtor_data"])[:255]

            records.append({
                "id": str(row["id"]),
                "external_id": str(row.get("external_id", row["id"])),
                "reservation_id": str(row["reservation_id"]) if pd.notnull(row.get("reservation_id")) else None,
                "booking_id": str(row["booking_id"]) if pd.notnull(row.get("booking_id")) else None,
                "property_id": str(row["property_id"]),
                "type": str(row.get("type", "Guest")),
                "status": str(row.get("status", "Open")),
                "balance": float(row.get("balance", 0.0)),
                "is_main_folio": bool(row.get("is_main_folio", True)),
                "is_empty": bool(row.get("is_empty", False)),
                "debtor_name": debtor_name,
                "created_at": pd.to_datetime(row["created_at"]).to_pydatetime() if pd.notnull(row.get("created_at")) else None,
                "updated_at": pd.to_datetime(row["updated_at"]).to_pydatetime() if pd.notnull(row.get("updated_at")) else None,
                "is_synthetic": False,
                "source_file": "folios.csv"
            })
        return records

    def fetch_invoices(self, property_id: str = None) -> List[Dict[str, Any]]:
        # Ingest both real PMS invoices and synthetic reconciliation invoices
        records = []
        inv_df = self._read_csv("invoices.csv")
        for _, row in inv_df.iterrows():
            if property_id and str(row["property_id"]) != property_id:
                continue
            
            line_items_data = []
            if pd.notnull(row.get("line_items")):
                try:
                    items = json.loads(row["line_items"])
                    for it in items:
                        line_items_data.append({
                            "description": str(it.get("description", "Room Charge")),
                            "quantity": float(it.get("quantity", 1)),
                            "unit_price": float(it.get("unit_price", 0.0)),
                            "amount": float(it.get("amount", 0.0))
                        })
                except Exception:
                    pass

            # Parse outstanding_payment JSON or float
            outstanding_val = 0.0
            raw_outstanding = row.get("outstanding_payment")
            if pd.notnull(raw_outstanding):
                if isinstance(raw_outstanding, (int, float)):
                    outstanding_val = float(raw_outstanding)
                else:
                    try:
                        parsed = json.loads(str(raw_outstanding))
                        if isinstance(parsed, dict):
                            outstanding_val = float(parsed.get("amount", 0.0))
                            if not currency and parsed.get("currency"):
                                currency = parsed.get("currency")
                        else:
                            outstanding_val = float(parsed)
                    except Exception:
                        try:
                            outstanding_val = float(raw_outstanding)
                        except Exception:
                            outstanding_val = 0.0

            currency = "GBP" if str(row.get("property_country_code")) == "GB" else "EUR"
            records.append({
                "id": str(row["id"]),
                "external_id": str(row.get("external_id", row["id"])),
                "invoice_number": str(row["invoice_number"]),
                "folio_id": str(row.get("folio_id")),
                "reservation_id": str(row.get("reservation_id")),
                "booking_id": str(row.get("booking_id")),
                "property_id": str(row["property_id"]),
                "property_country_code": str(row.get("property_country_code")),
                "status": str(row.get("status", "ISSUED")),
                "type": str(row.get("type", "STAY")),
                "payment_settled": bool(row.get("payment_settled", False)),
                "total_amount": float(row.get("total", 0.0)),
                "outstanding_balance": outstanding_val,
                "invoice_date": pd.to_datetime(row["invoice_date"]).date(),
                "due_from": pd.to_datetime(row["due_from"]).date() if pd.notnull(row.get("due_from")) else None,
                "due_to": pd.to_datetime(row["due_to"]).date() if pd.notnull(row.get("due_to")) else None,
                "currency": currency,
                "language_code": str(row.get("language_code", "en")),
                "created_at": pd.to_datetime(row["created_at"]).to_pydatetime() if pd.notnull(row.get("created_at")) else None,
                "is_synthetic": False,
                "source_file": "invoices.csv",
                "items": line_items_data
            })

        # Synthetic invoices for reconciliation suite
        syn_df = self._read_csv("synthetic_invoices_full.csv")
        for _, row in syn_df.iterrows():
            if property_id and str(row["property_id"]) != property_id:
                continue
            currency = "GBP" if str(row["property_id"]) == "LND" else "EUR"
            records.append({
                "id": str(row["id"]),
                "external_id": str(row["id"]),
                "invoice_number": str(row["invoice_number"]),
                "folio_id": str(row["folio_id"]),
                "reservation_id": str(row["reservation_id"]),
                "booking_id": None,
                "property_id": str(row["property_id"]),
                "property_country_code": "GB" if str(row["property_id"]) == "LND" else "DE",
                "status": str(row.get("status", "ISSUED")),
                "type": "STAY",
                "payment_settled": False,
                "total_amount": float(row.get("total", 0.0)),
                "outstanding_balance": float(row.get("total", 0.0)),
                "invoice_date": pd.to_datetime(row["invoice_date"]).date(),
                "due_from": pd.to_datetime(row["invoice_date"]).date(),
                "due_to": pd.to_datetime(row["invoice_date"]).date(),
                "currency": currency,
                "language_code": "en",
                "created_at": pd.to_datetime(row["invoice_date"]).to_pydatetime(),
                "is_synthetic": True,
                "source_file": "synthetic_invoices_full.csv",
                "items": []
            })
        return records

    def fetch_payments(self, property_id: str = None) -> List[Dict[str, Any]]:
        df = self._read_csv("payments_full.csv")
        records = []
        for _, row in df.iterrows():
            if property_id and str(row["property_id"]) != property_id:
                continue
            records.append({
                "id": str(row["id"]),
                "reservation_id": str(row["reservation_id"]),
                "folio_id": str(row.get("folio_id")),
                "property_id": str(row["property_id"]),
                "payment_method": str(row["payment_method"]),
                "amount": float(row["amount"]),
                "payment_date": pd.to_datetime(row["payment_date"]).date(),
                "currency": str(row.get("currency", "EUR")),
                "transaction_reference": str(row.get("transaction_reference", "")),
                "status": str(row.get("status", "PARTIALLY_PAID")),
                "is_synthetic": True,
                "source_file": "payments_full.csv"
            })
        return records

    def fetch_charges(self, property_id: str = None) -> List[Dict[str, Any]]:
        df = self._read_csv("charges_full.csv")
        records = []
        for _, row in df.iterrows():
            if property_id and str(row["property_id"]) != property_id:
                continue
            records.append({
                "id": str(row["id"]),
                "reservation_id": str(row["reservation_id"]),
                "folio_id": str(row.get("folio_id")),
                "property_id": str(row["property_id"]),
                "charge_type": str(row["charge_type"]),
                "description": str(row["description"]),
                "quantity": float(row.get("quantity", 1)),
                "unit_price": float(row.get("unit_price", 0.0)),
                "tax_amount": float(row.get("tax_amount", 0.0)),
                "gross_amount": float(row.get("gross_amount", 0.0)),
                "charge_date": pd.to_datetime(row["charge_date"]).date(),
                "currency": str(row.get("currency", "EUR")),
                "is_synthetic": True,
                "source_file": "charges_full.csv"
            })
        return records

    def fetch_ota_settlements(self, property_id: str = None) -> List[Dict[str, Any]]:
        df = self._read_csv("ota_reservations_full.csv")
        records = []
        for _, row in df.iterrows():
            if property_id and str(row["property_id"]) != property_id:
                continue
            records.append({
                "id": str(row["id"]),
                "channel_name": str(row["ota_name"]),
                "ota_reservation_id": str(row["ota_reservation_id"]),
                "reservation_id": str(row["pms_reservation_id"]),
                "property_id": str(row["property_id"]),
                "booking_date": pd.to_datetime(row["booking_date"]).date(),
                "arrival_date": pd.to_datetime(row["arrival"]).date(),
                "departure_date": pd.to_datetime(row["departure"]).date(),
                "room_nights": int(row.get("room_nights", 1)),
                "gross_amount": float(row.get("gross_amount", 0.0)),
                "commission_rate": float(row.get("commission_rate", 0.15)),
                "commission_amount": float(row.get("commission_amount", 0.0)),
                "expected_settlement": float(row.get("expected_settlement", 0.0)),
                "actual_settlement": float(row["actual_settlement"]) if pd.notnull(row.get("actual_settlement")) else None,
                "settlement_date": pd.to_datetime(row["settlement_date"]).date() if pd.notnull(row.get("settlement_date")) else None,
                "currency": str(row.get("currency", "EUR")),
                "status": str(row.get("status", "SETTLED")),
                "reconciliation_scenario": str(row.get("reconciliation_scenario", "exact")),
                "is_synthetic": True,
                "source_file": "ota_reservations_full.csv"
            })
        return records

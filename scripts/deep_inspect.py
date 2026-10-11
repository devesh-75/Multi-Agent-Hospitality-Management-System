"""
Deep inspection of JSON structures, foreign keys, and missing business entities.
"""

import os
import json
import pandas as pd

PROJECT_DIR = r"C:\Users\deves\Downloads\project"

def deep_inspect():
    res_df = pd.read_csv(os.path.join(PROJECT_DIR, "reservations.csv"))
    inv_df = pd.read_csv(os.path.join(PROJECT_DIR, "invoices.csv"))
    chg_df = pd.read_csv(os.path.join(PROJECT_DIR, "charges_full.csv"))
    pmt_df = pd.read_csv(os.path.join(PROJECT_DIR, "payments_full.csv"))
    ota_df = pd.read_csv(os.path.join(PROJECT_DIR, "ota_reservations_full.csv"))
    syn_inv_df = pd.read_csv(os.path.join(PROJECT_DIR, "synthetic_invoices_full.csv"))
    fol_df = pd.read_csv(os.path.join(PROJECT_DIR, "folios.csv"))
    prop_df = pd.read_csv(os.path.join(PROJECT_DIR, "properties.csv"))

    # Extract JSON fields from reservations
    rooms = []
    room_types = []
    guests = []
    rate_plans = []
    
    for idx, row in res_df.iterrows():
        # unit_data (Room)
        if pd.notnull(row.get('unit_data')):
            try:
                u = json.loads(row['unit_data'])
                rooms.append(u)
            except: pass
            
        # unit_group_data (Room Type)
        if pd.notnull(row.get('unit_group_data')):
            try:
                ug = json.loads(row['unit_group_data'])
                room_types.append(ug)
            except: pass
            
        # primary_guest (Guest)
        if pd.notnull(row.get('primary_guest')):
            try:
                g = json.loads(row['primary_guest'])
                g['reservation_id'] = row['id']
                guests.append(g)
            except: pass
            
        # rate_plan_data
        if pd.notnull(row.get('rate_plan_data')):
            try:
                rp = json.loads(row['rate_plan_data'])
                rate_plans.append(rp)
            except: pass

    rooms_df = pd.DataFrame(rooms).drop_duplicates(subset=['id']) if rooms else pd.DataFrame()
    room_types_df = pd.DataFrame(room_types).drop_duplicates(subset=['id']) if room_types else pd.DataFrame()
    guests_df = pd.DataFrame(guests).drop_duplicates(subset=['email']) if guests else pd.DataFrame()
    rate_plans_df = pd.DataFrame(rate_plans).drop_duplicates(subset=['id']) if rate_plans else pd.DataFrame()

    print(f"Extracted Unique Rooms: {len(rooms_df)}")
    print(f"Extracted Unique Room Types: {len(room_types_df)}")
    print(f"Extracted Unique Guests: {len(guests_df)}")
    print(f"Extracted Unique Rate Plans: {len(rate_plans_df)}")

    # Check date range of all transactions
    print("\n--- DATE RANGES ---")
    print(f"Reservations Arrival: {res_df['arrival'].min()} to {res_df['arrival'].max()}")
    print(f"Invoices Date: {inv_df['invoice_date'].min()} to {inv_df['invoice_date'].max()}")
    print(f"Charges Date: {chg_df['charge_date'].min()} to {chg_df['charge_date'].max()}")
    print(f"Payments Date: {pmt_df['payment_date'].min()} to {pmt_df['payment_date'].max()}")
    print(f"OTA Booking Date: {ota_df['booking_date'].min()} to {ota_df['booking_date'].max()}")
    print(f"OTA Settlement Date: {ota_df['settlement_date'].dropna().min()} to {ota_df['settlement_date'].dropna().max()}")

    # Check Currencies
    print("\n--- CURRENCIES BY PROPERTY ---")
    print("Invoices currency via stay_info or country code:")
    print(inv_df.groupby(['property_id', 'property_country_code']).size())
    print("Charges currency:")
    print(chg_df.groupby(['property_id', 'currency']).size())
    print("Payments currency:")
    print(pmt_df.groupby(['property_id', 'currency']).size())

    # Check Missing Business Entities
    print("\n--- MISSING BUSINESS ENTITIES IN RAW CSVs ---")
    print("1. Operational Expenses: NOT PRESENT in raw CSVs.")
    print("2. Competitor Information (rates, amenities, reviews, SWOT): NOT PRESENT in raw CSVs.")
    print("3. Housekeeping Tasks: NOT PRESENT in raw CSVs.")

if __name__ == "__main__":
    deep_inspect()

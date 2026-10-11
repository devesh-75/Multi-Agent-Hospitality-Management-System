"""
Deterministic Synthetic Entity Generator for Missing Hospitality Domains
Generates:
1. Departmental Operational Expenses (Payroll, Utilities, Maintenance, F&B, Linen, SaaS, Marketing)
2. Competitor Intelligence Master, Features, Pricing History, Reviews, and Performance Snapshots

Rules:
- Uses fixed random seed 42 for 100% reproducibility.
- All records carry is_synthetic = True and source_type = 'synthetic_seed'.
- Preserves referential integrity to the 5 real properties (BER, LND, MUC, PAR, VIE).
"""

import random
from datetime import date, timedelta
from typing import List, Dict, Any

random.seed(42)

def generate_synthetic_expenses() -> List[Dict[str, Any]]:
    properties = ["BER", "LND", "MUC", "PAR", "VIE"]
    categories = [
        ("Payroll", ["Front Desk Staffing Solutions", "Hospitality Personnel Ltd", "European Hospitality Staff AG"]),
        ("Utilities", ["Berliner Stadtwerke", "London Hydro & Power", "EDF Energy France", "Wien Energie GmbH"]),
        ("F&B Supplies", ["Metro Cash & Carry", "Sysco European Wholesale", "Brakes Foodservice", "Transgourmet"]),
        ("Linen & Laundry", ["CleanLinen Euro Services", "Elis Hospitality Laundry", "Alsco Uniforms & Linen"]),
        ("SaaS & PMS", ["Apaleo Cloud PMS", "BookingCenter CRS", "SiteMinder Channel Manager", "Stripe Tech Fees"]),
        ("Maintenance", ["Schindler Elevators", "Siemens HVAC Systems", "ProClean Facility Maintenance"]),
        ("Marketing", ["Google Ads Hospitality", "Meta Ads Tourism", "Expedia Partner Solutions Marketing"])
    ]

    start_date = date(2026, 8, 1)
    end_date = date(2026, 10, 25)
    days = (end_date - start_date).days

    expenses = []
    exp_counter = 1

    for prop_id in properties:
        curr = "GBP" if prop_id == "LND" else "EUR"
        
        # Monthly fixed expenses (Payroll, SaaS)
        for month_offset in [0, 31, 61]:
            d = start_date + timedelta(days=month_offset + random.randint(1, 5))
            # Payroll
            expenses.append({
                "id": f"EXP-{prop_id}-{exp_counter:04d}",
                "property_id": prop_id,
                "category": "Payroll",
                "vendor_name": "Hospitality Personnel Ltd" if prop_id == "LND" else "European Hospitality Staff AG",
                "description": f"Monthly staff payroll and front-desk remuneration ({d.strftime('%B %Y')})",
                "amount": round(random.uniform(9500.0, 14000.0), 2),
                "currency": curr,
                "expense_date": d,
                "status": "APPROVED",
                "is_synthetic": True,
                "source_type": "synthetic_seed"
            })
            exp_counter += 1

            # SaaS
            expenses.append({
                "id": f"EXP-{prop_id}-{exp_counter:04d}",
                "property_id": prop_id,
                "category": "SaaS & PMS",
                "vendor_name": "Apaleo Cloud PMS",
                "description": f"Core PMS subscription and API throughput tier ({d.strftime('%B %Y')})",
                "amount": round(random.uniform(1200.0, 1800.0), 2),
                "currency": curr,
                "expense_date": d,
                "status": "APPROVED",
                "is_synthetic": True,
                "source_type": "synthetic_seed"
            })
            exp_counter += 1

        # Periodic operating expenses
        for _ in range(12):
            d = start_date + timedelta(days=random.randint(0, days))
            cat_tuple = random.choice([c for c in categories if c[0] not in ["Payroll", "SaaS & PMS"]])
            category, vendors = cat_tuple
            vendor = random.choice(vendors)

            # Base amount by category
            if category == "Utilities":
                base_amt = random.uniform(1800.0, 3200.0)
            elif category == "F&B Supplies":
                base_amt = random.uniform(1200.0, 2800.0)
            elif category == "Linen & Laundry":
                base_amt = random.uniform(800.0, 1500.0)
            elif category == "Maintenance":
                base_amt = random.uniform(500.0, 2200.0)
            else: # Marketing
                base_amt = random.uniform(600.0, 1600.0)

            expenses.append({
                "id": f"EXP-{prop_id}-{exp_counter:04d}",
                "property_id": prop_id,
                "category": category,
                "vendor_name": vendor,
                "description": f"Operating expenditure: {category} supplies and maintenance",
                "amount": round(base_amt, 2),
                "currency": curr,
                "expense_date": d,
                "status": "APPROVED",
                "is_synthetic": True,
                "source_type": "synthetic_seed"
            })
            exp_counter += 1

        # Controlled anomaly: High unexpected HVAC / plumbing emergency repair in September for BER and LND
        if prop_id in ["BER", "LND"]:
            anomaly_date = date(2026, 9, 14)
            expenses.append({
                "id": f"EXP-{prop_id}-{exp_counter:04d}",
                "property_id": prop_id,
                "category": "Maintenance",
                "vendor_name": "Emergency Facility Engineering GmbH",
                "description": "ANOMALY: Emergency chiller compressor overhaul and boiler valve replacement",
                "amount": round(7850.00 if curr == "EUR" else 6900.00, 2),
                "currency": curr,
                "expense_date": anomaly_date,
                "status": "APPROVED",
                "is_synthetic": True,
                "source_type": "synthetic_seed"
            })
            exp_counter += 1

    return expenses


def generate_synthetic_competitors() -> Dict[str, Any]:
    comp_defs = [
        # Berlin (BER)
        {"id": "COMP-BER-01", "name": "Motel One Berlin-Alexanderplatz", "brand": "Motel One", "city": "Berlin", "country_code": "DE", "star_rating": 3.8, "distance_km": 0.8, "target_property_id": "BER"},
        {"id": "COMP-BER-02", "name": "CitizenM Berlin Mitte", "brand": "CitizenM", "city": "Berlin", "country_code": "DE", "star_rating": 4.4, "distance_km": 1.2, "target_property_id": "BER"},
        {"id": "COMP-BER-03", "name": "Scandic Berlin Potsdamer Platz", "brand": "Scandic", "city": "Berlin", "country_code": "DE", "star_rating": 4.1, "distance_km": 1.9, "target_property_id": "BER"},
        # London (LND)
        {"id": "COMP-LND-01", "name": "The Hoxton Shoreditch", "brand": "The Hoxton", "city": "London", "country_code": "GB", "star_rating": 4.5, "distance_km": 0.9, "target_property_id": "LND"},
        {"id": "COMP-LND-02", "name": "CitizenM Tower of London", "brand": "CitizenM", "city": "London", "country_code": "GB", "star_rating": 4.3, "distance_km": 1.5, "target_property_id": "LND"},
        {"id": "COMP-LND-03", "name": "Apex City of London Hotel", "brand": "Apex Hotels", "city": "London", "country_code": "GB", "star_rating": 4.0, "distance_km": 1.8, "target_property_id": "LND"},
        # Munich (MUC)
        {"id": "COMP-MUC-01", "name": "Ruby Lilly Hotel Munich", "brand": "Ruby Hotels", "city": "Munich", "country_code": "DE", "star_rating": 4.3, "distance_km": 0.7, "target_property_id": "MUC"},
        {"id": "COMP-MUC-02", "name": "25hours Hotel The Royal Bavarian", "brand": "25hours", "city": "Munich", "country_code": "DE", "star_rating": 4.6, "distance_km": 1.4, "target_property_id": "MUC"},
        # Paris (PAR)
        {"id": "COMP-PAR-01", "name": "Mama Shelter Paris East", "brand": "Mama Shelter", "city": "Paris", "country_code": "FR", "star_rating": 4.2, "distance_km": 1.1, "target_property_id": "PAR"},
        {"id": "COMP-PAR-02", "name": "CitizenM Paris Gare de Lyon", "brand": "CitizenM", "city": "Paris", "country_code": "FR", "star_rating": 4.4, "distance_km": 1.6, "target_property_id": "PAR"},
        # Vienna (VIE)
        {"id": "COMP-VIE-01", "name": "25hours Hotel Museumsquartier", "brand": "25hours", "city": "Vienna", "country_code": "AT", "star_rating": 4.5, "distance_km": 0.6, "target_property_id": "VIE"},
        {"id": "COMP-VIE-02", "name": "Motel One Wien-Staatsoper", "brand": "Motel One", "city": "Vienna", "country_code": "AT", "star_rating": 4.1, "distance_km": 1.3, "target_property_id": "VIE"}
    ]

    # Amenity feature catalog for feature-gap analysis
    feature_catalog = [
        ("Rooftop Bar & Lounge", "F&B"),
        ("24/7 Co-Working Space", "Service"),
        ("Keyless Mobile Check-In", "Tech"),
        ("EV Charging Stations", "Amenity"),
        ("Artisan Specialty Coffee Bar", "F&B"),
        ("Pet-Friendly Rooms", "Service"),
        ("Wellness & Finnish Sauna", "Amenity"),
        ("Complimentary High-Speed WiFi (Gigabit)", "Tech"),
        ("Designer Rainfall Showers", "Amenity"),
        ("Smart Room Tablet Automation", "Tech")
    ]

    features = []
    feat_counter = 1
    for comp in comp_defs:
        c_id = comp["id"]
        for feat_name, cat in feature_catalog:
            # Deterministic availability
            avail = "Confirmed Available" if random.random() > 0.35 else ("Confirmed Unavailable" if random.random() > 0.4 else "Unknown")
            features.append({
                "id": f"FEAT-{feat_counter:04d}",
                "competitor_id": c_id,
                "feature_name": feat_name,
                "category": cat,
                "status": avail,
                "notes": f"Observed via public OTA / website audit in Oct 2026.",
                "is_synthetic": True
            })
            feat_counter += 1

    # Pricing history (Daily rates across August - October 2026)
    prices = []
    price_counter = 1
    start_date = date(2026, 8, 10)
    for comp in comp_defs:
        c_id = comp["id"]
        curr = "GBP" if comp["country_code"] == "GB" else "EUR"
        base_rate = 145.0 if curr == "EUR" else 165.0
        if "CitizenM" in comp["name"] or "Hoxton" in comp["name"] or "25hours" in comp["name"]:
            base_rate += 35.0

        for day_idx in range(0, 75, 3): # Every 3 days snapshot
            obs_date = start_date + timedelta(days=day_idx)
            # Weekend surge
            multiplier = 1.25 if obs_date.weekday() in [4, 5] else 1.0
            price_val = round((base_rate * multiplier) + random.uniform(-12.0, 18.0), 2)
            prices.append({
                "id": f"PRC-{price_counter:05d}",
                "competitor_id": c_id,
                "room_type": "Standard Double",
                "price": price_val,
                "currency": curr,
                "observation_date": obs_date,
                "channel": "Booking.com / Public Web",
                "is_synthetic": True
            })
            price_counter += 1

    # Reviews and reputation
    reviews = []
    rev_counter = 1
    complaints = [
        "Elevators crowded during 10:00 AM check-out surge",
        "Street traffic audible on 2nd floor street-facing units",
        "Air conditioning took 30 minutes to cool room down",
        "Breakfast buffet line delayed on Saturday morning"
    ]
    praises = [
        "Vibrant rooftop bar ambiance and cocktail selection",
        "Seamless digital check-in in under 45 seconds",
        "Exceptional specialty espresso and warm bakery selection",
        "Co-working lounge desks with ergonomic chairs and fiber WiFi"
    ]

    for comp in comp_defs:
        c_id = comp["id"]
        reviews.append({
            "id": f"REV-{rev_counter:04d}",
            "competitor_id": c_id,
            "platform": "Google Reviews",
            "rating": round(comp["star_rating"] + random.uniform(-0.15, 0.15), 2),
            "review_count": random.randint(350, 1850),
            "sentiment_score": round(random.uniform(0.65, 0.88), 2),
            "top_complaint": random.choice(complaints),
            "top_praise": random.choice(praises),
            "observation_date": date(2026, 10, 1),
            "is_synthetic": True
        })
        rev_counter += 1

        reviews.append({
            "id": f"REV-{rev_counter:04d}",
            "competitor_id": c_id,
            "platform": "Tripadvisor",
            "rating": round(comp["star_rating"] + random.uniform(-0.2, 0.1), 2),
            "review_count": random.randint(220, 980),
            "sentiment_score": round(random.uniform(0.60, 0.82), 2),
            "top_complaint": random.choice(complaints),
            "top_praise": random.choice(praises),
            "observation_date": date(2026, 10, 1),
            "is_synthetic": True
        })
        rev_counter += 1

    # Benchmarking Snapshots
    snapshots = []
    snap_counter = 1
    for comp in comp_defs:
        snapshots.append({
            "id": f"SNAP-{snap_counter:04d}",
            "competitor_id": comp["id"],
            "property_id": comp["target_property_id"],
            "observation_date": date(2026, 10, 10),
            "adr_estimate": round(random.uniform(130.0, 185.0), 2),
            "occupancy_estimate": round(random.uniform(76.0, 89.5), 1),
            "revpar_estimate": round(random.uniform(105.0, 155.0), 2),
            "is_synthetic": True
        })
        snap_counter += 1

    return {
        "competitors": comp_defs,
        "features": features,
        "prices": prices,
        "reviews": reviews,
        "snapshots": snapshots
    }

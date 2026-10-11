# Business Development Executive (BDE) & Competitive Intelligence Agent

## 1. Executive Purpose & Strategic Mandate

The **Business Development Executive (BDE) Agent** is a core specialized agent designed to answer three fundamental hospitality business questions:
1. *What are competing hotels in our local market doing better than us?*
2. *Where do amenity, pricing, and distribution gaps exist between our property and competitors?*
3. *What evidence-grounded operational and financial actions can improve our market position and RevPAR?*

The BDE Agent strictly delivers **evidence-based decision support**, avoiding unsupported generic business advice.

---

## 2. Competitive Intelligence Data Model

Competitor data is structured into dedicated relational tables within the unified database:

```
+----------------------------------------------------------------------------------+
|                            COMPETITORS MASTER (competitors)                      |
|  - id, name, brand, city, country_code, star_rating, distance_km, target_property|
+----------------------------------------------------------------------------------+
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
+──────────────────────+     +──────────────────────+     +──────────────────────+
| COMPETITOR FEATURES  |     |  COMPETITOR PRICES   |     |  COMPETITOR REVIEWS  |
| (competitor_features)|     | (competitor_prices)  |     | (competitor_reviews) |
| - feature_name       |     | - room_type          |     | - platform           |
| - category (F&B/Tech)|     | - price, currency    |     | - rating, reviews    |
| - status             |     | - observation_date   |     | - sentiment_score    |
| - notes              |     | - booking_channel    |     | - top complaints/praise|
+──────────────────────+     +──────────────────────+     +──────────────────────+
```

---

## 3. Key Analytical Capabilities

### 3.1 Competitor Performance Benchmarking
Compares internal Property Management System operational metrics (ADR, RevPAR, Occupancy) against localized competitive sets:
- **Berlin (`BER`):** Motel One Berlin-Alexanderplatz, CitizenM Berlin Mitte, Scandic Berlin Potsdamer Platz
- **London (`LND`):** The Hoxton Shoreditch, CitizenM Tower of London, Apex City of London Hotel
- **Munich (`MUC`):** Ruby Lilly Hotel Munich, 25hours Hotel The Royal Bavarian
- **Paris (`PAR`):** Mama Shelter Paris East, CitizenM Paris Gare de Lyon
- **Vienna (`VIE`):** 25hours Hotel Museumsquartier, Motel One Wien-Staatsoper

### 3.2 Competitive Feature-Gap Analysis
Audits amenity presence across three explicit states:
- `Confirmed Available`
- `Confirmed Unavailable`
- `Unknown / Not Recorded`

For each identified feature gap, the system outputs:
- **Feature & Category:** e.g., *Keyless Mobile Check-In (Tech)* or *Rooftop Bar (F&B)*
- **Competitor Penetration:** Percentage and names of local competitors offering the feature
- **Business Severity:** Ranked as High, Medium, or Low based on market adoption
- **Actionable Next Step:** Suggested feasibility assessment or vendor onboarding

### 3.3 Grounded Data-Driven SWOT Analysis
Unlike generic AI SWOT outputs, every single statement cites specific empirical data:
- **Strengths:** Cites exact booked revenue figures and low cancellation rates from PMS reservations.
- **Weaknesses:** Cites exact outstanding receivables from unsettled folios and identified amenity gaps.
- **Opportunities:** Quantifies OTA commission recovery potential (15-18%) and premium weekend rate headroom.
- **Threats:** Measures average competitor proximity in kilometers and flags unresolved OTA settlement exceptions.

### 3.4 Actionable Business Growth Recommendations
In strict adherence to Section 14.7, every recommendation follows an 8-part structured format:
1. **Observation:** What the empirical data indicates.
2. **Evidence:** Concrete records, metrics, competitors, and observation dates.
3. **Business Opportunity:** Why this matters for profitability.
4. **Recommended Action:** Realistic operational next step.
5. **Expected Business Impact:** Directional or quantified financial projection.
6. **Confidence Level:** High, Medium, or Low.
7. **Data Limitations:** Stated uncertainties and boundary conditions.
8. **Human Validation Required:** Mandatory management verification checkpoint before execution.

---

## 4. Ethical Standards & Non-Fabrication Policy
- **No Unconsented Scraping:** The system does not bypass CAPTCHAs, violate terms of service, or evade paywalls.
- **Explicit Provenance:** All demonstration competitor records are tagged with `is_synthetic = TRUE` and visually badged in the UI.
- **No Autonomous Execution:** The BDE Agent never alters live room prices, pays vendors, or publishes promotional campaigns autonomously. It provides decision support for human management sign-off.

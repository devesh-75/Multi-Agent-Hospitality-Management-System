-- =====================================================================
-- UNIFIED DATABASE SCHEMA: AGENTIC FINTECH IN HOSPITALITY SERVICES
-- Compatible with PostgreSQL 15+ and SQLite3
-- =====================================================================

-- 1. Property Master
CREATE TABLE IF NOT EXISTS properties (
    id VARCHAR(16) PRIMARY KEY,
    code VARCHAR(16) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'Active',
    is_archived BOOLEAN NOT NULL DEFAULT FALSE,
    country_code VARCHAR(2) NOT NULL,
    timezone VARCHAR(64) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'EUR',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_synthetic BOOLEAN NOT NULL DEFAULT FALSE,
    source_file VARCHAR(64) DEFAULT 'properties.csv'
);

-- 2. Room Types
CREATE TABLE IF NOT EXISTS room_types (
    id VARCHAR(64) PRIMARY KEY,
    code VARCHAR(32) NOT NULL,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    category VARCHAR(64) DEFAULT 'BedRoom',
    property_id VARCHAR(16) REFERENCES properties(id)
);

-- 3. Rooms
CREATE TABLE IF NOT EXISTS rooms (
    id VARCHAR(64) PRIMARY KEY,
    room_number VARCHAR(32) NOT NULL,
    description VARCHAR(255),
    room_type_id VARCHAR(64) REFERENCES room_types(id),
    property_id VARCHAR(16) REFERENCES properties(id)
);

-- 4. Guests
CREATE TABLE IF NOT EXISTS guests (
    id VARCHAR(64) PRIMARY KEY,
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    email VARCHAR(255),
    phone VARCHAR(64),
    address VARCHAR(255),
    postal_code VARCHAR(32),
    city VARCHAR(128),
    country_code VARCHAR(2)
);

-- 5. Rate Plans
CREATE TABLE IF NOT EXISTS rate_plans (
    id VARCHAR(64) PRIMARY KEY,
    code VARCHAR(32) NOT NULL,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    property_id VARCHAR(16) REFERENCES properties(id)
);

-- 6. Reservations
CREATE TABLE IF NOT EXISTS reservations (
    id VARCHAR(64) PRIMARY KEY,
    external_id VARCHAR(64),
    booking_id VARCHAR(32) NOT NULL,
    property_id VARCHAR(16) NOT NULL REFERENCES properties(id),
    room_id VARCHAR(64) REFERENCES rooms(id),
    room_type_id VARCHAR(64) REFERENCES room_types(id),
    guest_id VARCHAR(64) REFERENCES guests(id),
    rate_plan_id VARCHAR(64) REFERENCES rate_plans(id),
    status VARCHAR(32) NOT NULL, -- Confirmed, InHouse, CheckedOut, Cancelled
    arrival_date TIMESTAMP WITH TIME ZONE NOT NULL,
    departure_date TIMESTAMP WITH TIME ZONE NOT NULL,
    adults INTEGER NOT NULL DEFAULT 1,
    channel_code VARCHAR(32) DEFAULT 'Direct',
    total_gross_amount NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    balance NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    guarantee_type VARCHAR(32) DEFAULT 'CreditCard',
    has_city_tax BOOLEAN DEFAULT FALSE,
    is_open_for_charges BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP WITH TIME ZONE,
    is_synthetic BOOLEAN NOT NULL DEFAULT FALSE,
    source_file VARCHAR(64) DEFAULT 'reservations.csv'
);

-- 7. Folios
CREATE TABLE IF NOT EXISTS folios (
    id VARCHAR(64) PRIMARY KEY,
    external_id VARCHAR(64),
    reservation_id VARCHAR(64),
    booking_id VARCHAR(32),
    property_id VARCHAR(16) NOT NULL REFERENCES properties(id),
    type VARCHAR(32) NOT NULL, -- Guest, Booking, House
    status VARCHAR(32) NOT NULL DEFAULT 'Open',
    balance NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    is_main_folio BOOLEAN DEFAULT TRUE,
    is_empty BOOLEAN DEFAULT FALSE,
    debtor_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    is_synthetic BOOLEAN NOT NULL DEFAULT FALSE,
    source_file VARCHAR(64) DEFAULT 'folios.csv'
);

-- 8. Invoices
CREATE TABLE IF NOT EXISTS invoices (
    id VARCHAR(64) PRIMARY KEY,
    external_id VARCHAR(64),
    invoice_number VARCHAR(64) NOT NULL,
    folio_id VARCHAR(64),
    reservation_id VARCHAR(64),
    booking_id VARCHAR(32),
    property_id VARCHAR(16) NOT NULL REFERENCES properties(id),
    property_country_code VARCHAR(2),
    status VARCHAR(32) NOT NULL DEFAULT 'ISSUED',
    type VARCHAR(32) DEFAULT 'STAY',
    payment_settled BOOLEAN DEFAULT FALSE,
    total_amount NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    outstanding_balance NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    invoice_date DATE NOT NULL,
    due_from DATE,
    due_to DATE,
    currency VARCHAR(3) DEFAULT 'EUR',
    language_code VARCHAR(5) DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_synthetic BOOLEAN NOT NULL DEFAULT FALSE,
    source_file VARCHAR(64) DEFAULT 'invoices.csv'
);

-- 9. Invoice Items
CREATE TABLE IF NOT EXISTS invoice_items (
    id VARCHAR(64) PRIMARY KEY,
    invoice_id VARCHAR(64) NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    description VARCHAR(255) NOT NULL,
    quantity NUMERIC(10, 2) NOT NULL DEFAULT 1,
    unit_price NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    amount NUMERIC(12, 2) NOT NULL DEFAULT 0.00
);

-- 10. Charges
CREATE TABLE IF NOT EXISTS charges (
    id VARCHAR(64) PRIMARY KEY,
    reservation_id VARCHAR(64) NOT NULL,
    folio_id VARCHAR(64),
    property_id VARCHAR(16) NOT NULL REFERENCES properties(id),
    charge_type VARCHAR(32) NOT NULL, -- ROOM, BREAKFAST, RESTAURANT, MINIBAR, PARKING
    description VARCHAR(255) NOT NULL,
    quantity NUMERIC(10, 2) NOT NULL DEFAULT 1,
    unit_price NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    tax_amount NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    gross_amount NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    charge_date DATE NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'EUR',
    is_synthetic BOOLEAN NOT NULL DEFAULT FALSE,
    source_file VARCHAR(64) DEFAULT 'charges_full.csv'
);

-- 11. Payments
CREATE TABLE IF NOT EXISTS payments (
    id VARCHAR(64) PRIMARY KEY,
    reservation_id VARCHAR(64) NOT NULL,
    folio_id VARCHAR(64),
    property_id VARCHAR(16) NOT NULL REFERENCES properties(id),
    payment_method VARCHAR(32) NOT NULL, -- CREDIT_CARD, BANK_TRANSFER, CASH
    amount NUMERIC(12, 2) NOT NULL,
    payment_date DATE NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'EUR',
    transaction_reference VARCHAR(64),
    status VARCHAR(32) NOT NULL DEFAULT 'PARTIALLY_PAID', -- FULLY_PAID, PARTIALLY_PAID
    is_synthetic BOOLEAN NOT NULL DEFAULT FALSE,
    source_file VARCHAR(64) DEFAULT 'payments_full.csv'
);

-- 12. OTA Settlements
CREATE TABLE IF NOT EXISTS ota_settlements (
    id VARCHAR(64) PRIMARY KEY,
    channel_name VARCHAR(64) NOT NULL, -- Booking.com, Expedia, Agoda, Airbnb
    ota_reservation_id VARCHAR(64) NOT NULL,
    reservation_id VARCHAR(64) NOT NULL,
    property_id VARCHAR(16) NOT NULL REFERENCES properties(id),
    booking_date DATE NOT NULL,
    arrival_date DATE NOT NULL,
    departure_date DATE NOT NULL,
    room_nights INTEGER NOT NULL DEFAULT 1,
    gross_amount NUMERIC(12, 2) NOT NULL,
    commission_rate NUMERIC(5, 4) NOT NULL,
    commission_amount NUMERIC(12, 2) NOT NULL,
    expected_settlement NUMERIC(12, 2) NOT NULL,
    actual_settlement NUMERIC(12, 2),
    settlement_date DATE,
    currency VARCHAR(3) NOT NULL DEFAULT 'EUR',
    status VARCHAR(32) NOT NULL DEFAULT 'SETTLED', -- SETTLED, MISSING
    reconciliation_scenario VARCHAR(64) NOT NULL, -- exact, underpayment, overpayment, missing_settlement, commission_discrepancy
    is_synthetic BOOLEAN NOT NULL DEFAULT TRUE,
    source_file VARCHAR(64) DEFAULT 'ota_reservations_full.csv'
);

-- 13. Operational Expenses
CREATE TABLE IF NOT EXISTS expenses (
    id VARCHAR(64) PRIMARY KEY,
    property_id VARCHAR(16) NOT NULL REFERENCES properties(id),
    category VARCHAR(64) NOT NULL, -- Payroll, Utilities, F&B Supplies, Linen & Laundry, SaaS & PMS, Maintenance, Marketing
    vendor_name VARCHAR(255) NOT NULL,
    description TEXT,
    amount NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'EUR',
    expense_date DATE NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'APPROVED',
    is_synthetic BOOLEAN NOT NULL DEFAULT TRUE,
    source_type VARCHAR(64) DEFAULT 'synthetic_seed'
);

-- 14. Competitor Master
CREATE TABLE IF NOT EXISTS competitors (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(128),
    city VARCHAR(128) NOT NULL,
    country_code VARCHAR(2) NOT NULL,
    star_rating NUMERIC(2, 1) DEFAULT 4.0,
    distance_km NUMERIC(5, 2) DEFAULT 1.0,
    target_property_id VARCHAR(16) REFERENCES properties(id),
    is_synthetic BOOLEAN NOT NULL DEFAULT TRUE
);

-- 15. Competitor Properties & Features
CREATE TABLE IF NOT EXISTS competitor_features (
    id VARCHAR(64) PRIMARY KEY,
    competitor_id VARCHAR(64) NOT NULL REFERENCES competitors(id) ON DELETE CASCADE,
    feature_name VARCHAR(128) NOT NULL,
    category VARCHAR(64) NOT NULL, -- Amenity, Service, Tech, F&B
    status VARCHAR(32) NOT NULL DEFAULT 'Confirmed Available', -- Confirmed Available, Confirmed Unavailable, Unknown
    notes TEXT,
    is_synthetic BOOLEAN NOT NULL DEFAULT TRUE
);

-- 16. Competitor Pricing Observations
CREATE TABLE IF NOT EXISTS competitor_prices (
    id VARCHAR(64) PRIMARY KEY,
    competitor_id VARCHAR(64) NOT NULL REFERENCES competitors(id) ON DELETE CASCADE,
    room_type VARCHAR(64) NOT NULL,
    price NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'EUR',
    observation_date DATE NOT NULL,
    channel VARCHAR(64) DEFAULT 'Direct / Booking.com',
    is_synthetic BOOLEAN NOT NULL DEFAULT TRUE
);

-- 17. Competitor Reviews & Reputation
CREATE TABLE IF NOT EXISTS competitor_reviews (
    id VARCHAR(64) PRIMARY KEY,
    competitor_id VARCHAR(64) NOT NULL REFERENCES competitors(id) ON DELETE CASCADE,
    platform VARCHAR(64) NOT NULL, -- Google Reviews, Tripadvisor, Booking.com
    rating NUMERIC(3, 2) NOT NULL,
    review_count INTEGER NOT NULL,
    sentiment_score NUMERIC(3, 2), -- -1.0 to 1.0
    top_complaint TEXT,
    top_praise TEXT,
    observation_date DATE NOT NULL,
    is_synthetic BOOLEAN NOT NULL DEFAULT TRUE
);

-- 18. Competitor Snapshots (Aggregated KPI Benchmarks)
CREATE TABLE IF NOT EXISTS competitor_snapshots (
    id VARCHAR(64) PRIMARY KEY,
    competitor_id VARCHAR(64) NOT NULL REFERENCES competitors(id) ON DELETE CASCADE,
    property_id VARCHAR(16) REFERENCES properties(id),
    observation_date DATE NOT NULL,
    adr_estimate NUMERIC(12, 2),
    occupancy_estimate NUMERIC(5, 2),
    revpar_estimate NUMERIC(12, 2),
    is_synthetic BOOLEAN NOT NULL DEFAULT TRUE
);

-- 19. Business Events (Event-Driven Streaming Log)
CREATE TABLE IF NOT EXISTS business_events (
    id VARCHAR(64) PRIMARY KEY,
    event_id VARCHAR(64) NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    property_id VARCHAR(16),
    entity_type VARCHAR(64) NOT NULL,
    entity_id VARCHAR(64) NOT NULL,
    payload JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

-- 20. Agent Execution Runs
CREATE TABLE IF NOT EXISTS agent_runs (
    id VARCHAR(64) PRIMARY KEY,
    agent_name VARCHAR(64) NOT NULL,
    property_id VARCHAR(16),
    status VARCHAR(32) NOT NULL, -- RUNNING, COMPLETED, FAILED
    input_parameters JSONB,
    result_summary JSONB,
    execution_time_ms INTEGER,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- 21. Actionable Alerts
CREATE TABLE IF NOT EXISTS alerts (
    id VARCHAR(64) PRIMARY KEY,
    alert_type VARCHAR(64) NOT NULL, -- RECONCILIATION_EXCEPTION, EXPENSE_ANOMALY, COMPETITOR_PRICE_DROP, AMENITY_GAP
    severity VARCHAR(16) NOT NULL DEFAULT 'MEDIUM', -- LOW, MEDIUM, HIGH, CRITICAL
    property_id VARCHAR(16) REFERENCES properties(id),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    evidence JSONB,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 22. Periodic Reports
CREATE TABLE IF NOT EXISTS reports (
    id VARCHAR(64) PRIMARY KEY,
    report_type VARCHAR(64) NOT NULL, -- DAILY_OPERATIONS, REVENUE_ANALYSIS, RECONCILIATION_EXCEPTION, EXPENSE_AUDIT, BDE_INTELLIGENCE
    property_id VARCHAR(16),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    kpis JSONB,
    content TEXT NOT NULL,
    generated_by VARCHAR(64) DEFAULT 'ReportingAgent',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================================
-- PERFORMANCE INDEXES
-- =====================================================================
CREATE INDEX IF NOT EXISTS idx_res_prop ON reservations(property_id);
CREATE INDEX IF NOT EXISTS idx_res_dates ON reservations(arrival_date, departure_date);
CREATE INDEX IF NOT EXISTS idx_res_status ON reservations(status);
CREATE INDEX IF NOT EXISTS idx_inv_prop ON invoices(property_id);
CREATE INDEX IF NOT EXISTS idx_inv_dates ON invoices(invoice_date);
CREATE INDEX IF NOT EXISTS idx_inv_settled ON invoices(payment_settled);
CREATE INDEX IF NOT EXISTS idx_pmt_prop ON payments(property_id);
CREATE INDEX IF NOT EXISTS idx_pmt_res ON payments(reservation_id);
CREATE INDEX IF NOT EXISTS idx_chg_res ON charges(reservation_id);
CREATE INDEX IF NOT EXISTS idx_ota_prop ON ota_settlements(property_id);
CREATE INDEX IF NOT EXISTS idx_ota_scenario ON ota_settlements(reconciliation_scenario);
CREATE INDEX IF NOT EXISTS idx_exp_prop ON expenses(property_id);
CREATE INDEX IF NOT EXISTS idx_exp_date ON expenses(expense_date);
CREATE INDEX IF NOT EXISTS idx_comp_prop ON competitors(target_property_id);
CREATE INDEX IF NOT EXISTS idx_events_processed ON business_events(processed);
CREATE INDEX IF NOT EXISTS idx_alerts_resolved ON alerts(is_resolved);

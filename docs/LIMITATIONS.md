# System Limitations & Future Enhancements

## 1. Known Implementation Limitations

1. **Source Data Boundaries:**
   - The source dataset at `C:\Users\deves\Downloads\project` contains 100 reservations across 5 properties between August 2026 and October 2026.
   - Channel distribution in the raw PMS export is listed as `Direct`; OTA channel reconciliation scenarios are modeled through `ota_reservations_full.csv`.
   - Departmental expenses and competitor intelligence were absent from the source files and are provided via controlled synthetic seeds (`is_synthetic = TRUE`, random seed `42`).

2. **PMS Live API Connection:**
   - The `BookingCenterPMSAdapter` defines the provider integration interface and method signatures. Live network calls are mocked pending client production API credentials (`BOOKINGCENTER_API_KEY`, `BOOKINGCENTER_SITE_ID`).
   - The system operates out-of-the-box using the verified `CSVPMSAdapter`.

3. **Financial Gateway Compliance:**
   - The application audits and reconciles payment transactions. In compliance with PCI-DSS standards, the system does not store unencrypted primary account numbers (PAN) or execute irreversible bank transfers autonomously.

4. **Hardware & Infrastructure Footprint:**
   - While the college project synopsis outlines server-side enterprise training on NVIDIA B200 GPU infrastructure, the local execution runtime is optimized for standalone Windows/Linux workstations using deterministic Python/SQL inference and lightweight dense hash embeddings.

---

## 2. Future Architectural Enhancements

1. **Live PMS Webhook Listeners:** Implementing bidirectional webhook listeners for Apaleo, Mews, and BookingCenter to consume room check-in events in real-time.
2. **Automated OTA Dispute Filing:** Direct API integration with Booking.com Partner Hub and Expedia Partner Central to submit automated reconciliation discrepancy claims.
3. **Open Banking Bank-Feed Integration:** Direct connection to European Open Banking APIs (PSD2) to ingest live bank statements for automated three-way cash matching.
4. **Dynamic Price Pushing:** Enabling an authorized front-desk approval workflow where hotel managers can approve and dispatch BDE pricing recommendations directly to channel managers.

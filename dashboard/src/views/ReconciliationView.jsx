import React from "react";
import { Scale, AlertCircle, CheckCircle, Clock, RefreshCw, ArrowRight } from "lucide-react";

export default function ReconciliationView({ reconciliationData, onRunAudit, loading = false }) {
  if (!reconciliationData) {
    return <div style={{ padding: "40px", textAlign: "center", color: "var(--text-muted)" }}>Loading reconciliation ledger...</div>;
  }

  const otaExceptions = Array.isArray(reconciliationData.ota_exceptions) ? reconciliationData.ota_exceptions : [];
  const topInvoices = Array.isArray(reconciliationData.top_invoice_exceptions) ? reconciliationData.top_invoice_exceptions : [];
  const formatAmount = (value) => Number(value || 0).toFixed(2);

  return (
    <div style={{ padding: "28px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: "24px" }}>
        <div>
          <h2 style={{ fontSize: "1.45rem", fontWeight: 800, color: "#ffffff", letterSpacing: "-0.02em" }}>
            Financial Reconciliation & Audit Engine
          </h2>
          <p style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
            Automated multi-way matching across guest folio invoices, payment gateways, and OTA channel settlement remittances.
          </p>
        </div>

        <button
          onClick={onRunAudit}
          disabled={loading}
          className="btn btn-primary"
          style={{ fontSize: "0.82rem", padding: "8px 16px" }}
        >
          <RefreshCw size={16} className={loading ? "spin-animation" : ""} />
          <span>Execute Full Audit Run</span>
        </button>
      </div>

      {/* KPI Cards */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
        gap: "18px",
        marginBottom: "28px"
      }}>
        <div className="glass-card" style={{ padding: "18px" }}>
          <span style={{ fontSize: "0.76rem", color: "var(--text-muted)", fontWeight: 600 }}>Total Invoices Audited</span>
          <div style={{ fontSize: "1.6rem", fontWeight: 800, color: "#ffffff", marginTop: "4px" }}>
            {reconciliationData.total_invoices_audited || 0}
          </div>
          <span style={{ fontSize: "0.72rem", color: "var(--text-dim)" }}>
            {reconciliationData.fully_paid_count || 0} Fully Balanced Accounts
          </span>
        </div>

        <div className="glass-card" style={{ padding: "18px" }}>
          <span style={{ fontSize: "0.76rem", color: "var(--text-muted)", fontWeight: 600 }}>Partially Paid Invoices</span>
          <div style={{ fontSize: "1.6rem", fontWeight: 800, color: "var(--warning)", marginTop: "4px" }}>
            {reconciliationData.partially_paid_count || 0}
          </div>
          <span style={{ fontSize: "0.72rem", color: "var(--text-dim)" }}>
            Unsettled front-desk balances
          </span>
        </div>

        <div className="glass-card" style={{ padding: "18px" }}>
          <span style={{ fontSize: "0.76rem", color: "var(--text-muted)", fontWeight: 600 }}>Unbalanced Receivables</span>
          <div style={{ fontSize: "1.6rem", fontWeight: 800, color: "var(--danger)", marginTop: "4px" }}>
            €{reconciliationData.total_unbalanced_receivables?.toLocaleString() || "0"}
          </div>
          <span style={{ fontSize: "0.72rem", color: "var(--text-dim)" }}>
            Requires front-desk collection
          </span>
        </div>

        <div className="glass-card" style={{ padding: "18px" }}>
          <span style={{ fontSize: "0.76rem", color: "var(--text-muted)", fontWeight: 600 }}>OTA Settlement Exceptions</span>
          <div style={{ fontSize: "1.6rem", fontWeight: 800, color: "var(--accent-cyan)", marginTop: "4px" }}>
            {reconciliationData.ota_exceptions_count || 0}
          </div>
          <span style={{ fontSize: "0.72rem", color: "var(--text-dim)" }}>
            Channel payout discrepancies
          </span>
        </div>
      </div>

      {/* OTA Channel Remittance Audit Matrix */}
      <div className="glass-card" style={{ padding: "22px", marginBottom: "28px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
          <div>
            <h3 style={{ fontSize: "1.1rem", fontWeight: 700, color: "#ffffff" }}>
              OTA Channel Settlement Remittance Audit
            </h3>
            <p style={{ fontSize: "0.78rem", color: "var(--text-muted)" }}>
              Comparing OTA gross bookings against net bank remittances received (Booking.com, Expedia, Agoda, Airbnb)
            </p>
          </div>
          <span className="badge badge-primary">20 Channel Bookings Audited</span>
        </div>

        <div style={{ overflowX: "auto" }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Channel</th>
                <th>OTA Booking ID</th>
                <th>Scenario</th>
                <th>Gross Amount</th>
                <th>Expected Net</th>
                <th>Actual Bank Payout</th>
                <th>Discrepancy</th>
                <th>Recommended Action</th>
              </tr>
            </thead>
            <tbody>
              {otaExceptions.map((o) => (
                <tr key={o.settlement_id}>
                  <td style={{ fontWeight: 700, color: "#ffffff" }}>{o.channel_name}</td>
                  <td style={{ fontFamily: "var(--font-mono)", fontSize: "0.78rem", color: "var(--accent-cyan)" }}>
                    {o.ota_reservation_id}
                  </td>
                  <td>
                    <span className={`badge ${
                      o.scenario === "exact" ? "badge-success" :
                      o.scenario === "missing_settlement" ? "badge-danger" : "badge-warning"
                    }`}>
                      {o.scenario}
                    </span>
                  </td>
                  <td>€{formatAmount(o.gross_amount)}</td>
                  <td>€{formatAmount(o.expected_settlement)}</td>
                  <td style={{ fontWeight: 700, color: o.actual_settlement ? "#ffffff" : "var(--danger)" }}>
                    {o.actual_settlement !== null && o.actual_settlement !== undefined ? `€${formatAmount(o.actual_settlement)}` : "MISSING"}
                  </td>
                  <td style={{ fontWeight: 700, color: o.difference > 0 ? "var(--warning)" : (o.difference < 0 ? "var(--accent-cyan)" : "var(--success)") }}>
                    {Number(o.difference || 0) !== 0 ? `€${formatAmount(o.difference)}` : "€0.00"}
                  </td>
                  <td style={{ fontSize: "0.76rem", color: "var(--text-muted)", maxWidth: "300px" }}>
                    {o.recommended_action}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Top Invoice Discrepancies */}
      <div className="glass-card" style={{ padding: "22px" }}>
        <h3 style={{ fontSize: "1.1rem", fontWeight: 700, color: "#ffffff", marginBottom: "4px" }}>
          Unbalanced Guest Folio Exceptions
        </h3>
        <p style={{ fontSize: "0.78rem", color: "var(--text-muted)", marginBottom: "16px" }}>
          Discrepancies identified between issued guest tax invoices and recorded gateway settlements
        </p>

        <div style={{ overflowX: "auto" }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Invoice #</th>
                <th>Reservation ID</th>
                <th>Invoice Total</th>
                <th>Recorded Payments</th>
                <th>Unbalanced Amount</th>
                <th>Status</th>
                <th>Recommended Action</th>
              </tr>
            </thead>
            <tbody>
              {topInvoices.map((inv) => (
                <tr key={inv.invoice_id}>
                  <td style={{ fontFamily: "var(--font-mono)", fontSize: "0.8rem", fontWeight: 700, color: "#ffffff" }}>
                    {inv.invoice_number}
                  </td>
                  <td style={{ fontFamily: "var(--font-mono)", fontSize: "0.76rem", color: "var(--text-dim)" }}>
                    {inv.reservation_id}
                  </td>
                  <td>€{formatAmount(inv.invoice_total)}</td>
                  <td style={{ color: "var(--success)" }}>€{formatAmount(inv.payments_total)}</td>
                  <td style={{ fontWeight: 700, color: "var(--danger)" }}>€{formatAmount(inv.difference)}</td>
                  <td>
                    <span className="badge badge-warning">{inv.status}</span>
                  </td>
                  <td style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                    {inv.recommended_action}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

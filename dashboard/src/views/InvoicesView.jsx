import React, { useState } from "react";
import { Receipt, CreditCard, Search, CheckCircle, Clock } from "lucide-react";

export default function InvoicesView({ invoices = [], payments = [] }) {
  const [activeTab, setActiveTab] = useState("invoices");
  const [search, setSearch] = useState("");

  const filteredInvoices = invoices.filter((i) =>
    i.invoice_number.toLowerCase().includes(search.toLowerCase()) ||
    i.id.toLowerCase().includes(search.toLowerCase()) ||
    (i.reservation_id && i.reservation_id.toLowerCase().includes(search.toLowerCase()))
  );

  const filteredPayments = payments.filter((p) =>
    p.id.toLowerCase().includes(search.toLowerCase()) ||
    p.reservation_id.toLowerCase().includes(search.toLowerCase()) ||
    (p.transaction_reference && p.transaction_reference.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div style={{ padding: "28px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: "24px" }}>
        <div>
          <h2 style={{ fontSize: "1.45rem", fontWeight: 800, color: "#ffffff", letterSpacing: "-0.02em" }}>
            Invoices & Payment Transactions
          </h2>
          <p style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
            Statutory tax invoices and front-desk settlement transactions across PMS accounts.
          </p>
        </div>

        {/* Tab Switcher & Search */}
        <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
          <div style={{
            display: "flex",
            background: "rgba(255, 255, 255, 0.05)",
            borderRadius: "8px",
            padding: "3px",
            border: "1px solid var(--border)"
          }}>
            <button
              onClick={() => setActiveTab("invoices")}
              style={{
                padding: "6px 14px",
                border: "none",
                borderRadius: "6px",
                background: activeTab === "invoices" ? "var(--primary)" : "transparent",
                color: activeTab === "invoices" ? "#ffffff" : "var(--text-muted)",
                fontSize: "0.8rem",
                fontWeight: 600,
                cursor: "pointer"
              }}
            >
              Invoices ({invoices.length})
            </button>
            <button
              onClick={() => setActiveTab("payments")}
              style={{
                padding: "6px 14px",
                border: "none",
                borderRadius: "6px",
                background: activeTab === "payments" ? "var(--primary)" : "transparent",
                color: activeTab === "payments" ? "#ffffff" : "var(--text-muted)",
                fontSize: "0.8rem",
                fontWeight: 600,
                cursor: "pointer"
              }}
            >
              Payments ({payments.length})
            </button>
          </div>

          <div style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            background: "rgba(255, 255, 255, 0.05)",
            border: "1px solid var(--border)",
            borderRadius: "8px",
            padding: "6px 12px"
          }}>
            <Search size={16} color="var(--text-dim)" />
            <input
              type="text"
              placeholder="Search invoice/payment..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{
                background: "transparent",
                border: "none",
                color: "#ffffff",
                outline: "none",
                fontSize: "0.82rem"
              }}
            />
          </div>
        </div>
      </div>

      {activeTab === "invoices" ? (
        <div className="glass-card" style={{ padding: "16px", overflowX: "auto" }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Invoice #</th>
                <th>Property</th>
                <th>Reservation ID</th>
                <th>Invoice Date</th>
                <th>Total Gross</th>
                <th>Outstanding</th>
                <th>Settled</th>
                <th>Provenance</th>
              </tr>
            </thead>
            <tbody>
              {filteredInvoices.map((inv) => (
                <tr key={inv.id}>
                  <td style={{ fontFamily: "var(--font-mono)", fontSize: "0.82rem", fontWeight: 700, color: "#ffffff" }}>
                    {inv.invoice_number}
                  </td>
                  <td>
                    <span style={{ fontWeight: 700, color: "var(--accent-cyan)" }}>{inv.property_id}</span>
                  </td>
                  <td style={{ fontFamily: "var(--font-mono)", fontSize: "0.78rem", color: "var(--text-muted)" }}>
                    {inv.reservation_id || "N/A"}
                  </td>
                  <td>{inv.invoice_date}</td>
                  <td style={{ fontWeight: 700, color: "#ffffff" }}>
                    €{Number(inv.total_amount).toFixed(2)}
                  </td>
                  <td style={{ color: Number(inv.outstanding_balance) > 0 ? "var(--warning)" : "var(--text-muted)" }}>
                    €{Number(inv.outstanding_balance).toFixed(2)}
                  </td>
                  <td>
                    {inv.payment_settled ? (
                      <span className="badge badge-success"><CheckCircle size={10} /> Settled</span>
                    ) : (
                      <span className="badge badge-warning"><Clock size={10} /> Pending</span>
                    )}
                  </td>
                  <td>
                    <span className={`badge ${inv.is_synthetic ? "badge-cyan" : "badge-primary"}`} style={{ fontSize: "0.65rem" }}>
                      {inv.is_synthetic ? "Reconciliation Suite" : "Real Apaleo Export"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="glass-card" style={{ padding: "16px", overflowX: "auto" }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Payment ID</th>
                <th>Property</th>
                <th>Reservation ID</th>
                <th>Method</th>
                <th>Amount</th>
                <th>Payment Date</th>
                <th>Reference</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {filteredPayments.map((pmt) => (
                <tr key={pmt.id}>
                  <td style={{ fontFamily: "var(--font-mono)", fontSize: "0.8rem", color: "var(--accent-cyan)" }}>
                    {pmt.id}
                  </td>
                  <td>
                    <span style={{ fontWeight: 700, color: "#ffffff" }}>{pmt.property_id}</span>
                  </td>
                  <td style={{ fontFamily: "var(--font-mono)", fontSize: "0.78rem", color: "var(--text-muted)" }}>
                    {pmt.reservation_id}
                  </td>
                  <td>
                    <span className="badge badge-primary">{pmt.payment_method}</span>
                  </td>
                  <td style={{ fontWeight: 700, color: "var(--success)" }}>
                    {pmt.currency === "GBP" ? "£" : "€"}{Number(pmt.amount).toFixed(2)}
                  </td>
                  <td>{pmt.payment_date}</td>
                  <td style={{ fontFamily: "var(--font-mono)", fontSize: "0.75rem", color: "var(--text-dim)" }}>
                    {pmt.transaction_reference}
                  </td>
                  <td>
                    <span className={`badge ${pmt.status === "FULLY_PAID" ? "badge-success" : "badge-warning"}`}>
                      {pmt.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

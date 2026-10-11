import React, { useState } from "react";
import { Calendar, User, Search, Filter } from "lucide-react";

export default function ReservationsView({ reservations = [] }) {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");

  const filtered = reservations.filter((r) => {
    const matchesSearch =
      r.id.toLowerCase().includes(search.toLowerCase()) ||
      r.booking_id.toLowerCase().includes(search.toLowerCase()) ||
      r.property_id.toLowerCase().includes(search.toLowerCase());
    const matchesStatus = statusFilter ? r.status === statusFilter : true;
    return matchesSearch && matchesStatus;
  });

  const getStatusBadge = (status) => {
    switch (status) {
      case "InHouse":
        return <span className="badge badge-success">In-House</span>;
      case "CheckedOut":
        return <span className="badge badge-primary">Checked-Out</span>;
      case "Confirmed":
        return <span className="badge badge-cyan">Confirmed</span>;
      default:
        return <span className="badge badge-warning">{status}</span>;
    }
  };

  return (
    <div style={{ padding: "28px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: "24px" }}>
        <div>
          <h2 style={{ fontSize: "1.45rem", fontWeight: 800, color: "#ffffff", letterSpacing: "-0.02em" }}>
            Reservations Ledger ({filtered.length} Bookings)
          </h2>
          <p style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
            Operational PMS stay records, arrival dates, and folio billing balances.
          </p>
        </div>

        {/* Filters */}
        <div style={{ display: "flex", gap: "12px" }}>
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
              placeholder="Search ID, booking..."
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

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            style={{
              background: "rgba(255, 255, 255, 0.05)",
              border: "1px solid var(--border)",
              color: "#ffffff",
              borderRadius: "8px",
              padding: "6px 12px",
              fontSize: "0.82rem",
              outline: "none"
            }}
          >
            <option value="">All Statuses</option>
            <option value="InHouse">In-House</option>
            <option value="Confirmed">Confirmed</option>
            <option value="CheckedOut">Checked-Out</option>
          </select>
        </div>
      </div>

      <div className="glass-card" style={{ padding: "16px", overflowX: "auto" }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Reservation ID</th>
              <th>Property</th>
              <th>Arrival</th>
              <th>Departure</th>
              <th>Status</th>
              <th>Adults</th>
              <th>Gross Amount</th>
              <th>Balance</th>
              <th>Guarantee</th>
              <th>Channel</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((r) => (
              <tr key={r.id}>
                <td style={{ fontFamily: "var(--font-mono)", fontSize: "0.8rem", color: "var(--accent-cyan)" }}>
                  {r.id}
                  <div style={{ color: "var(--text-dim)", fontSize: "0.7rem" }}>Booking: {r.booking_id}</div>
                </td>
                <td>
                  <span style={{ fontWeight: 700, color: "#ffffff" }}>{r.property_id}</span>
                </td>
                <td>{new Date(r.arrival_date).toLocaleDateString()}</td>
                <td>{new Date(r.departure_date).toLocaleDateString()}</td>
                <td>{getStatusBadge(r.status)}</td>
                <td>{r.adults}</td>
                <td style={{ fontWeight: 700, color: "#ffffff" }}>
                  €{Number(r.total_gross_amount).toFixed(2)}
                </td>
                <td style={{ color: Number(r.balance) !== 0 ? "var(--warning)" : "var(--text-muted)" }}>
                  €{Number(r.balance).toFixed(2)}
                </td>
                <td>
                  <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
                    {r.guarantee_type}
                  </span>
                </td>
                <td>
                  <span className="badge badge-primary">{r.channel_code}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

import React from "react";
import {
  TrendingUp,
  DollarSign,
  CreditCard,
  AlertTriangle,
  BedDouble,
  BarChart3,
  ArrowUpRight,
  ShieldAlert,
  Building,
  CheckCircle2
} from "lucide-react";

export default function ExecutiveOverview({
  kpis,
  comparison = [],
  alerts = [],
  onResolveAlert,
  onNavigate
}) {
  if (!kpis) {
    return (
      <div style={{ padding: "40px", textAlign: "center", color: "var(--text-muted)" }}>
        Loading executive metrics...
      </div>
    );
  }

  const kpiCards = [
    {
      title: "Booked Revenue",
      value: `€${kpis.booked_revenue?.toLocaleString() || "0"}`,
      sub: `${kpis.reservations_count} Total Reservations`,
      icon: TrendingUp,
      color: "var(--primary)"
    },
    {
      title: "Collected Revenue",
      value: `€${kpis.collected_revenue?.toLocaleString() || "0"}`,
      sub: "Settled Payments & Remittances",
      icon: DollarSign,
      color: "var(--success)"
    },
    {
      title: "Outstanding Receivables",
      value: `€${kpis.outstanding_receivables?.toLocaleString() || "0"}`,
      sub: `${kpis.unresolved_reconciliation_exceptions || 0} Audit Exceptions`,
      icon: CreditCard,
      color: "var(--warning)"
    },
    {
      title: "Net Operating Income (NOI)",
      value: `€${kpis.net_operating_income?.toLocaleString() || "0"}`,
      sub: `Expenses: €${kpis.total_expenses?.toLocaleString() || "0"}`,
      icon: BarChart3,
      color: kpis.net_operating_income >= 0 ? "var(--success)" : "var(--danger)"
    },
    {
      title: "Occupancy Rate",
      value: `${kpis.occupancy_rate_pct || 0}%`,
      sub: `${kpis.total_rooms || 99} Physical Units`,
      icon: BedDouble,
      color: "var(--accent-cyan)"
    },
    {
      title: "ADR / RevPAR",
      value: `€${kpis.adr || 0} / €${kpis.revpar || 0}`,
      sub: "Average Yield per Available Night",
      icon: ArrowUpRight,
      color: "#a855f7"
    }
  ];

  return (
    <div style={{ padding: "28px" }}>
      {/* Title */}
      <div style={{ marginBottom: "24px" }}>
        <h2 style={{ fontSize: "1.45rem", fontWeight: 800, color: "#ffffff", letterSpacing: "-0.02em" }}>
          Executive Performance Overview
        </h2>
        <p style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
          Consolidated Property Management System (PMS) operations and fintech treasury synchronization.
        </p>
      </div>

      {/* KPI Cards Grid */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
        gap: "18px",
        marginBottom: "28px"
      }}>
        {kpiCards.map((k, idx) => {
          const Icon = k.icon;
          return (
            <div key={idx} className="glass-card" style={{ padding: "20px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                <span style={{ fontSize: "0.8rem", fontWeight: 600, color: "var(--text-muted)" }}>
                  {k.title}
                </span>
                <div style={{
                  padding: "8px",
                  borderRadius: "8px",
                  background: "rgba(255, 255, 255, 0.04)",
                  color: k.color
                }}>
                  <Icon size={18} />
                </div>
              </div>
              <div style={{ fontSize: "1.6rem", fontWeight: 800, color: "#ffffff", marginBottom: "4px" }}>
                {k.value}
              </div>
              <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>
                {k.sub}
              </div>
            </div>
          );
        })}
      </div>

      {/* Two Column Layout: Multi-Property Performance & Operational Alerts */}
      <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: "22px" }}>
        {/* Left: Multi-Property Synchronization Matrix */}
        <div className="glass-card" style={{ padding: "22px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
            <div>
              <h3 style={{ fontSize: "1.05rem", fontWeight: 700, color: "#ffffff" }}>
                Multi-Property Consolidated Matrix
              </h3>
              <p style={{ fontSize: "0.78rem", color: "var(--text-muted)" }}>
                Treasury performance across Berlin, London, Munich, Paris, and Vienna
              </p>
            </div>
            <button
              onClick={() => onNavigate("properties")}
              className="btn btn-secondary"
              style={{ fontSize: "0.76rem", padding: "6px 12px" }}
            >
              View All Properties
            </button>
          </div>

          <div style={{ overflowX: "auto" }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Property</th>
                  <th>City</th>
                  <th>Occupancy</th>
                  <th>Booked Rev</th>
                  <th>Collected</th>
                  <th>Expenses</th>
                  <th>ADR</th>
                  <th>Exceptions</th>
                </tr>
              </thead>
              <tbody>
                {comparison.map((p) => (
                  <tr key={p.property_id}>
                    <td>
                      <span style={{ fontWeight: 700, color: "#ffffff" }}>{p.property_id}</span>
                      <div style={{ fontSize: "0.72rem", color: "var(--text-dim)" }}>{p.property_name}</div>
                    </td>
                    <td>{p.city}</td>
                    <td>
                      <span style={{ fontWeight: 600, color: p.occupancy_rate_pct > 60 ? "var(--success)" : "var(--warning)" }}>
                        {p.occupancy_rate_pct}%
                      </span>
                    </td>
                    <td>€{p.booked_revenue?.toLocaleString()}</td>
                    <td style={{ color: "var(--success)" }}>€{p.collected_revenue?.toLocaleString()}</td>
                    <td style={{ color: "var(--text-muted)" }}>€{p.total_expenses?.toLocaleString()}</td>
                    <td>€{p.adr}</td>
                    <td>
                      {p.unresolved_reconciliation > 0 ? (
                        <span className="badge badge-warning">{p.unresolved_reconciliation} OTA</span>
                      ) : (
                        <span className="badge badge-success">Balanced</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right: Active Operational Alerts Widget */}
        <div className="glass-card" style={{ padding: "22px" }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "16px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <ShieldAlert size={18} color="var(--danger)" />
              <h3 style={{ fontSize: "1.05rem", fontWeight: 700, color: "#ffffff" }}>
                Active Alerts ({alerts.length})
              </h3>
            </div>
            <span className="badge badge-danger">Requires Action</span>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "12px", maxHeight: "380px", overflowY: "auto" }}>
            {alerts.length === 0 ? (
              <div style={{ padding: "30px 10px", textAlign: "center", color: "var(--text-dim)", fontSize: "0.85rem" }}>
                <CheckCircle2 size={32} color="var(--success)" style={{ margin: "0 auto 8px" }} />
                No pending critical alerts.
              </div>
            ) : (
              alerts.slice(0, 5).map((a) => (
                <div key={a.id} style={{
                  padding: "12px",
                  borderRadius: "8px",
                  background: "rgba(255, 255, 255, 0.03)",
                  border: "1px solid rgba(239, 68, 68, 0.2)"
                }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "4px" }}>
                    <span style={{ fontSize: "0.82rem", fontWeight: 700, color: "#ffffff" }}>
                      {a.title}
                    </span>
                    <span className={`badge ${a.severity === "CRITICAL" ? "badge-danger" : "badge-warning"}`}>
                      {a.severity}
                    </span>
                  </div>
                  <p style={{ fontSize: "0.74rem", color: "var(--text-muted)", marginBottom: "8px" }}>
                    {a.message}
                  </p>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <span style={{ fontSize: "0.68rem", color: "var(--text-dim)" }}>
                      {a.property_id || "All"}
                    </span>
                    <button
                      onClick={() => onResolveAlert(a.id)}
                      className="btn btn-secondary"
                      style={{ fontSize: "0.68rem", padding: "3px 8px" }}
                    >
                      Acknowledge
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

import React from "react";
import { TrendingUp, BarChart2, DollarSign, ArrowUpRight, ShieldCheck, Activity } from "lucide-react";

export default function RevenueView({ revenueData, kpis }) {
  if (!revenueData || !kpis) {
    return <div style={{ padding: "40px", textAlign: "center", color: "var(--text-muted)" }}>Loading revenue analytics...</div>;
  }

  const timeSeries = revenueData.time_series || [];
  const forecast = revenueData.forecast?.forecast || [];

  return (
    <div style={{ padding: "28px" }}>
      <div style={{ marginBottom: "24px" }}>
        <h2 style={{ fontSize: "1.45rem", fontWeight: 800, color: "#ffffff", letterSpacing: "-0.02em" }}>
          Revenue & Yield Analytics
        </h2>
        <p style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
          Strict decomposition of Booked, Invoiced, and Collected revenues alongside statistical yield forecasting.
        </p>
      </div>

      {/* Revenue Decomposition Metric Cards */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(230px, 1fr))",
        gap: "18px",
        marginBottom: "28px"
      }}>
        <div className="glass-card" style={{ padding: "18px" }}>
          <span style={{ fontSize: "0.76rem", fontWeight: 600, color: "var(--text-muted)" }}>Booked Revenue</span>
          <div style={{ fontSize: "1.5rem", fontWeight: 800, color: "#ffffff", marginTop: "4px" }}>
            €{kpis.booked_revenue?.toLocaleString()}
          </div>
          <p style={{ fontSize: "0.72rem", color: "var(--text-dim)", marginTop: "4px" }}>
            Contracted stay amounts
          </p>
        </div>

        <div className="glass-card" style={{ padding: "18px" }}>
          <span style={{ fontSize: "0.76rem", fontWeight: 600, color: "var(--text-muted)" }}>Invoiced Revenue</span>
          <div style={{ fontSize: "1.5rem", fontWeight: 800, color: "var(--primary)", marginTop: "4px" }}>
            €{kpis.invoiced_revenue?.toLocaleString()}
          </div>
          <p style={{ fontSize: "0.72rem", color: "var(--text-dim)", marginTop: "4px" }}>
            Statutory issued invoices
          </p>
        </div>

        <div className="glass-card" style={{ padding: "18px" }}>
          <span style={{ fontSize: "0.76rem", fontWeight: 600, color: "var(--text-muted)" }}>Collected Remittances</span>
          <div style={{ fontSize: "1.5rem", fontWeight: 800, color: "var(--success)", marginTop: "4px" }}>
            €{kpis.collected_revenue?.toLocaleString()}
          </div>
          <p style={{ fontSize: "0.72rem", color: "var(--text-dim)", marginTop: "4px" }}>
            Bank & card gateway settled
          </p>
        </div>

        <div className="glass-card" style={{ padding: "18px" }}>
          <span style={{ fontSize: "0.76rem", fontWeight: 600, color: "var(--text-muted)" }}>Outstanding Receivables</span>
          <div style={{ fontSize: "1.5rem", fontWeight: 800, color: "var(--warning)", marginTop: "4px" }}>
            €{kpis.outstanding_receivables?.toLocaleString()}
          </div>
          <p style={{ fontSize: "0.72rem", color: "var(--text-dim)", marginTop: "4px" }}>
            Unsettled debtor balances
          </p>
        </div>
      </div>

      {/* Two Columns: Daily Revenue Trend & Forecasting */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "22px" }}>
        {/* Left: Historical Daily Revenue */}
        <div className="glass-card" style={{ padding: "22px" }}>
          <h3 style={{ fontSize: "1.05rem", fontWeight: 700, color: "#ffffff", marginBottom: "4px" }}>
            Historical Daily Booked Velocity
          </h3>
          <p style={{ fontSize: "0.76rem", color: "var(--text-muted)", marginBottom: "16px" }}>
            Daily revenue bookings across the active operational horizon
          </p>

          <div style={{ maxHeight: "360px", overflowY: "auto" }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Bookings</th>
                  <th>Revenue</th>
                </tr>
              </thead>
              <tbody>
                {timeSeries.slice(-15).map((ts) => (
                  <tr key={ts.date}>
                    <td style={{ fontFamily: "var(--font-mono)", fontSize: "0.8rem" }}>{ts.date}</td>
                    <td>{ts.reservations} stays</td>
                    <td style={{ fontWeight: 700, color: "#ffffff" }}>€{ts.booked_revenue.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right: 14-Day Statistical Revenue Forecast */}
        <div className="glass-card" style={{ padding: "22px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "4px" }}>
            <div>
              <h3 style={{ fontSize: "1.05rem", fontWeight: 700, color: "#ffffff" }}>
                14-Day Revenue Forecast
              </h3>
              <p style={{ fontSize: "0.76rem", color: "var(--text-muted)" }}>
                Seasonal Moving Average with Polyfit Drift Projection
              </p>
            </div>
            <span className="badge badge-primary">Model Projection</span>
          </div>

          <div style={{ marginTop: "16px", maxHeight: "360px", overflowY: "auto" }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Projected Date</th>
                  <th>Expected Revenue</th>
                  <th>Lower Bound</th>
                  <th>Upper Bound</th>
                </tr>
              </thead>
              <tbody>
                {forecast.map((f) => (
                  <tr key={f.date}>
                    <td style={{ fontFamily: "var(--font-mono)", fontSize: "0.8rem", color: "var(--accent-cyan)" }}>
                      {f.date}
                    </td>
                    <td style={{ fontWeight: 700, color: "#ffffff" }}>
                      €{f.predicted_revenue.toFixed(2)}
                    </td>
                    <td style={{ color: "var(--text-dim)" }}>
                      €{f.lower_bound.toFixed(2)}
                    </td>
                    <td style={{ color: "var(--success)" }}>
                      €{f.upper_bound.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

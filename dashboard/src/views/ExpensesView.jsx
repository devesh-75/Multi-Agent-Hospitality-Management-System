import React from "react";
import { Wallet, AlertTriangle, TrendingDown, Layers, Building, RefreshCw } from "lucide-react";

export default function ExpensesView({ expensesData, onRunAudit, loading = false }) {
  if (!expensesData) {
    return <div style={{ padding: "40px", textAlign: "center", color: "var(--text-muted)" }}>Loading operating expenses...</div>;
  }

  const breakdown = expensesData.breakdown || {};
  const byCat = breakdown.by_category || {};
  const byCatPct = breakdown.category_percentages || {};
  const anomalies = expensesData.anomalies || [];
  const recommendations = expensesData.recommendations || [];

  return (
    <div style={{ padding: "28px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: "24px" }}>
        <div>
          <h2 style={{ fontSize: "1.45rem", fontWeight: 800, color: "#ffffff", letterSpacing: "-0.02em" }}>
            Operational Expense Tracking & Auditing
          </h2>
          <p style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
            Departmental spending breakdowns, statistical z-score outlier detection, and vendor spend auditing.
          </p>
        </div>

        <button
          onClick={onRunAudit}
          disabled={loading}
          className="btn btn-primary"
          style={{ fontSize: "0.82rem", padding: "8px 16px" }}
        >
          <RefreshCw size={16} className={loading ? "spin-animation" : ""} />
          <span>Execute Expense Audit</span>
        </button>
      </div>

      {/* Top Metric Cards */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
        gap: "18px",
        marginBottom: "28px"
      }}>
        <div className="glass-card" style={{ padding: "18px" }}>
          <span style={{ fontSize: "0.76rem", color: "var(--text-muted)", fontWeight: 600 }}>Total Operating Expenses</span>
          <div style={{ fontSize: "1.6rem", fontWeight: 800, color: "#ffffff", marginTop: "4px" }}>
            €{expensesData.total_expenses?.toLocaleString() || "0"}
          </div>
          <span style={{ fontSize: "0.72rem", color: "var(--text-dim)" }}>
            August - October 2026 Fiscal Window
          </span>
        </div>

        <div className="glass-card" style={{ padding: "18px" }}>
          <span style={{ fontSize: "0.76rem", color: "var(--text-muted)", fontWeight: 600 }}>Statistical Anomalies</span>
          <div style={{ fontSize: "1.6rem", fontWeight: 800, color: anomalies.length > 0 ? "var(--danger)" : "var(--success)", marginTop: "4px" }}>
            {anomalies.length}
          </div>
          <span style={{ fontSize: "0.72rem", color: "var(--text-dim)" }}>
            Z-score &gt; 2.0σ threshold
          </span>
        </div>

        <div className="glass-card" style={{ padding: "18px" }}>
          <span style={{ fontSize: "0.76rem", color: "var(--text-muted)", fontWeight: 600 }}>Primary Spend Category</span>
          <div style={{ fontSize: "1.4rem", fontWeight: 800, color: "var(--accent-cyan)", marginTop: "4px" }}>
            Payroll & Personnel
          </div>
          <span style={{ fontSize: "0.72rem", color: "var(--text-dim)" }}>
            Fixed operational overhead
          </span>
        </div>
      </div>

      {/* Categorical Breakdown Matrix & Statistical Anomalies */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "22px", marginBottom: "28px" }}>
        {/* Departmental Spend Categories */}
        <div className="glass-card" style={{ padding: "22px" }}>
          <h3 style={{ fontSize: "1.05rem", fontWeight: 700, color: "#ffffff", marginBottom: "4px" }}>
            Departmental Cost Distribution
          </h3>
          <p style={{ fontSize: "0.76rem", color: "var(--text-muted)", marginBottom: "16px" }}>
            Expense allocations across core hotel operational centers
          </p>

          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            {Object.entries(byCat).map(([cat, amt]) => {
              const pct = byCatPct[cat] || 0;
              return (
                <div key={cat} style={{ background: "rgba(255, 255, 255, 0.02)", padding: "10px 14px", borderRadius: "8px" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                    <span style={{ fontSize: "0.82rem", fontWeight: 600, color: "#ffffff" }}>{cat}</span>
                    <span style={{ fontSize: "0.82rem", fontWeight: 700, color: "var(--text-main)" }}>
                      €{amt.toLocaleString()} ({pct}%)
                    </span>
                  </div>
                  {/* Progress Bar */}
                  <div style={{ width: "100%", height: "6px", background: "rgba(255, 255, 255, 0.06)", borderRadius: "3px", overflow: "hidden" }}>
                    <div style={{
                      width: `${pct}%`,
                      height: "100%",
                      background: cat === "Payroll" ? "var(--primary)" : (cat === "Utilities" ? "var(--warning)" : "var(--accent-cyan)")
                    }} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Statistical Anomaly Audit Log */}
        <div className="glass-card" style={{ padding: "22px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "16px" }}>
            <div>
              <h3 style={{ fontSize: "1.05rem", fontWeight: 700, color: "#ffffff" }}>
                Statistical Spend Outliers (Z-Score &gt; 2.0)
              </h3>
              <p style={{ fontSize: "0.76rem", color: "var(--text-muted)" }}>
                Unexpected spikes verified by the Expense Tracking Agent
              </p>
            </div>
            <span className="badge badge-danger">High Severity</span>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "12px", maxHeight: "380px", overflowY: "auto" }}>
            {anomalies.map((a) => (
              <div key={a.expense_id} style={{
                padding: "14px",
                borderRadius: "10px",
                background: "rgba(239, 68, 68, 0.05)",
                border: "1px solid rgba(239, 68, 68, 0.25)"
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                  <span style={{ fontSize: "0.85rem", fontWeight: 700, color: "#ffffff" }}>
                    {a.vendor}
                  </span>
                  <span style={{ fontSize: "0.85rem", fontWeight: 800, color: "var(--danger)" }}>
                    €{a.amount.toFixed(2)}
                  </span>
                </div>
                <p style={{ fontSize: "0.76rem", color: "var(--text-muted)", marginBottom: "6px" }}>
                  {a.description}
                </p>
                <div style={{ fontSize: "0.72rem", color: "var(--warning)", fontWeight: 600, marginBottom: "8px" }}>
                  {a.evidence}
                </div>
                <div style={{ fontSize: "0.72rem", color: "var(--text-dim)", borderTop: "1px solid rgba(255, 255, 255, 0.05)", paddingTop: "6px" }}>
                  <strong>Next Action:</strong> {a.recommended_action}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

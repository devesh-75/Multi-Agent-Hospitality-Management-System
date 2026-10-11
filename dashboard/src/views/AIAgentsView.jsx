import React, { useState } from "react";
import { Bot, Play, CheckCircle2, Clock, Layers, Sparkles, RefreshCw } from "lucide-react";

export default function AIAgentsView({
  onRunAudit,
  agentRuns = [],
  lastResult = null,
  loading = false,
  selectedProperty
}) {
  const [selectedAgent, setSelectedAgent] = useState("all");

  const handleRun = () => {
    onRunAudit(selectedAgent);
  };

  return (
    <div style={{ padding: "28px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: "24px" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
            <span className="badge badge-primary">LangGraph Framework</span>
            <span style={{ fontSize: "0.78rem", color: "var(--accent-cyan)", fontWeight: 600 }}>Multi-Agent Orchestration</span>
          </div>
          <h2 style={{ fontSize: "1.45rem", fontWeight: 800, color: "#ffffff", letterSpacing: "-0.02em" }}>
            Specialized AI Agent Framework
          </h2>
          <p style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
            Coordinated workflow of deterministic analytical agents: Reconciliation, Expense, Revenue, Reporting, and BDE.
          </p>
        </div>

        {/* Agent Selector & Run Button */}
        <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
          <select
            value={selectedAgent}
            onChange={(e) => setSelectedAgent(e.target.value)}
            style={{
              background: "rgba(255, 255, 255, 0.05)",
              border: "1px solid var(--border)",
              color: "#ffffff",
              borderRadius: "8px",
              padding: "8px 14px",
              fontSize: "0.82rem",
              fontWeight: 600,
              outline: "none"
            }}
          >
            <option value="all">Full Workflow (All 5 Agents)</option>
            <option value="reconciliation">Reconciliation Agent</option>
            <option value="expense">Expense Tracking Agent</option>
            <option value="revenue">Revenue Insight Agent</option>
            <option value="reporting">Reporting Agent</option>
            <option value="bde">BDE Competitive Intelligence Agent</option>
          </select>

          <button
            onClick={handleRun}
            disabled={loading}
            className="btn btn-primary"
            style={{ padding: "8px 18px" }}
          >
            <Play size={16} />
            <span>{loading ? "Running Graph..." : "Execute Workflow"}</span>
          </button>
        </div>
      </div>

      {/* Agents Architecture Overview Cards */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))",
        gap: "16px",
        marginBottom: "28px"
      }}>
        {[
          { name: "Reconciliation Agent", role: "Audits Invoices & OTA settlements", status: "Active" },
          { name: "Expense Agent", role: "Z-score spend outlier detection", status: "Active" },
          { name: "Revenue Agent", role: "ADR, RevPAR & yield forecasting", status: "Active" },
          { name: "Reporting Agent", role: "Generates executive audit briefs", status: "Active" },
          { name: "BDE Agent", role: "Competitor intelligence & SWOT", status: "Active" },
        ].map((ag, i) => (
          <div key={i} className="glass-card" style={{ padding: "16px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
              <Bot size={18} color="var(--primary)" />
              <span className="badge badge-success" style={{ fontSize: "0.62rem" }}>{ag.status}</span>
            </div>
            <h4 style={{ fontSize: "0.88rem", fontWeight: 700, color: "#ffffff" }}>{ag.name}</h4>
            <p style={{ fontSize: "0.72rem", color: "var(--text-muted)", marginTop: "4px" }}>{ag.role}</p>
          </div>
        ))}
      </div>

      {/* Results & Execution Log */}
      <div style={{ display: "grid", gridTemplateColumns: "1.5fr 1fr", gap: "22px" }}>
        {/* Left: Latest Multi-Agent Output Brief */}
        <div className="glass-card" style={{ padding: "24px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
            <h3 style={{ fontSize: "1.1rem", fontWeight: 700, color: "#ffffff" }}>
              Synthesized Multi-Agent Output
            </h3>
            {lastResult && (
              <span className="badge badge-primary">
                Executed in {lastResult.execution_time_ms} ms
              </span>
            )}
          </div>

          {lastResult && lastResult.final_response ? (
            <div style={{
              background: "rgba(0, 0, 0, 0.2)",
              borderRadius: "10px",
              padding: "20px",
              fontSize: "0.86rem",
              lineHeight: 1.6,
              whiteSpace: "pre-line",
              maxHeight: "450px",
              overflowY: "auto",
              color: "#e2e8f0"
            }}>
              {lastResult.final_response}
            </div>
          ) : (
            <div style={{ padding: "40px", textAlign: "center", color: "var(--text-dim)", fontSize: "0.85rem" }}>
              Click <strong>Execute Workflow</strong> above to run the LangGraph pipeline across Property Management System ledgers.
            </div>
          )}
        </div>

        {/* Right: Historical Agent Execution Log */}
        <div className="glass-card" style={{ padding: "24px" }}>
          <h3 style={{ fontSize: "1.1rem", fontWeight: 700, color: "#ffffff", marginBottom: "4px" }}>
            Agent Execution Runs ({agentRuns.length})
          </h3>
          <p style={{ fontSize: "0.76rem", color: "var(--text-muted)", marginBottom: "16px" }}>
            Immutable audit trail of previous pipeline invocations
          </p>

          <div style={{ display: "flex", flexDirection: "column", gap: "10px", maxHeight: "420px", overflowY: "auto" }}>
            {agentRuns.map((r) => (
              <div key={r.id} style={{
                background: "rgba(255, 255, 255, 0.02)",
                padding: "12px",
                borderRadius: "8px",
                border: "1px solid var(--border)",
                fontSize: "0.78rem"
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                  <span style={{ fontWeight: 700, color: "#ffffff" }}>{r.agent_name}</span>
                  <span className="badge badge-success" style={{ fontSize: "0.62rem" }}>{r.status}</span>
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", color: "var(--text-dim)", fontSize: "0.72rem" }}>
                  <span>Scope: {r.property_id || "ALL"}</span>
                  <span>Duration: {r.execution_time_ms} ms</span>
                </div>
                <div style={{ fontSize: "0.68rem", color: "var(--text-muted)", marginTop: "4px" }}>
                  {r.started_at ? new Date(r.started_at).toLocaleString() : ""}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

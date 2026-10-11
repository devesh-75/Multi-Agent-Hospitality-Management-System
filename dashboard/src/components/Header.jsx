import React from "react";
import { RefreshCw, Play, Building, Activity, Sparkles } from "lucide-react";

export default function Header({
  selectedProperty,
  setSelectedProperty,
  properties = [],
  onRefresh,
  onRunAudit,
  backendStatus = "healthy",
  loading = false
}) {
  return (
    <header style={{
      height: "70px",
      borderBottom: "1px solid var(--border)",
      background: "rgba(15, 20, 32, 0.75)",
      backdropFilter: "blur(12px)",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "0 28px",
      position: "sticky",
      top: 0,
      zIndex: 40
    }}>
      {/* Left: Property Filter */}
      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "var(--text-muted)", fontSize: "0.85rem" }}>
          <Building size={18} color="var(--primary)" />
          <span style={{ fontWeight: 600 }}>Active Property Scope:</span>
        </div>
        <select
          value={selectedProperty}
          onChange={(e) => setSelectedProperty(e.target.value)}
          style={{
            background: "rgba(255, 255, 255, 0.06)",
            color: "#ffffff",
            border: "1px solid var(--border)",
            borderRadius: "8px",
            padding: "8px 14px",
            fontSize: "0.86rem",
            fontWeight: 600,
            cursor: "pointer",
            outline: "none"
          }}
        >
          <option value="">Consolidated Network (All 5 Properties)</option>
          {properties.map((p) => (
            <option key={p.id} value={p.id}>
              {p.id} - {p.name} ({p.country_code})
            </option>
          ))}
        </select>
      </div>

      {/* Right Actions & Health */}
      <div style={{ display: "flex", alignItems: "center", gap: "14px" }}>
        {/* Backend Status Badge */}
        <div style={{
          display: "flex",
          alignItems: "center",
          gap: "8px",
          padding: "6px 12px",
          borderRadius: "8px",
          background: backendStatus === "healthy" ? "rgba(16, 185, 129, 0.1)" : "rgba(239, 68, 68, 0.1)",
          border: `1px solid ${backendStatus === "healthy" ? "rgba(16, 185, 129, 0.25)" : "rgba(239, 68, 68, 0.25)"}`,
          fontSize: "0.78rem"
        }}>
          <div className="live-indicator" style={{
            backgroundColor: backendStatus === "healthy" ? "#10b981" : "#ef4444",
            boxShadow: `0 0 8px ${backendStatus === "healthy" ? "#10b981" : "#ef4444"}`
          }} />
          <span style={{ fontWeight: 600, color: backendStatus === "healthy" ? "#34d399" : "#f87171" }}>
            Backend {backendStatus === "healthy" ? "Online" : "Disconnected"}
          </span>
        </div>

        {/* Trigger Audit Button */}
        <button
          onClick={onRunAudit}
          disabled={loading}
          className="btn btn-primary"
          style={{ fontSize: "0.82rem", padding: "7px 14px" }}
        >
          <Sparkles size={16} />
          <span>Execute Multi-Agent Audit</span>
        </button>

        {/* Refresh Button */}
        <button
          onClick={onRefresh}
          disabled={loading}
          className="btn btn-secondary"
          style={{ padding: "7px 12px" }}
          title="Refresh dataset from backend"
        >
          <RefreshCw size={16} className={loading ? "spin-animation" : ""} />
        </button>
      </div>
    </header>
  );
}

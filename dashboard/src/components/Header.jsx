import React, { useState } from "react";
import { RefreshCw, Building, ChevronDown, MoreHorizontal, CalendarDays, Download, Sun, Moon } from "lucide-react";

const titles = {
  overview: "Executive Overview",
  properties: "Properties & Rooms",
  reservations: "Reservations & Occupancy",
  revenue: "Revenue Analytics",
  invoices: "Invoices & Payments",
  reconciliation: "Reconciliation",
  expenses: "Expense Tracking",
  agents: "AI Multi-Agent Layer",
  bde: "Business Development",
  reports: "Operational Reports",
  data_quality: "Data Quality & Lineage",
  ask_ai: "Ask AI Assistant"
};

export default function Header({ selectedProperty, setSelectedProperty, properties = [], onRefresh, onRunAudit, onExport, backendStatus = "healthy", loading = false, currentView = "overview", darkTheme = false, onToggleTheme }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [mode, setMode] = useState("Desktop");
  const [environment, setEnvironment] = useState("Production");
  return (
    <>
      <header style={{ height: "64px", borderBottom: "1px solid var(--border)", background: "var(--bg-panel)", display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 24px", position: "sticky", top: 0, zIndex: 40 }}>
        <div style={{ display: "flex", alignItems: "center", gap: "12px", minWidth: "280px" }}>
          <div style={{ position: "relative" }}>
            <button type="button" className="btn btn-secondary" onClick={() => setSelectedProperty(selectedProperty ? "" : (properties[0]?.id || ""))} aria-label="Toggle property scope" style={{ padding: "6px 10px" }}>
              <Building size={15} color="var(--primary)" />
              <span>{selectedProperty || "All properties"}</span>
              <ChevronDown size={14} color="var(--text-dim)" />
            </button>
          </div>
          <select value={selectedProperty} onChange={(event) => setSelectedProperty(event.target.value)} aria-label="Global property selector" style={{ maxWidth: "170px", padding: "7px 8px", border: "1px solid var(--border)", borderRadius: "6px", background: "var(--bg-panel)" }}>
            <option value="">All properties</option>
            {properties.map((property) => <option key={property.id} value={property.id}>{property.id} - {property.name}</option>)}
          </select>
        </div>
        <h1 style={{ margin: 0, fontSize: "16px", fontWeight: 650, color: "var(--text-main)" }}>{titles[currentView] || "Hospitality Operations"}</h1>
        <div style={{ minWidth: "280px", display: "flex", alignItems: "center", justifyContent: "flex-end", gap: "14px" }}>
          <span style={{ fontSize: "12px", color: backendStatus === "healthy" ? "var(--success)" : "var(--danger)" }}>Backend {backendStatus === "healthy" ? "online" : "degraded"}</span>
          <button type="button" className="btn btn-secondary" onClick={() => setMenuOpen((open) => !open)} aria-label="Open dashboard actions" aria-expanded={menuOpen} style={{ padding: "7px" }}><MoreHorizontal size={17} /></button>
          {menuOpen && <div style={{ position: "absolute", top: "52px", right: "20px", width: "170px", padding: "6px", border: "1px solid var(--border)", borderRadius: "6px", background: "var(--bg-panel)", boxShadow: "0 4px 12px rgba(0,0,0,0.08)" }}>
            <button type="button" className="btn" onClick={() => { setMenuOpen(false); onRefresh(); }} disabled={loading} style={{ width: "100%", justifyContent: "flex-start", border: 0 }}><RefreshCw size={14} /> Refresh</button>
            <button type="button" className="btn" onClick={() => { setMenuOpen(false); onExport?.(); }} style={{ width: "100%", justifyContent: "flex-start", border: 0 }}><Download size={14} /> Export</button>
            <button type="button" className="btn" onClick={() => { setMenuOpen(false); onToggleTheme(); }} style={{ width: "100%", justifyContent: "flex-start", border: 0 }}>{darkTheme ? <Sun size={14} /> : <Moon size={14} />} Toggle theme</button>
          </div>}
        </div>
      </header>
      <div style={{ minHeight: "52px", padding: "10px 24px", display: "flex", alignItems: "center", gap: "10px", borderBottom: "1px solid var(--border)", background: "var(--bg-main)" }}>
        <div style={{ display: "inline-flex", border: "1px solid var(--border)", borderRadius: "6px", background: "var(--bg-panel)", padding: "2px" }}>
          {["Desktop", "Mobile"].map((item) => <button type="button" key={item} onClick={() => setMode(item)} style={{ border: 0, borderRadius: "4px", padding: "6px 12px", background: mode === item ? "var(--text-main)" : "transparent", color: mode === item ? "var(--bg-panel)" : "var(--text-muted)", cursor: "pointer", fontSize: "12px", fontWeight: 600 }}>{item}</button>)}
        </div>
        <select value={environment} onChange={(event) => setEnvironment(event.target.value)} aria-label="Environment" style={{ padding: "7px 10px", border: "1px solid var(--border)", borderRadius: "6px", background: "var(--bg-panel)" }}><option>Production</option><option>Demo data</option></select>
        <button type="button" className="btn btn-secondary" onClick={() => onRefresh()} disabled={loading} style={{ marginLeft: "auto" }}><CalendarDays size={14} /> Last 7 days</button>
        <button type="button" className="btn btn-primary" onClick={onRunAudit} disabled={loading}>{loading ? "Running..." : "Run audit"}</button>
      </div>
    </>
  );
}

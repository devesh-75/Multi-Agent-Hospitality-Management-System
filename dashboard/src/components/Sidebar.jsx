import React, { useState } from "react";
import { LayoutDashboard, Building2, CalendarDays, TrendingUp, Receipt, Scale, Wallet, Bot, Target, FileText, Database, Sparkles, ShieldCheck, Search } from "lucide-react";

export default function Sidebar({ currentView, setCurrentView, alertCount = 0 }) {
  const [navQuery, setNavQuery] = useState("");
  const navItems = [
    { id: "overview", label: "Executive Overview", icon: LayoutDashboard },
    { id: "properties", label: "Properties & Rooms", icon: Building2 },
    { id: "reservations", label: "Reservations & Occupancy", icon: CalendarDays },
    { id: "revenue", label: "Revenue Analytics", icon: TrendingUp },
    { id: "invoices", label: "Invoices & Payments", icon: Receipt },
    { id: "reconciliation", label: "Reconciliation", icon: Scale },
    { id: "expenses", label: "Expense Tracking", icon: Wallet },
    { id: "agents", label: "AI Multi-Agent Layer", icon: Bot },
    { id: "bde", label: "Business Development", icon: Target },
    { id: "reports", label: "Operational Reports", icon: FileText },
    { id: "data_quality", label: "Data Quality & Lineage", icon: Database },
    { id: "ask_ai", label: "Ask AI Assistant", icon: Sparkles }
  ];
  const visibleItems = navItems.filter((item) => item.label.toLowerCase().includes(navQuery.toLowerCase()));

  return (
    <aside style={{ width: "275px", height: "100vh", background: "var(--bg-sidebar)", borderRight: "1px solid var(--border)", display: "flex", flexDirection: "column", flexShrink: 0, position: "sticky", top: 0 }}>
      <div style={{ padding: "18px 16px 12px", display: "flex", alignItems: "center", gap: "10px" }}>
        <div style={{ width: "30px", height: "30px", borderRadius: "50%", background: "var(--primary)", display: "flex", alignItems: "center", justifyContent: "center" }}><ShieldCheck size={16} color="#ffffff" /></div>
        <div><h1 style={{ margin: 0, fontSize: "0.92rem", fontWeight: 700, color: "var(--text-main)" }}>hospitality-ops</h1><span className="badge badge-primary" style={{ marginTop: "3px" }}>Demo</span></div>
      </div>
      <div style={{ padding: "4px 16px 14px", position: "relative" }}>
        <Search size={15} color="var(--text-dim)" style={{ position: "absolute", left: "27px", top: "12px" }} />
        <input value={navQuery} onChange={(event) => setNavQuery(event.target.value)} placeholder="Search..." aria-label="Filter navigation" style={{ width: "100%", padding: "9px 34px 9px 32px", border: "1px solid var(--border)", borderRadius: "6px", background: "var(--bg-subtle)", color: "var(--text-main)" }} />
        <span style={{ position: "absolute", right: "25px", top: "12px", color: "var(--text-dim)", fontSize: "11px" }}>F</span>
      </div>
      <nav style={{ flex: 1, padding: "8px 12px", overflowY: "auto" }}>
        <p style={{ fontSize: "11px", fontWeight: 700, color: "var(--text-dim)", textTransform: "uppercase", letterSpacing: "0.08em", padding: "4px 12px 10px" }}>Workspace</p>
        {visibleItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return <button key={item.id} onClick={() => setCurrentView(item.id)} aria-current={isActive ? "page" : undefined} style={{ width: "100%", display: "flex", alignItems: "center", gap: "12px", padding: "10px 14px", borderRadius: "6px", border: "none", background: isActive ? "var(--primary-soft)" : "transparent", color: isActive ? "var(--text-main)" : "var(--text-muted)", cursor: "pointer", textAlign: "left", fontSize: "14px", fontWeight: isActive ? 600 : 500, marginBottom: "3px", borderLeft: isActive ? "3px solid var(--primary)" : "3px solid transparent" }}><Icon size={18} color={isActive ? "var(--primary)" : "var(--text-muted)"} /><span style={{ flex: 1 }}>{item.label}</span>{item.id === "alerts" && alertCount > 0 && <span className="badge badge-danger">{alertCount}</span>}</button>;
        })}
      </nav>
      <div style={{ padding: "14px 16px", borderTop: "1px solid var(--border)" }}><div style={{ background: "var(--bg-subtle)", border: "1px solid var(--border)", borderRadius: "6px", padding: "12px", fontSize: "12px" }}><div style={{ color: "var(--text-main)", fontWeight: 600, marginBottom: "4px" }}>Backend data</div><p style={{ color: "var(--text-muted)", fontSize: "12px", margin: 0 }}>5 properties available</p><div style={{ display: "flex", justifyContent: "space-between", marginTop: "8px", color: "var(--text-dim)", fontSize: "11px" }}><span>FastAPI</span><span>SQLite</span></div></div></div>
    </aside>
  );
}

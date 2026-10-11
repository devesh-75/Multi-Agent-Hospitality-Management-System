import React from "react";
import {
  LayoutDashboard,
  Building2,
  CalendarDays,
  TrendingUp,
  Receipt,
  Scale,
  Wallet,
  Bot,
  Target,
  FileText,
  Database,
  Sparkles,
  ShieldCheck,
  ChevronRight
} from "lucide-react";

export default function Sidebar({ currentView, setCurrentView, alertCount = 0 }) {
  const navItems = [
    { id: "overview", label: "Executive Overview", icon: LayoutDashboard },
    { id: "properties", label: "Properties & Rooms", icon: Building2 },
    { id: "reservations", label: "Reservations & Occupancy", icon: CalendarDays },
    { id: "revenue", label: "Revenue Analytics", icon: TrendingUp },
    { id: "invoices", label: "Invoices & Payments", icon: Receipt },
    { id: "reconciliation", label: "Reconciliation", icon: Scale, badge: "Audit" },
    { id: "expenses", label: "Expense Tracking", icon: Wallet },
    { id: "agents", label: "AI Multi-Agent Layer", icon: Bot, badge: "LangGraph" },
    { id: "bde", label: "Business Development", icon: Target, badge: "BDE AI" },
    { id: "reports", label: "Operational Reports", icon: FileText },
    { id: "data_quality", label: "Data Quality & Lineage", icon: Database },
    { id: "ask_ai", label: "Ask AI Assistant", icon: Sparkles, badge: "RAG" },
  ];

  return (
    <aside style={{
      width: "280px",
      height: "100vh",
      background: "var(--bg-sidebar)",
      borderRight: "1px solid var(--border)",
      display: "flex",
      flexDirection: "column",
      flexShrink: 0,
      position: "sticky",
      top: 0
    }}>
      {/* Brand Header */}
      <div style={{
        padding: "24px 20px 20px",
        borderBottom: "1px solid var(--border)",
        display: "flex",
        alignItems: "center",
        gap: "12px"
      }}>
        <div style={{
          width: "42px",
          height: "42px",
          borderRadius: "10px",
          background: "linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          boxShadow: "0 4px 12px rgba(79, 70, 229, 0.4)"
        }}>
          <ShieldCheck size={24} color="#ffffff" />
        </div>
        <div>
          <h1 style={{ fontSize: "1.02rem", fontWeight: 800, color: "#ffffff", letterSpacing: "-0.02em" }}>
            AGENTIC FINTECH
          </h1>
          <p style={{ fontSize: "0.72rem", color: "var(--accent-cyan)", fontWeight: 600 }}>
            Hospitality Intelligence Layer
          </p>
        </div>
      </div>

      {/* Navigation List */}
      <nav style={{ flex: 1, padding: "16px 12px", overflowY: "auto" }}>
        <p style={{
          fontSize: "0.68rem",
          fontWeight: 700,
          color: "var(--text-dim)",
          textTransform: "uppercase",
          letterSpacing: "0.08em",
          padding: "4px 12px 10px"
        }}>
          Operations & Intelligence
        </p>

        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentView(item.id)}
              style={{
                width: "100%",
                display: "flex",
                alignItems: "center",
                gap: "12px",
                padding: "10px 14px",
                borderRadius: "9px",
                border: "none",
                background: isActive ? "rgba(99, 102, 241, 0.16)" : "transparent",
                color: isActive ? "#ffffff" : "var(--text-muted)",
                cursor: "pointer",
                textAlign: "left",
                fontSize: "0.86rem",
                fontWeight: isActive ? 600 : 500,
                transition: "all 0.15s ease",
                marginBottom: "4px",
                borderLeft: isActive ? "3px solid var(--primary)" : "3px solid transparent"
              }}
              onMouseEnter={(e) => {
                if (!isActive) e.currentTarget.style.background = "rgba(255, 255, 255, 0.04)";
              }}
              onMouseLeave={(e) => {
                if (!isActive) e.currentTarget.style.background = "transparent";
              }}
            >
              <Icon size={18} color={isActive ? "var(--primary)" : "var(--text-muted)"} />
              <span style={{ flex: 1 }}>{item.label}</span>
              {item.badge && (
                <span className={`badge ${isActive ? "badge-primary" : "badge-cyan"}`} style={{ fontSize: "0.65rem", padding: "2px 6px" }}>
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Bottom Environment Status Card */}
      <div style={{ padding: "16px", borderTop: "1px solid var(--border)" }}>
        <div style={{
          background: "rgba(255, 255, 255, 0.03)",
          border: "1px solid var(--border)",
          borderRadius: "10px",
          padding: "12px",
          fontSize: "0.76rem"
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "6px" }}>
            <div className="live-indicator" />
            <span style={{ color: "var(--text-main)", fontWeight: 600 }}>Apaleo PMS Stream</span>
          </div>
          <p style={{ color: "var(--text-muted)", fontSize: "0.72rem" }}>
            5 Properties Synchronized
          </p>
          <div style={{ display: "flex", justifyContent: "space-between", marginTop: "8px", color: "var(--text-dim)", fontSize: "0.68rem" }}>
            <span>Engine: FastAPI</span>
            <span>RAG: Qdrant</span>
          </div>
        </div>
      </div>
    </aside>
  );
}

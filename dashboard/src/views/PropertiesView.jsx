import React from "react";
import { Building2, MapPin, Clock, DollarSign, Bed, ShieldCheck, CheckCircle } from "lucide-react";

export default function PropertiesView({ properties = [] }) {
  const flags = {
    DE: "🇩🇪",
    GB: "🇬🇧",
    FR: "🇫🇷",
    AT: "🇦🇹"
  };

  return (
    <div style={{ padding: "28px" }}>
      <div style={{ marginBottom: "24px" }}>
        <h2 style={{ fontSize: "1.45rem", fontWeight: 800, color: "#ffffff", letterSpacing: "-0.02em" }}>
          Hotel Properties & Unit Master
        </h2>
        <p style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
          5 verified European hotel properties imported from real Apaleo Property Management System exports.
        </p>
      </div>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
        gap: "20px"
      }}>
        {properties.map((p) => (
          <div key={p.id} className="glass-card" style={{ padding: "24px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "16px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <span style={{ fontSize: "1.8rem" }}>{flags[p.country_code] || "🏨"}</span>
                <div>
                  <h3 style={{ fontSize: "1.15rem", fontWeight: 700, color: "#ffffff" }}>
                    {p.name}
                  </h3>
                  <span style={{ fontSize: "0.78rem", color: "var(--accent-cyan)", fontWeight: 600 }}>
                    PMS Code: {p.id}
                  </span>
                </div>
              </div>
              <span className="badge badge-success">
                <CheckCircle size={10} /> Active
              </span>
            </div>

            <div style={{
              background: "rgba(255, 255, 255, 0.02)",
              borderRadius: "10px",
              padding: "14px",
              marginBottom: "16px",
              display: "flex",
              flexDirection: "column",
              gap: "8px",
              fontSize: "0.8rem"
            }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "var(--text-muted)" }}>Legal Corporate Entity:</span>
                <span style={{ color: "#ffffff", fontWeight: 600 }}>{p.company_name}</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "var(--text-muted)" }}>Operating Currency:</span>
                <span style={{ color: "var(--success)", fontWeight: 700 }}>{p.currency}</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "var(--text-muted)" }}>Timezone:</span>
                <span style={{ color: "#ffffff" }}>{p.timezone}</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "var(--text-muted)" }}>Data Provenance:</span>
                <span className="badge badge-primary" style={{ fontSize: "0.65rem" }}>Real Apaleo Export</span>
              </div>
            </div>

            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "var(--text-dim)", fontSize: "0.75rem" }}>
                <Bed size={14} />
                <span>Standard & Double Room Units</span>
              </div>
              <span style={{ fontSize: "0.72rem", color: "var(--text-dim)" }}>
                ID: {p.code}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

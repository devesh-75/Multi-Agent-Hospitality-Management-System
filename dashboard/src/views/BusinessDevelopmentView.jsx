import React, { useState } from "react";
import {
  Target,
  TrendingUp,
  Award,
  Layers,
  Sparkles,
  AlertTriangle,
  Send,
  Building,
  CheckCircle,
  HelpCircle,
  XCircle,
  ChevronRight
} from "lucide-react";

export default function BusinessDevelopmentView({
  competitors = [],
  comparison,
  featureGaps = [],
  trends,
  swot,
  opportunities = [],
  onAskBDE,
  selectedProperty = "BER",
  loading = false
}) {
  const [bdeQuestion, setBdeQuestion] = useState("");
  const [bdeChat, setBdeChat] = useState([]);
  const [asking, setAsking] = useState(false);
  const [activeTab, setActiveTab] = useState("overview");

  const handleSend = async (e) => {
    e.preventDefault();
    if (!bdeQuestion.trim() || asking) return;

    const q = bdeQuestion.trim();
    setBdeQuestion("");
    setBdeChat((prev) => [...prev, { sender: "user", text: q }]);
    setAsking(true);

    try {
      const resp = await onAskBDE(q, selectedProperty);
      setBdeChat((prev) => [...prev, {
        sender: "bde_agent",
        text: resp.answer,
        sources: resp.sources,
        confidence: resp.confidence,
        limitations: resp.data_limitations
      }]);
    } catch (err) {
      setBdeChat((prev) => [...prev, {
        sender: "bde_agent",
        text: "Error executing BDE Agent query: " + err.message
      }]);
    } finally {
      setAsking(false);
    }
  };

  return (
    <div style={{ padding: "28px" }}>
      {/* Title */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: "24px" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
            <span className="badge badge-primary">Specialized Agent</span>
            <span style={{ fontSize: "0.78rem", color: "var(--accent-cyan)", fontWeight: 600 }}>LangGraph Orchestrated</span>
          </div>
          <h2 style={{ fontSize: "1.45rem", fontWeight: 800, color: "#ffffff", letterSpacing: "-0.02em" }}>
            Business Development & Competitive Intelligence
          </h2>
          <p style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
            Integrating internal Property Management System records with competitor intelligence for data-grounded growth decisions.
          </p>
        </div>

        {/* Tab Navigation */}
        <div style={{
          display: "flex",
          background: "rgba(255, 255, 255, 0.05)",
          borderRadius: "8px",
          padding: "3px",
          border: "1px solid var(--border)",
          overflowX: "auto"
        }}>
          {[
            { id: "overview", label: "Competitor Overview" },
            { id: "comparison", label: "Hotel vs Competitors" },
            { id: "gaps", label: "Feature Gaps" },
            { id: "swot", label: "Grounded SWOT" },
            { id: "opportunities", label: "Growth Opportunities" },
            { id: "ask_bde", label: "Ask BDE AI" }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                padding: "6px 12px",
                border: "none",
                borderRadius: "6px",
                background: activeTab === tab.id ? "var(--primary)" : "transparent",
                color: activeTab === tab.id ? "#ffffff" : "var(--text-muted)",
                fontSize: "0.78rem",
                fontWeight: 600,
                cursor: "pointer",
                whiteSpace: "nowrap"
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* 1. Competitor Overview */}
      {activeTab === "overview" && (
        <div>
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
            gap: "20px"
          }}>
            {competitors.map((c) => (
              <div key={c.id} className="glass-card" style={{ padding: "20px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
                  <div>
                    <h3 style={{ fontSize: "1.05rem", fontWeight: 700, color: "#ffffff" }}>{c.name}</h3>
                    <span style={{ fontSize: "0.76rem", color: "var(--text-dim)" }}>
                      {c.brand || "Independent"} · {c.city}, {c.country_code}
                    </span>
                  </div>
                  <span className="badge badge-primary">★ {c.star_rating}</span>
                </div>

                <div style={{
                  background: "rgba(255, 255, 255, 0.02)",
                  borderRadius: "8px",
                  padding: "12px",
                  marginBottom: "14px",
                  fontSize: "0.78rem",
                  display: "flex",
                  flexDirection: "column",
                  gap: "6px"
                }}>
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <span style={{ color: "var(--text-muted)" }}>Average Room Rate:</span>
                    <span style={{ color: "#ffffff", fontWeight: 700 }}>€{c.average_price.toFixed(2)}</span>
                  </div>
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <span style={{ color: "var(--text-muted)" }}>Proximity Distance:</span>
                    <span style={{ color: "#ffffff" }}>{c.distance_km} km to hotel</span>
                  </div>
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <span style={{ color: "var(--text-muted)" }}>Tracked Amenities:</span>
                    <span style={{ color: "var(--accent-cyan)", fontWeight: 600 }}>{c.confirmed_features_count} cataloged</span>
                  </div>
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <span style={{ color: "var(--text-muted)" }}>Review Sentiment:</span>
                    <span style={{ color: "var(--success)", fontWeight: 600 }}>{(c.sentiment_score * 100).toFixed(0)}% Positive</span>
                  </div>
                </div>

                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span className="badge badge-cyan" style={{ fontSize: "0.65rem" }}>
                    Synthetic Benchmark
                  </span>
                  <span style={{ fontSize: "0.7rem", color: "var(--text-dim)" }}>
                    Target: {c.target_property_id}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 2. Hotel vs Competitors Comparison */}
      {activeTab === "comparison" && comparison && (
        <div className="glass-card" style={{ padding: "24px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "18px" }}>
            <div>
              <h3 style={{ fontSize: "1.1rem", fontWeight: 700, color: "#ffffff" }}>
                Property Benchmarking: {comparison.property_name} ({comparison.city})
              </h3>
              <p style={{ fontSize: "0.78rem", color: "var(--text-muted)" }}>
                Internal PMS ADR (€{comparison.our_kpis.adr}) vs Local Competitor Room Pricing
              </p>
            </div>
            <span className="badge badge-success">ADR Benchmark</span>
          </div>

          <table className="data-table">
            <thead>
              <tr>
                <th>Competitor</th>
                <th>Star Rating</th>
                <th>Distance</th>
                <th>Avg Room Rate</th>
                <th>Rate Variance</th>
                <th>Market Positioning</th>
              </tr>
            </thead>
            <tbody>
              {comparison.competitive_set.map((cs) => (
                <tr key={cs.competitor_id}>
                  <td style={{ fontWeight: 700, color: "#ffffff" }}>{cs.competitor_name}</td>
                  <td>★ {cs.star_rating}</td>
                  <td>{cs.distance_km} km</td>
                  <td style={{ fontWeight: 700, color: "#ffffff" }}>€{cs.avg_price.toFixed(2)}</td>
                  <td style={{
                    fontWeight: 700,
                    color: cs.price_difference > 0 ? "var(--warning)" : "var(--accent-cyan)"
                  }}>
                    {cs.price_difference > 0 ? `+€${cs.price_difference.toFixed(2)}` : `-€${Math.abs(cs.price_difference).toFixed(2)}`}
                    <span style={{ fontSize: "0.72rem", marginLeft: "4px" }}>({cs.price_difference_pct}%)</span>
                  </td>
                  <td>
                    <span className={`badge ${cs.price_difference > 0 ? "badge-primary" : "badge-cyan"}`}>
                      {cs.market_position}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* 3. Feature Gap Analysis */}
      {activeTab === "gaps" && (
        <div className="glass-card" style={{ padding: "24px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "18px" }}>
            <div>
              <h3 style={{ fontSize: "1.1rem", fontWeight: 700, color: "#ffffff" }}>
                Competitive Feature & Amenity Gaps
              </h3>
              <p style={{ fontSize: "0.78rem", color: "var(--text-muted)" }}>
                Amenities confirmed available across local competitors but absent or unlisted at our property
              </p>
            </div>
            <span className="badge badge-warning">Conversion Impact</span>
          </div>

          <table className="data-table">
            <thead>
              <tr>
                <th>Amenity / Service</th>
                <th>Category</th>
                <th>Our Property</th>
                <th>Competitor Penetration</th>
                <th>Relevance / Suggested Action</th>
              </tr>
            </thead>
            <tbody>
              {featureGaps.map((g, idx) => (
                <tr key={idx}>
                  <td style={{ fontWeight: 700, color: "#ffffff" }}>{g.feature_name}</td>
                  <td><span className="badge badge-primary">{g.category}</span></td>
                  <td>
                    <span style={{ color: "var(--text-dim)", fontSize: "0.78rem" }}>
                      {g.our_property_status}
                    </span>
                  </td>
                  <td>
                    <span style={{ fontWeight: 700, color: "var(--accent-cyan)" }}>
                      {g.offering_competitor_count} Competitors ({g.market_penetration_pct}%)
                    </span>
                    <div style={{ fontSize: "0.7rem", color: "var(--text-dim)" }}>
                      {g.competitors_offering.slice(0, 2).join(", ")}
                    </div>
                  </td>
                  <td style={{ fontSize: "0.78rem", color: "var(--text-muted)", maxWidth: "340px" }}>
                    {g.suggested_action}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* 4. Grounded SWOT Analysis */}
      {activeTab === "swot" && swot && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
          {/* Strengths */}
          <div className="glass-card" style={{ padding: "22px", borderLeft: "4px solid var(--success)" }}>
            <h3 style={{ fontSize: "1.05rem", fontWeight: 700, color: "var(--success)", marginBottom: "12px" }}>
              Strengths (Internal PMS Verified)
            </h3>
            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              {swot.strengths.map((s, idx) => (
                <div key={idx} style={{ background: "rgba(255, 255, 255, 0.02)", padding: "10px 12px", borderRadius: "8px" }}>
                  <div style={{ fontWeight: 600, color: "#ffffff", fontSize: "0.85rem" }}>{s.point}</div>
                  <div style={{ fontSize: "0.74rem", color: "var(--text-muted)", marginTop: "2px" }}>Evidence: {s.evidence}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Weaknesses */}
          <div className="glass-card" style={{ padding: "22px", borderLeft: "4px solid var(--danger)" }}>
            <h3 style={{ fontSize: "1.05rem", fontWeight: 700, color: "var(--danger)", marginBottom: "12px" }}>
              Weaknesses (Actionable Gaps)
            </h3>
            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              {swot.weaknesses.map((w, idx) => (
                <div key={idx} style={{ background: "rgba(255, 255, 255, 0.02)", padding: "10px 12px", borderRadius: "8px" }}>
                  <div style={{ fontWeight: 600, color: "#ffffff", fontSize: "0.85rem" }}>{w.point}</div>
                  <div style={{ fontSize: "0.74rem", color: "var(--text-muted)", marginTop: "2px" }}>Evidence: {w.evidence}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Opportunities */}
          <div className="glass-card" style={{ padding: "22px", borderLeft: "4px solid var(--accent-cyan)" }}>
            <h3 style={{ fontSize: "1.05rem", fontWeight: 700, color: "var(--accent-cyan)", marginBottom: "12px" }}>
              Opportunities (Market & Distribution)
            </h3>
            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              {swot.opportunities.map((o, idx) => (
                <div key={idx} style={{ background: "rgba(255, 255, 255, 0.02)", padding: "10px 12px", borderRadius: "8px" }}>
                  <div style={{ fontWeight: 600, color: "#ffffff", fontSize: "0.85rem" }}>{o.point}</div>
                  <div style={{ fontSize: "0.74rem", color: "var(--text-muted)", marginTop: "2px" }}>Evidence: {o.evidence}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Threats */}
          <div className="glass-card" style={{ padding: "22px", borderLeft: "4px solid var(--warning)" }}>
            <h3 style={{ fontSize: "1.05rem", fontWeight: 700, color: "var(--warning)", marginBottom: "12px" }}>
              Threats (Competitors & Channel Risks)
            </h3>
            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              {swot.threats.map((t, idx) => (
                <div key={idx} style={{ background: "rgba(255, 255, 255, 0.02)", padding: "10px 12px", borderRadius: "8px" }}>
                  <div style={{ fontWeight: 600, color: "#ffffff", fontSize: "0.85rem" }}>{t.point}</div>
                  <div style={{ fontSize: "0.74rem", color: "var(--text-muted)", marginTop: "2px" }}>Evidence: {t.evidence}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 5. Business Growth Opportunities */}
      {activeTab === "opportunities" && (
        <div style={{ display: "flex", flexDirection: "column", gap: "18px" }}>
          {opportunities.map((opp) => (
            <div key={opp.id} className="glass-card" style={{ padding: "24px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
                <div>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
                    <span className="badge badge-primary">{opp.category}</span>
                    <span style={{ fontSize: "0.75rem", color: "var(--success)", fontWeight: 600 }}>Confidence: {opp.confidence_level}</span>
                  </div>
                  <h3 style={{ fontSize: "1.15rem", fontWeight: 700, color: "#ffffff" }}>
                    {opp.title}
                  </h3>
                </div>
                <span className="badge badge-cyan">{opp.id}</span>
              </div>

              <div style={{
                background: "rgba(255, 255, 255, 0.02)",
                borderRadius: "10px",
                padding: "16px",
                marginBottom: "16px",
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: "16px",
                fontSize: "0.82rem"
              }}>
                <div>
                  <strong style={{ color: "var(--text-muted)" }}>1. Observation:</strong>
                  <p style={{ color: "#ffffff", marginTop: "2px" }}>{opp.observation}</p>
                </div>
                <div>
                  <strong style={{ color: "var(--text-muted)" }}>2. Recommended Action:</strong>
                  <p style={{ color: "var(--accent-cyan)", fontWeight: 600, marginTop: "2px" }}>{opp.recommended_action}</p>
                </div>
                <div>
                  <strong style={{ color: "var(--text-muted)" }}>3. Expected Business Impact:</strong>
                  <p style={{ color: "var(--success)", fontWeight: 700, marginTop: "2px" }}>{opp.expected_business_impact}</p>
                </div>
                <div>
                  <strong style={{ color: "var(--text-muted)" }}>4. Human Validation Required:</strong>
                  <p style={{ color: "var(--warning)", marginTop: "2px" }}>{opp.human_validation}</p>
                </div>
              </div>

              <div style={{ fontSize: "0.72rem", color: "var(--text-dim)" }}>
                <strong>Data Limitations:</strong> {opp.data_limitations}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* 6. Ask BDE AI Interactive Query Console */}
      {activeTab === "ask_bde" && (
        <div className="glass-card" style={{ padding: "24px", minHeight: "500px", display: "flex", flexDirection: "column" }}>
          <div style={{ marginBottom: "16px" }}>
            <h3 style={{ fontSize: "1.1rem", fontWeight: 700, color: "#ffffff" }}>
              Ask BDE AI: Competitive Intelligence Query Console
            </h3>
            <p style={{ fontSize: "0.78rem", color: "var(--text-muted)" }}>
              Ask strategic questions regarding competitor pricing, amenity gaps, or SWOT positioning.
            </p>
          </div>

          {/* Chat Messages */}
          <div style={{
            flex: 1,
            background: "rgba(0, 0, 0, 0.2)",
            borderRadius: "10px",
            padding: "16px",
            overflowY: "auto",
            marginBottom: "16px",
            minHeight: "320px",
            display: "flex",
            flexDirection: "column",
            gap: "14px"
          }}>
            {bdeChat.length === 0 ? (
              <div style={{ textAlign: "center", color: "var(--text-dim)", margin: "auto" }}>
                <Target size={36} color="var(--primary)" style={{ margin: "0 auto 8px" }} />
                <p>Try asking: "Who are our main competitors and what are their rates?"</p>
                <p style={{ fontSize: "0.75rem", marginTop: "4px" }}>or "What amenity gaps exist compared to local boutique hotels?"</p>
              </div>
            ) : (
              bdeChat.map((msg, i) => (
                <div key={i} style={{
                  alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
                  maxWidth: "80%",
                  background: msg.sender === "user" ? "var(--primary)" : "rgba(255, 255, 255, 0.05)",
                  border: msg.sender === "user" ? "none" : "1px solid var(--border)",
                  borderRadius: "10px",
                  padding: "12px 16px",
                  color: "#ffffff",
                  fontSize: "0.85rem"
                }}>
                  <div style={{ fontWeight: 700, fontSize: "0.72rem", marginBottom: "4px", color: msg.sender === "user" ? "#ffffff" : "var(--accent-cyan)" }}>
                    {msg.sender === "user" ? "You" : "BDE Intelligence Agent"}
                  </div>
                  <div style={{ whiteSpace: "pre-line", lineHeight: 1.5 }}>
                    {msg.text}
                  </div>
                  {msg.sources && (
                    <div style={{ fontSize: "0.7rem", color: "var(--text-dim)", marginTop: "8px", borderTop: "1px solid rgba(255,255,255,0.06)", paddingTop: "4px" }}>
                      Sources: {msg.sources.join(", ")}
                    </div>
                  )}
                </div>
              ))
            )}
            {asking && (
              <div style={{ color: "var(--accent-cyan)", fontSize: "0.8rem", fontStyle: "italic" }}>
                Synthesizing competitor benchmarks and PMS records...
              </div>
            )}
          </div>

          {/* Input Form */}
          <form onSubmit={handleSend} style={{ display: "flex", gap: "10px" }}>
            <input
              type="text"
              placeholder="Ask a competitive intelligence question..."
              value={bdeQuestion}
              onChange={(e) => setBdeQuestion(e.target.value)}
              style={{
                flex: 1,
                background: "rgba(255, 255, 255, 0.05)",
                border: "1px solid var(--border)",
                borderRadius: "8px",
                padding: "12px 16px",
                color: "#ffffff",
                fontSize: "0.85rem",
                outline: "none"
              }}
            />
            <button
              type="submit"
              disabled={asking || !bdeQuestion.trim()}
              className="btn btn-primary"
              style={{ padding: "0 20px" }}
            >
              <Send size={16} />
              <span>Ask BDE</span>
            </button>
          </form>
        </div>
      )}
    </div>
  );
}

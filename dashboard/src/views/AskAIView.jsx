import React, { useState } from "react";
import { Sparkles, Send, Database, CheckCircle, ShieldCheck } from "lucide-react";

export default function AskAIView({ onAsk, selectedProperty = "" }) {
  const [question, setQuestion] = useState("");
  const [chat, setChat] = useState([
    {
      sender: "assistant",
      text: "Hello! I am your Hospitality Fintech Intelligence Assistant. You can ask me any question about hotel operations, revenue KPIs, average daily rates (ADR), occupancy, reconciliation exceptions, departmental expenses, or competitor benchmarks."
    }
  ]);
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    const q = question.trim();
    setQuestion("");
    setChat((prev) => [...prev, { sender: "user", text: q }]);
    setLoading(true);

    try {
      const resp = await onAsk(q, selectedProperty);
      setChat((prev) => [...prev, {
        sender: "assistant",
        text: resp.answer,
        sources: resp.sources,
        confidence: resp.confidence,
        structured_data: resp.structured_data,
        limitations: resp.data_limitations
      }]);
    } catch (err) {
      setChat((prev) => [...prev, {
        sender: "assistant",
        text: "Error retrieving answer: " + err.message
      }]);
    } finally {
      setLoading(false);
    }
  };

  const sampleQueries = [
    "What is our total booked revenue and ADR across all properties?",
    "Show me the reconciliation exceptions and missing OTA payouts.",
    "Did we detect any unusual operating expense spikes in September?",
    "Compare Hotel Berlin performance against local competitors."
  ];

  return (
    <div style={{ padding: "28px" }}>
      <div style={{ marginBottom: "24px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
          <span className="badge badge-primary">Hybrid RAG Architecture</span>
          <span style={{ fontSize: "0.78rem", color: "var(--accent-cyan)", fontWeight: 600 }}>SQL Deterministic + Qdrant Vector</span>
        </div>
        <h2 style={{ fontSize: "1.45rem", fontWeight: 800, color: "#ffffff", letterSpacing: "-0.02em" }}>
          Natural Language Financial Assistant
        </h2>
        <p style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
          Ask operational, financial, or competitive questions. Numerical answers are executed via deterministic SQL; contextual insights are retrieved from indexed reports.
        </p>
      </div>

      <div className="glass-card" style={{ padding: "24px", minHeight: "560px", display: "flex", flexDirection: "column" }}>
        {/* Sample queries pills */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: "8px", marginBottom: "16px" }}>
          {sampleQueries.map((sq, i) => (
            <button
              key={i}
              onClick={() => setQuestion(sq)}
              className="btn btn-secondary"
              style={{ fontSize: "0.74rem", padding: "5px 11px", borderRadius: "9999px" }}
            >
              {sq}
            </button>
          ))}
        </div>

        {/* Chat History */}
        <div style={{
          flex: 1,
          background: "rgba(0, 0, 0, 0.25)",
          borderRadius: "10px",
          padding: "18px",
          overflowY: "auto",
          marginBottom: "16px",
          display: "flex",
          flexDirection: "column",
          gap: "14px"
        }}>
          {chat.map((msg, i) => (
            <div key={i} style={{
              alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
              maxWidth: "82%",
              background: msg.sender === "user" ? "var(--primary)" : "rgba(255, 255, 255, 0.04)",
              border: msg.sender === "user" ? "none" : "1px solid var(--border)",
              borderRadius: "10px",
              padding: "14px 18px",
              color: "#ffffff",
              fontSize: "0.86rem"
            }}>
              <div style={{ fontWeight: 700, fontSize: "0.74rem", marginBottom: "4px", color: msg.sender === "user" ? "#ffffff" : "var(--accent-cyan)" }}>
                {msg.sender === "user" ? "You" : "Fintech RAG Assistant"}
              </div>
              <div style={{ whiteSpace: "pre-line", lineHeight: 1.6 }}>
                {msg.text}
              </div>
              {msg.sources && msg.sources.length > 0 && (
                <div style={{ fontSize: "0.72rem", color: "var(--text-dim)", marginTop: "10px", borderTop: "1px solid rgba(255,255,255,0.06)", paddingTop: "6px" }}>
                  <strong>Authoritative Citations:</strong> {msg.sources.join(" | ")}
                </div>
              )}
            </div>
          ))}
          {loading && (
            <div style={{ color: "var(--accent-cyan)", fontSize: "0.82rem", fontStyle: "italic" }}>
              Synthesizing response from authoritative SQL ledgers and vector indices...
            </div>
          )}
        </div>

        {/* Query Input */}
        <form onSubmit={handleSend} style={{ display: "flex", gap: "10px" }}>
          <input
            type="text"
            placeholder="Type your question about revenue, reconciliation, expenses, or competitors..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            style={{
              flex: 1,
              background: "rgba(255, 255, 255, 0.05)",
              border: "1px solid var(--border)",
              borderRadius: "8px",
              padding: "12px 18px",
              color: "#ffffff",
              fontSize: "0.88rem",
              outline: "none"
            }}
          />
          <button
            type="submit"
            disabled={loading || !question.trim()}
            className="btn btn-primary"
            style={{ padding: "0 24px" }}
          >
            <Send size={16} />
            <span>Send Query</span>
          </button>
        </form>
      </div>
    </div>
  );
}

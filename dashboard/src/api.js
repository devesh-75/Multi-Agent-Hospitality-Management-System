/**
 * Centralized API Client for Hospitality Fintech Backend
 */

const API_BASE = import.meta.env.VITE_API_BASE || "/api/v1";

async function request(endpoint, options = {}) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || `Request failed with status ${res.status}`);
    }
    return await res.json();
  } catch (error) {
    console.error(`API Error on ${endpoint}:`, error);
    throw error;
  }
}

export const api = {
  // Health
  getHealth: () => request("/health"),

  // Properties
  getProperties: () => request("/properties"),
  getProperty: (id) => request(`/properties/${id}`),

  // Executive Overview & Analytics
  getRevenueSummary: (propId) => request(`/revenue${propId ? `?property_id=${propId}` : ""}`),
  getPropertyComparison: () => request("/revenue/comparison"),
  getRevenueForecast: (propId, horizon = 14) => request(`/revenue/forecast?horizon_days=${horizon}${propId ? `&property_id=${propId}` : ""}`),
  getOccupancy: (propId) => request(`/occupancy${propId ? `?property_id=${propId}` : ""}`),

  // Reservations
  getReservations: (propId, limit = 50) => request(`/reservations?limit=${limit}${propId ? `&property_id=${propId}` : ""}`),

  // Invoices & Payments
  getInvoices: (propId, limit = 50) => request(`/invoices?limit=${limit}${propId ? `&property_id=${propId}` : ""}`),
  getPayments: (propId, limit = 50) => request(`/invoices/payments/list?limit=${limit}${propId ? `&property_id=${propId}` : ""}`),

  // Reconciliation
  getReconciliation: (propId) => request(`/reconciliation${propId ? `?property_id=${propId}` : ""}`),
  runReconciliation: (propId) => request(`/reconciliation/run${propId ? `?property_id=${propId}` : ""}`, { method: "POST" }),

  // Expenses
  getExpenses: (propId) => request(`/expenses${propId ? `?property_id=${propId}` : ""}`),
  getExpensesList: (propId, limit = 50) => request(`/expenses/list?limit=${limit}${propId ? `&property_id=${propId}` : ""}`),
  runExpenseAudit: (propId) => request(`/expenses/run${propId ? `?property_id=${propId}` : ""}`, { method: "POST" }),

  // Competitor Intelligence & BDE
  getCompetitors: (propId) => request(`/competitors${propId ? `?property_id=${propId}` : ""}`),
  getCompetitorOverview: (propId) => request(`/competitor-overview${propId ? `?property_id=${propId}` : ""}`),
  getCompetitorComparison: (propId = "BER") => request(`/competitor-comparison?property_id=${propId}`),
  getCompetitiveGaps: (propId = "BER") => request(`/competitive-gaps?property_id=${propId}`),
  getCompetitiveTrends: (propId = "BER") => request(`/competitive-trends?property_id=${propId}`),
  getBusinessOpportunities: (propId = "BER") => request(`/business-opportunities?property_id=${propId}`),
  getSWOTAnalysis: (propId = "BER") => request(`/swot-analysis?property_id=${propId}`),
  askBDE: (question, propId) => request("/bde/ask", {
    method: "POST",
    body: JSON.stringify({ question, property_id: propId })
  }),

  // Reports
  getReports: (propId) => request(`/reports${propId ? `?property_id=${propId}` : ""}`),
  generateReport: (reportType, propId) => request(`/reports/generate?report_type=${reportType}${propId ? `&property_id=${propId}` : ""}`, { method: "POST" }),

  // Alerts
  getAlerts: (propId) => request(`/alerts?unresolved_only=true${propId ? `&property_id=${propId}` : ""}`),
  resolveAlert: (alertId) => request(`/alerts/${alertId}/resolve`, { method: "POST" }),

  // Multi-Agent Orchestration
  runAgents: (propId, agent = "all", query = "Run full operations audit") => request(`/agents/run?agent=${agent}${propId ? `&property_id=${propId}` : ""}`, {
    method: "POST",
    body: JSON.stringify({ query })
  }),
  getAgentRuns: () => request("/agents/runs"),

  // RAG / Q&A
  ask: (question, propId) => request("/ask", {
    method: "POST",
    body: JSON.stringify({ question, property_id: propId })
  })
};

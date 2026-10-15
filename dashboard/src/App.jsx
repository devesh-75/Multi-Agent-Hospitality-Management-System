import React, { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import ExecutiveOverview from "./views/ExecutiveOverview";
import PropertiesView from "./views/PropertiesView";
import ReservationsView from "./views/ReservationsView";
import RevenueView from "./views/RevenueView";
import InvoicesView from "./views/InvoicesView";
import ReconciliationView from "./views/ReconciliationView";
import ExpensesView from "./views/ExpensesView";
import AIAgentsView from "./views/AIAgentsView";
import BusinessDevelopmentView from "./views/BusinessDevelopmentView";
import ReportsView from "./views/ReportsView";
import DataQualityView from "./views/DataQualityView";
import AskAIView from "./views/AskAIView";
import { api } from "./api";

export default function App() {
  const [currentView, setCurrentView] = useState("overview");
  const [selectedProperty, setSelectedProperty] = useState("");
  const [loading, setLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState("healthy");

  // State holders
  const [properties, setProperties] = useState([]);
  const [kpis, setKpis] = useState(null);
  const [comparison, setComparison] = useState([]);
  const [revenueData, setRevenueData] = useState(null);
  const [reservations, setReservations] = useState([]);
  const [invoices, setInvoices] = useState([]);
  const [payments, setPayments] = useState([]);
  const [reconciliationData, setReconciliationData] = useState(null);
  const [expensesData, setExpensesData] = useState(null);
  const [competitors, setCompetitors] = useState([]);
  const [compComparison, setCompComparison] = useState(null);
  const [featureGaps, setFeatureGaps] = useState([]);
  const [trends, setTrends] = useState(null);
  const [swot, setSwot] = useState(null);
  const [opportunities, setOpportunities] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [reports, setReports] = useState([]);
  const [agentRuns, setAgentRuns] = useState([]);
  const [lastAgentResult, setLastAgentResult] = useState(null);
  const [requestErrors, setRequestErrors] = useState([]);
  const [toast, setToast] = useState(null);
  const [darkTheme, setDarkTheme] = useState(() => localStorage.getItem("hospitality-theme") === "dark");

  useEffect(() => {
    document.documentElement.dataset.theme = darkTheme ? "dark" : "light";
    localStorage.setItem("hospitality-theme", darkTheme ? "dark" : "light");
  }, [darkTheme]);

  const fetchData = async () => {
    setLoading(true);
    setRequestErrors([]);
    try {
      const requests = [
        ["health", api.getHealth()],
        ["properties", api.getProperties()],
        ["revenue", api.getRevenueSummary(selectedProperty)],
        ["revenue/comparison", api.getPropertyComparison()],
        ["reservations", api.getReservations(selectedProperty, 100)],
        ["invoices", api.getInvoices(selectedProperty, 100)],
        ["invoices/payments/list", api.getPayments(selectedProperty, 100)],
        ["reconciliation", api.getReconciliation(selectedProperty)],
        ["expenses", api.getExpenses(selectedProperty)],
        ["competitor-overview", api.getCompetitorOverview(selectedProperty)],
        ["alerts", api.getAlerts(selectedProperty)],
        ["reports", api.getReports(selectedProperty)],
        ["agents/runs", api.getAgentRuns()]
      ];
      const results = await Promise.allSettled(requests.map(([, request]) => request));
      const failures = results
        .map((result, index) => ({ result, endpoint: requests[index][0] }))
        .filter(({ result }) => result.status === "rejected");
      failures.forEach(({ result, endpoint }) => {
        console.error(`Dashboard request failed: ${endpoint}`, result.reason);
      });
      setRequestErrors(failures.map(({ endpoint }) => endpoint));

      const [healthRes, propsRes, revSummary, propComp, resRes, invRes, pmtRes, recRes, expRes, compRes, alertsRes, repRes, runsRes] = results;

      if (healthRes.status === "fulfilled") {
        setBackendStatus(healthRes.value.status);
      }
      if (propsRes.status === "fulfilled") setProperties(propsRes.value);
      if (revSummary.status === "fulfilled") {
        setRevenueData(revSummary.value);
        setKpis(revSummary.value.kpis);
      }
      if (propComp.status === "fulfilled") setComparison(propComp.value);
      if (resRes.status === "fulfilled") setReservations(resRes.value);
      if (invRes.status === "fulfilled") setInvoices(invRes.value);
      if (pmtRes.status === "fulfilled") setPayments(pmtRes.value);
      if (recRes.status === "fulfilled") setReconciliationData(recRes.value);
      if (expRes.status === "fulfilled") setExpensesData(expRes.value);
      if (compRes.status === "fulfilled") setCompetitors(compRes.value);
      if (alertsRes.status === "fulfilled") setAlerts(alertsRes.value);
      if (repRes.status === "fulfilled") setReports(repRes.value);
      if (runsRes.status === "fulfilled") setAgentRuns(runsRes.value);

      // Fetch BDE details for specific property (or BER default)
      const bdeProp = selectedProperty || "BER";
      const bdeRequests = [
        ["competitor-comparison", api.getCompetitorComparison(bdeProp)],
        ["competitive-gaps", api.getCompetitiveGaps(bdeProp)],
        ["competitive-trends", api.getCompetitiveTrends(bdeProp)],
        ["swot-analysis", api.getSWOTAnalysis(bdeProp)],
        ["business-opportunities", api.getBusinessOpportunities(bdeProp)]
      ];
      const bdeResults = await Promise.allSettled(bdeRequests.map(([, request]) => request));
      const bdeFailures = bdeResults
        .map((result, index) => ({ result, endpoint: bdeRequests[index][0] }))
        .filter(({ result }) => result.status === "rejected");
      bdeFailures.forEach(({ result, endpoint }) => {
        console.error(`Dashboard request failed: ${endpoint}`, result.reason);
      });
      setRequestErrors((previous) => [
        ...new Set([...previous, ...bdeFailures.map(({ endpoint }) => endpoint)])
      ]);
      const [compCompRes, gapsRes, trendsRes, swotRes, oppsRes] = bdeResults;

      if (compCompRes.status === "fulfilled") setCompComparison(compCompRes.value);
      if (gapsRes.status === "fulfilled") setFeatureGaps(gapsRes.value);
      if (trendsRes.status === "fulfilled") setTrends(trendsRes.value);
      if (swotRes.status === "fulfilled") setSwot(swotRes.value);
      if (oppsRes.status === "fulfilled") setOpportunities(oppsRes.value);

    } catch (err) {
      console.error("Error loading dashboard data:", err);
      setBackendStatus("degraded");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [selectedProperty]);

  const handleRunAudit = async (agent = "all") => {
    setLoading(true);
    try {
      const result = await api.runAgents(selectedProperty, agent);
      setLastAgentResult(result);
      setToast({ type: "success", message: `${agent === "all" ? "Full workflow" : agent} run completed.` });
      // Refresh metrics after run
      await fetchData();
    } catch (err) {
      console.error("Agent run failed", err);
      setToast({ type: "error", message: err.message || "The agent run failed." });
    } finally {
      setLoading(false);
    }
  };

  const handleResolveAlert = async (alertId) => {
    try {
      await api.resolveAlert(alertId);
      setAlerts((prev) => prev.filter((a) => a.id !== alertId));
    } catch (err) {
      console.error("Error resolving alert:", err);
    }
  };

  const handleGenerateReport = async (reportType, propId) => {
    setLoading(true);
    try {
      await api.generateReport(reportType, propId);
      const updatedReports = await api.getReports(propId);
      setReports(updatedReports);
    } catch (err) {
      alert("Error generating report: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = () => {
    if (!reconciliationData) {
      setToast({ type: "error", message: "There is no reconciliation data to export." });
      return;
    }
    const blob = new Blob([JSON.stringify(reconciliationData, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "reconciliation-data.json";
    link.click();
    URL.revokeObjectURL(url);
    setToast({ type: "success", message: "Reconciliation data exported." });
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "var(--bg-main)" }}>
      {requestErrors.length > 0 && (
        <div className="error-banner" role="alert">
          <span>Unable to load: {requestErrors.join(", ")}</span>
          <button type="button" onClick={() => setRequestErrors([])} aria-label="Dismiss request errors">Dismiss</button>
        </div>
      )}
      {toast && (
        <div className={`toast toast-${toast.type}`} role="status">
          <span>{toast.message}</span>
          <button type="button" onClick={() => setToast(null)} aria-label="Dismiss notification">Dismiss</button>
        </div>
      )}
      {/* Sidebar Navigation */}
      <Sidebar
        currentView={currentView}
        setCurrentView={setCurrentView}
        alertCount={alerts.length}
      />

      {/* Main Content Area */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", minWidth: 0 }}>
        <Header
          selectedProperty={selectedProperty}
          setSelectedProperty={setSelectedProperty}
          properties={properties}
          onRefresh={fetchData}
          onRunAudit={() => handleRunAudit("all")}
          onExport={handleExport}
          currentView={currentView}
          darkTheme={darkTheme}
          onToggleTheme={() => setDarkTheme((current) => !current)}
          backendStatus={backendStatus}
          loading={loading}
        />

        <main style={{ flex: 1, overflowY: "auto" }}>
          {currentView === "overview" && (
            <ExecutiveOverview
              kpis={kpis}
              comparison={comparison}
              alerts={alerts}
              onResolveAlert={handleResolveAlert}
              onNavigate={setCurrentView}
            />
          )}

          {currentView === "properties" && (
            <PropertiesView properties={properties} />
          )}

          {currentView === "reservations" && (
            <ReservationsView reservations={reservations} />
          )}

          {currentView === "revenue" && (
            <RevenueView revenueData={revenueData} kpis={kpis} />
          )}

          {currentView === "invoices" && (
            <InvoicesView invoices={invoices} payments={payments} />
          )}

          {currentView === "reconciliation" && (
            <ReconciliationView
              reconciliationData={reconciliationData}
              onRunAudit={() => handleRunAudit("reconciliation")}
              loading={loading}
            />
          )}

          {currentView === "expenses" && (
            <ExpensesView
              expensesData={expensesData}
              onRunAudit={() => handleRunAudit("expense")}
              loading={loading}
            />
          )}

          {currentView === "agents" && (
            <AIAgentsView
              onRunAudit={handleRunAudit}
              agentRuns={agentRuns}
              lastResult={lastAgentResult}
              loading={loading}
              selectedProperty={selectedProperty}
            />
          )}

          {currentView === "bde" && (
            <BusinessDevelopmentView
              competitors={competitors}
              comparison={compComparison}
              featureGaps={featureGaps}
              trends={trends}
              swot={swot}
              opportunities={opportunities}
              onAskBDE={api.askBDE}
              selectedProperty={selectedProperty || "BER"}
              loading={loading}
            />
          )}

          {currentView === "reports" && (
            <ReportsView
              reports={reports}
              onGenerateReport={handleGenerateReport}
              loading={loading}
              selectedProperty={selectedProperty}
            />
          )}

          {currentView === "data_quality" && (
            <DataQualityView />
          )}

          {currentView === "ask_ai" && (
            <AskAIView onAsk={api.ask} selectedProperty={selectedProperty} />
          )}
        </main>
      </div>
    </div>
  );
}

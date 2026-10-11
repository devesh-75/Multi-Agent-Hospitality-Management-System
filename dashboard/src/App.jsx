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

  const fetchData = async () => {
    setLoading(true);
    try {
      const [
        healthRes,
        propsRes,
        revSummary,
        propComp,
        resRes,
        invRes,
        pmtRes,
        recRes,
        expRes,
        compRes,
        alertsRes,
        repRes,
        runsRes
      ] = await Promise.allSettled([
        api.getHealth(),
        api.getProperties(),
        api.getRevenueSummary(selectedProperty),
        api.getPropertyComparison(),
        api.getReservations(selectedProperty, 100),
        api.getInvoices(selectedProperty, 100),
        api.getPayments(selectedProperty, 100),
        api.getReconciliation(selectedProperty),
        api.getExpenses(selectedProperty),
        api.getCompetitors(selectedProperty),
        api.getAlerts(selectedProperty),
        api.getReports(selectedProperty),
        api.getAgentRuns()
      ]);

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
      const [compCompRes, gapsRes, trendsRes, swotRes, oppsRes] = await Promise.allSettled([
        api.getCompetitorComparison(bdeProp),
        api.getCompetitiveGaps(bdeProp),
        api.getCompetitiveTrends(bdeProp),
        api.getSWOTAnalysis(bdeProp),
        api.getBusinessOpportunities(bdeProp)
      ]);

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
      // Refresh metrics after run
      await fetchData();
    } catch (err) {
      alert("Error executing agent run: " + err.message);
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

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "var(--bg-main)" }}>
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

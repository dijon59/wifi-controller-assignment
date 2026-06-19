import { useEffect, useState } from "react";
import "./App.css";

import DashboardHeader from "./components/DashboardHeader";
import ErrorMessage from "./components/ErrorMessage";
import PaginationControls from "./components/PaginationControls";
import SessionsTable from "./components/SessionsTable";
import SyncHistoryTable from "./components/SyncHistoryTable";
import SyncSummary from "./components/SyncSummary";
import VenuesTable from "./components/VenuesTable";

const API_BASE_URL = "http://localhost:8000";

function App() {
  const [venues, setVenues] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [syncLog, setSyncLog] = useState({
    status: "Not synced yet",
    lastSync: "Waiting for first sync",
  });
  const [syncHistory, setSyncHistory] = useState([]);

  const [isVenuesLoading, setIsVenuesLoading] = useState(false);
  const [isSessionsLoading, setIsSessionsLoading] = useState(false);
  const [isSyncInfoLoading, setIsSyncInfoLoading] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const [venuePage, setVenuePage] = useState(0);
  const [sessionPage, setSessionPage] = useState(0);
  const [syncInfoPage, setSyncInfoPage] = useState(0);


  const [venuesTotal, setVenuesTotal] = useState(0);
  const [sessionsTotal, setSessionsTotal] = useState(0);
  const [syncInfoTotal, setSyncInfoTotal] = useState(0);

  const [venuesPageSize, setVenuesPageSize] = useState(10);
  const [sessionsPageSize, setSessionsPageSize] = useState(10);
  const [syncInfoPageSize, setSyncInfoPageSize] = useState(10);

  
  async function loadVenues(nextVenuePage = venuePage) {
    setIsVenuesLoading(true);
    setErrorMessage("");

    try {
      const venuesResp = await fetch(`${API_BASE_URL}/venues?page=${nextVenuePage + 1}`)

      if (!venuesResp.ok) {
        throw new Error("Failed to load venues data");
      }

      const venuesData = await venuesResp.json();

      setVenues(venuesData.items ?? []);
      setVenuesPageSize(venuesData.limit ?? 10);
      setVenuesTotal(venuesData.total ?? 0);
    } catch (error) {
      setErrorMessage(error.message || "Failled to load venues data");
    } finally {
      setIsVenuesLoading(false);
    }
  }

  async function loadSessions(nextSessionPage = sessionPage) {
    setIsSessionsLoading(true);
    setErrorMessage("");

    try {
      const sessionsResp = await fetch(`${API_BASE_URL}/wifi-sessions?page=${nextSessionPage + 1}`)

      if (!sessionsResp.ok) {
        throw new Error("Failed to load sessions data");
      }

      const sessionsData = await sessionsResp.json();

      setSessions(sessionsData.items ?? []);
      setSessionsPageSize(sessionsData.limit ?? 10);
      setSessionsTotal(sessionsData.total ?? 0);
    } catch (error) {
      setErrorMessage(error.message || "Failled to load sessions data");
    } finally {
      setIsSessionsLoading(false);
    }
  }

  async function loadSyncInfo(nextsyncInfoPage = syncInfoPage) {
    setIsSyncInfoLoading(true);
    setErrorMessage("");

    try {
      const syncInfoResp = await fetch(`${API_BASE_URL}/sync-info?page=${nextsyncInfoPage + 1}`)

      if (!syncInfoResp.ok) {
        throw new Error("Failed to load sync info data");
      }

      const syncInfoData = await syncInfoResp.json();

      setSyncHistory(syncInfoData.history ?? []);
      setSyncInfoPageSize(syncInfoData.limit ?? 10);
      setSyncInfoTotal(syncInfoData.total ?? 0);
      setSyncLog(syncInfoData.latest);
    } catch (error) {
      setErrorMessage(error.message || "Failled to load sync info data");
    } finally {
      setIsSyncInfoLoading(false);
    }
  }

  useEffect(() => {
    loadVenues();
  }, [venuePage]);

  useEffect (() => {
    loadSessions();
  }, [sessionPage])

  useEffect(() => {
    loadSyncInfo();
  }, [syncInfoPage]);

  async function handleSyncClick() {
    setIsSyncing(true);
    setErrorMessage("");

    try {
      const response = await fetch(`${API_BASE_URL}/sync`, { method: "POST" });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Sync failed");
      }

      loadVenues();
      loadSessions();
      loadSyncInfo();

    } catch (error) {
      setErrorMessage(error.message || "Sync failed");
    } finally {
      setIsSyncing(false);
    }
  }

  return (
    <main className="app-shell">
      <DashboardHeader
        isSyncing={isSyncing}
        onSync={handleSyncClick}
      />
      <ErrorMessage message={errorMessage} />

      <SyncSummary
        sessionsCount={sessions.length}
        status={syncLog}
        venuesCount={venues.length}
      />

      <section className="content-grid">
        <div>
          <VenuesTable isLoading={isVenuesLoading} venues={venues} />
          {!isVenuesLoading && venuesTotal > 0 && (
            <PaginationControls
              currentPage={venuePage}
              onPageChange={setVenuePage}
              pageSize={venuesPageSize}
              totalItems={venuesTotal}
            />
          )}
        </div>

        <div>
          <SessionsTable isLoading={isSessionsLoading} sessions={sessions} />
          {!isSessionsLoading && sessionsTotal > 0 && (
            <PaginationControls
              currentPage={sessionPage}
              onPageChange={setSessionPage}
              pageSize={sessionsPageSize}
              totalItems={sessionsTotal}
            />
          )}
        </div>
      </section>

      <SyncHistoryTable isLoading={isSyncInfoLoading} syncHistory={syncHistory} />
      {!isSyncInfoLoading && syncInfoTotal > 0 && (
            <PaginationControls
              currentPage={syncInfoPage}
              onPageChange={setSyncInfoPage}
              pageSize={syncInfoPageSize}
              totalItems={syncInfoTotal}
            />
          )}
    </main>
  );
}

export default App;

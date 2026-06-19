function DashboardHeader({ isSyncing, onSync }) {
  return (
    <header className="page-header">
      <div>
        <p className="eyebrow">Wi-Fi Controller Integration</p>
        <h1>Bconnect Dashboard</h1>
        <p className="page-description">
          Trigger a controller sync and review normalised venue and session data.
        </p>
      </div>

      <button className="primary-button" disabled={isSyncing} onClick={onSync}>
        {isSyncing ? "Syncing..." : "Run Sync"}
      </button>
    </header>
  );
}

export default DashboardHeader;

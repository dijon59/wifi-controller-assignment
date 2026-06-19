import EmptyState from "./EmptyState";

function formatDate(value) {
  if (!value) {
    return "-";
  }

  return new Intl.DateTimeFormat("en-ZA", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(new Date(value));
}

function SyncHistoryTable({ isLoading, syncHistory }) {
  return (
    <article className="panel">
      <div className="panel-header">
        <h2>Sync History</h2>
        <p>Recent sync attempts and their record counts.</p>
      </div>

      {isLoading ? (
        <EmptyState message="Loading sync history..." />
      ) : syncHistory.length === 0 ? (
        <EmptyState message="No sync runs recorded yet." />
      ) : (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Status</th>
                <th>Started</th>
                <th>Finished</th>
                <th>Venues</th>
                <th>APs</th>
                <th>Sessions</th>
                <th>Error</th>
              </tr>
            </thead>
            <tbody>
              {syncHistory.map((syncRun) => (
                <tr key={syncRun.id}>
                  <td>
                    <span className={`status-pill ${syncRun.status}`}>
                      {syncRun.status}
                    </span>
                  </td>
                  <td>{formatDate(syncRun.startedAt)}</td>
                  <td>{formatDate(syncRun.finishedAt)}</td>
                  <td>{syncRun.venuesSynced}</td>
                  <td>{syncRun.accessPointsSynced}</td>
                  <td>{syncRun.sessionsSynced}</td>
                  <td>{syncRun.error ?? "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </article>
  );
}

export default SyncHistoryTable;

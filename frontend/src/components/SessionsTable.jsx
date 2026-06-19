import EmptyState from "./EmptyState";

function SessionsTable({ isLoading, sessions }) {
  return (
    <article className="panel">
      <div className="panel-header">
        <h2>Wi-Fi Sessions</h2>
        <p>Recent connected-user session activity.</p>
      </div>

      {isLoading ? (
        <EmptyState message="Loading sessions..." />
      ) : sessions.length === 0 ? (
        <EmptyState message="No sessions synced yet." />
      ) : (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Client</th>
                <th>Venue</th>
                <th>Access Point</th>
                <th>Status</th>
                <th>Usage</th>
                <th>Last Synced</th>
              </tr>
            </thead>
            <tbody>
              {sessions.map((session) => {
                const status = session.ended_at ? "Completed" : "Active";
                const usage =
                  session.bytes_received || session.bytes_sent
                    ? `${session.bytes_received ?? 0} / ${session.bytes_sent ?? 0}`
                    : "-";
                const lastSynced = session.last_synced_at
                  ? new Intl.DateTimeFormat("en-ZA", {
                      year: "numeric",
                      month: "2-digit",
                      day: "2-digit",
                      hour: "2-digit",
                      minute: "2-digit",
                      second: "2-digit",
                      hour12: false,
                    }).format(new Date(session.last_synced_at))
                  : "-";

                return (
                  <tr key={session.session_id}>
                    <td>{session.client_mac}</td>
                    <td>{session.venue_name ?? "-"}</td>
                    <td>{session.access_point_name ?? session.access_point_id}</td>
                    <td>
                      <span className={`status-pill ${status.toLowerCase()}`}>
                        {status}
                      </span>
                    </td>
                    <td>{usage}</td>
                    <td>{lastSynced}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </article>
  );
}

export default SessionsTable;

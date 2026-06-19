import EmptyState from "./EmptyState";

function VenuesTable({ isLoading, venues }) {
  return (
    <article className="panel">
      <div className="panel-header">
        <h2>Venues</h2>
        <p>Synced sites from the controller.</p>
      </div>

      {isLoading ? (
        <EmptyState message="Loading venues..." />
      ) : venues.length === 0 ? (
        <EmptyState message="No venues synced yet." />
      ) : (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Controller ID</th>
                <th>Timezone</th>
                <th>APs</th>
                <th>Last Synced</th>
              </tr>
            </thead>
            <tbody>
              {venues.map((venue) => {
                const lastSynced = venue.last_synced_at
                  ? new Intl.DateTimeFormat("en-ZA", {
                      year: "numeric",
                      month: "2-digit",
                      day: "2-digit",
                      hour: "2-digit",
                      minute: "2-digit",
                      second: "2-digit",
                      hour12: false,
                    }).format(new Date(venue.last_synced_at))
                  : "-";

                return (
                  <tr key={venue.venue_id}>
                    <td>{venue.name}</td>
                    <td>{venue.venue_id}</td>
                    <td>{venue.timezone}</td>
                    <td>{venue.access_points_count ?? "-"}</td>
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

export default VenuesTable;

function SyncSummary({ sessionsCount, status, venuesCount }) {
  function formatLastSync(value) {
    if (!value || value === "Never synced" || value === "Waiting for first sync") {
      return value;
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
      return value;
    }

    return new Intl.DateTimeFormat("en-ZA", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false,
    }).format(date);
  }

  const cards = [
    ["Status", status.status],
    ["Last Sync", formatLastSync(status.lastSync)],
    ["Venues", venuesCount],
    ["Sessions", sessionsCount],
  ];

  return (
    <section className="summary-grid">
      {cards.map(([label, value]) => (
        <article className="summary-card" key={label}>
          <span>{label}</span>
          <strong>{value}</strong>
        </article>
      ))}
    </section>
  );
}

export default SyncSummary;

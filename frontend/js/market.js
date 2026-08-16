function formatLastSynced(isoString) {
  if (!isoString) return "Not synced yet";
  const diffMinutes = Math.floor((new Date() - new Date(isoString)) / 60000);
  if (diffMinutes < 60) return `Synced ${diffMinutes}m ago`;
  const diffHours = Math.floor(diffMinutes / 60);
  if (diffHours < 24) return `Synced ${diffHours}h ago`;
  return `Synced ${Math.floor(diffHours / 24)}d ago`;
}

async function searchMarketPrices() {
  const state = document.getElementById("stateInput").value.trim();
  const commodity = document.getElementById("commodityInput").value.trim();
  const resultsEl = document.getElementById("marketResults");
  const countEl = document.getElementById("resultCount");
  const syncedEl = document.getElementById("lastSynced");

  resultsEl.innerHTML = `<div class="empty-state"><p>Searching...</p></div>`;

  try {
    const data = await MarketAPI.get(state, commodity);
    syncedEl.textContent = formatLastSynced(data.last_synced);

    if (data.records.length === 0) {
      countEl.textContent = "";
      resultsEl.innerHTML = `
        <div class="empty-state">
          <span class="empty-state-icon">📈</span>
          <h2>No market data available yet</h2>
          <p>${data.last_synced ? "Try a different state or commodity." : "This data hasn't been synced from the source yet — check back soon, or ask an admin to run a sync."}</p>
        </div>`;
      return;
    }

    countEl.textContent = `${data.count} result${data.count !== 1 ? "s" : ""}`;

    resultsEl.innerHTML = `
      <table class="admin-table" style="width:100%;">
        <thead>
          <tr>
            <th>Commodity</th>
            <th>Variety</th>
            <th>Market</th>
            <th>State</th>
            <th>Min Price</th>
            <th>Max Price</th>
            <th>Modal Price</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          ${data.records.map(r => `
            <tr>
              <td>${r.commodity || "-"}</td>
              <td>${r.variety || "-"}</td>
              <td>${r.market || "-"}</td>
              <td>${r.state || "-"}</td>
              <td>₹${r.min_price ?? "-"}</td>
              <td>₹${r.max_price ?? "-"}</td>
              <td>₹${r.modal_price ?? "-"}</td>
              <td>${r.arrival_date || "-"}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    `;
  } catch (err) {
    resultsEl.innerHTML = `<div class="empty-state"><span class="empty-state-icon">⚠️</span><h2>Couldn't load market data</h2><p>${err.message}</p></div>`;
  }
}

document.getElementById("marketForm").addEventListener("submit", (e) => {
  e.preventDefault();
  searchMarketPrices();
});
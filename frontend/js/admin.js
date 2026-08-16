async function loadAdminDashboard() {
  try {
    const [stats, farmers, datasetsRes] = await Promise.all([
      AdminAPI.stats(),
      AdminAPI.farmers(),
      AdminAPI.datasets()
    ]);

    renderStats(stats);
    renderFarmers(farmers);
    renderDatasets(datasetsRes.datasets);
  } catch (err) {
    console.error("Failed to load admin dashboard:", err);
  }
}

function renderStats(stats) {
  document.getElementById("adminStats").innerHTML = `
    <div class="card stat-card">
      <div class="stat-label">Total Farmers</div>
      <div class="stat-value">${stats.total_farmers}</div>
    </div>
    <div class="card stat-card">
      <div class="stat-label">Total Farms</div>
      <div class="stat-value">${stats.total_farms}</div>
    </div>
    <div class="card stat-card">
      <div class="stat-label">Crop Records</div>
      <div class="stat-value">${stats.total_crop_records}</div>
    </div>
    <div class="card stat-card">
      <div class="stat-label">Disease Records</div>
      <div class="stat-value">${stats.total_disease_records}</div>
    </div>
  `;
}

function renderFarmers(farmers) {
  document.getElementById("farmerCount").textContent = `${farmers.length} total`;

  const table = document.getElementById("farmersTable");

  if (farmers.length === 0) {
    table.innerHTML = `<tr><td style="padding:24px; text-align:center; color:var(--color-text-faint);">No farmers registered yet.</td></tr>`;
    return;
  }

  table.innerHTML = `
    <thead>
      <tr>
        <th>Name</th>
        <th>Email</th>
        <th>Farms</th>
        <th>Joined</th>
        <th>Status</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      ${farmers.map(f => `
        <tr>
          <td>${f.full_name}</td>
          <td>${f.email}</td>
          <td>${f.farm_count}</td>
          <td>${new Date(f.joined).toLocaleDateString()}</td>
          <td>${f.is_active ? '<span style="color:var(--color-green);">Active</span>' : '<span style="color:var(--color-rust);">Deactivated</span>'}</td>
          <td style="display:flex; gap:8px;">
            <button class="btn btn-secondary" style="padding:6px 12px; font-size:0.78rem;" onclick="handleDeactivate(${f.id}, '${f.full_name}')">${f.is_active ? 'Deactivate' : 'Reactivate'}</button>
            <button class="btn btn-secondary" style="padding:6px 12px; font-size:0.78rem;" onclick="handlePromote(${f.id}, '${f.full_name}')">Promote</button>
          </td>
        </tr>
      `).join("")}
    </tbody>
  `;
}

async function handleDeactivate(id, name) {
  if (!confirm(`Toggle active status for ${name}?`)) return;
  try {
    await AdminAPI.deactivateFarmer(id);
    loadAdminDashboard();
  } catch (err) {
    alert("Failed: " + err.message);
  }
}

async function handlePromote(id, name) {
  if (!confirm(`Promote ${name} to admin? This cannot be undone from the UI.`)) return;
  try {
    await AdminAPI.promoteFarmer(id);
    loadAdminDashboard();
  } catch (err) {
    alert("Failed: " + err.message);
  }
}

function renderDatasets(datasets) {
  const container = document.getElementById("datasetsCard");

  if (datasets.length === 0) {
    container.innerHTML = `
      <p style="color:var(--color-text-dim); font-size:0.9rem;">
        No datasets uploaded yet. Add files to <code>ml/datasets/raw/</code> to begin the ML training phase.
      </p>`;
    return;
  }

  container.innerHTML = `<div style="display:flex; flex-wrap:wrap; gap:10px;">
    ${datasets.map(d => `<span class="dataset-pill">📄 ${d}</span>`).join("")}
  </div>`;
}
async function syncMarketPrices() {
  const btn = document.getElementById("syncMarketBtn");
  btn.disabled = true;
  btn.textContent = "Syncing...";

  try {
    const result = await AdminAPI.syncMarketPrices();
    alert(`${result.success ? "✅" : "⚠️"} ${result.message}`);
  } catch (err) {
    alert("Sync failed: " + err.message);
  } finally {
    btn.disabled = false;
    btn.textContent = "Sync Market Prices";
  }
}
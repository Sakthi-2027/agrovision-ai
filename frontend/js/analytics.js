function renderStatCards(data) {
  document.getElementById("analyticsStats").innerHTML = `
    <div class="card stat-card">
      <div class="stat-label">Total Farms</div>
      <div class="stat-value">${data.total_farms}</div>
    </div>
    <div class="card stat-card">
      <div class="stat-label">Crop Records</div>
      <div class="stat-value">${data.total_crop_records}</div>
    </div>
    <div class="card stat-card">
      <div class="stat-label">Fertilizer Records</div>
      <div class="stat-value">${data.total_fertilizer_records}</div>
    </div>
    <div class="card stat-card">
      <div class="stat-label">Disease Records</div>
      <div class="stat-value">${data.total_disease_records}</div>
    </div>
  `;
}

// Shared dark-theme chart styling so charts match the design system
const CHART_COLORS = ["#7CB342", "#E0A94C", "#4FA3C7", "#C1502E", "#8A8272"];

function baseChartOptions() {
  return {
    responsive: true,
    plugins: {
      legend: {
        position: "bottom",
        labels: { color: "#C9C3B4", font: { family: "Inter", size: 12 } }
      }
    }
  };
}

function renderCropChart(distribution) {
  const ctx = document.getElementById("cropChart");

  if (distribution.length === 0) {
    ctx.parentElement.innerHTML = `<h3>Crop Distribution</h3><p style="color:var(--color-text-faint); font-size:0.85rem;">No crop records yet.</p>`;
    return;
  }

  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: distribution.map(d => d.name),
      datasets: [{
        data: distribution.map(d => d.count),
        backgroundColor: CHART_COLORS,
        borderColor: "#1E1912",
        borderWidth: 2
      }]
    },
    options: baseChartOptions()
  });
}

function renderSeverityChart(breakdown) {
  const ctx = document.getElementById("severityChart");

  if (breakdown.length === 0) {
    ctx.parentElement.innerHTML = `<h3>Disease Severity Breakdown</h3><p style="color:var(--color-text-faint); font-size:0.85rem;">No disease records yet.</p>`;
    return;
  }

  const severityColorMap = { Low: "#7CB342", Medium: "#E0A94C", High: "#C1502E" };

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: breakdown.map(d => d.severity),
      datasets: [{
        label: "Records",
        data: breakdown.map(d => d.count),
        backgroundColor: breakdown.map(d => severityColorMap[d.severity] || "#8A8272")
      }]
    },
    options: {
      ...baseChartOptions(),
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: "#C9C3B4" }, grid: { color: "#33291D" } },
        y: { ticks: { color: "#C9C3B4", stepSize: 1 }, grid: { color: "#33291D" }, beginAtZero: true }
      }
    }
  });
}

function renderRecentActivity(activity) {
  const container = document.getElementById("recentActivity");

  if (activity.length === 0) {
    container.innerHTML = `<p style="color:var(--color-text-faint); font-size:0.85rem;">No activity yet.</p>`;
    return;
  }

  container.innerHTML = activity.map(a => `
    <div class="activity-row">
      <span>🌾 Planted <strong>${a.crop_name}</strong>${a.season ? ` (${a.season})` : ""}</span>
      <span class="activity-row-meta">${new Date(a.created_at).toLocaleDateString()}</span>
    </div>
  `).join("");
}

async function loadAnalytics() {
  try {
    const data = await AnalyticsAPI.get();
    renderStatCards(data);
    renderCropChart(data.crop_distribution);
    renderSeverityChart(data.disease_severity_breakdown);
    renderRecentActivity(data.recent_activity);
  } catch (err) {
    console.error("Failed to load analytics:", err);
  }
}
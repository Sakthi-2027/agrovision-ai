const RECOMMENDATION_COLORS = {
  "Irrigate now": "var(--color-rust)",
  "Irrigate lightly": "var(--color-amber)",
  "No irrigation needed": "var(--color-green)",
  "Skip — rain expected": "var(--color-sky)"
};

const RECOMMENDATION_ICONS = {
  "Irrigate now": "💧",
  "Irrigate lightly": "🚿",
  "No irrigation needed": "✅",
  "Skip — rain expected": "🌧️"
};

async function loadIrrigationOptions() {
  try {
    const { crop_types, soil_types } = await IrrigationAPI.options();
    document.getElementById("irrigCrop").innerHTML = crop_types.map(c => `<option value="${c}">${c}</option>`).join("");
    document.getElementById("irrigSoil").innerHTML = soil_types.map(s => `<option value="${s}">${s}</option>`).join("");
  } catch (err) {
    console.error("Failed to load irrigation options:", err);
  }
}

document.getElementById("irrigationForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const btn = document.getElementById("irrigSubmitBtn");
  const resultEl = document.getElementById("irrigResult");

  const payload = {
    crop_type: document.getElementById("irrigCrop").value,
    soil_type: document.getElementById("irrigSoil").value,
    current_moisture: document.getElementById("irrigMoisture").value,
    location: document.getElementById("irrigLocation").value.trim()
  };

  btn.disabled = true;
  btn.textContent = "Analyzing...";
  resultEl.innerHTML = "";

  try {
    const result = await IrrigationAPI.recommend(payload);
    const color = RECOMMENDATION_COLORS[result.recommendation] || "var(--color-green)";
    const icon = RECOMMENDATION_ICONS[result.recommendation] || "💧";

    resultEl.innerHTML = `
      <div class="card fade-in-up" style="padding:32px; max-width:640px;">
        <div style="text-align:center; margin-bottom:24px;">
          <div style="font-family:var(--font-mono); font-size:0.75rem; text-transform:uppercase; color:var(--color-text-faint); letter-spacing:0.06em; margin-bottom:12px;">Recommendation</div>
          <div style="font-family:var(--font-display); font-size:1.8rem; font-weight:600; color:${color}; margin-bottom:8px;">
            ${icon} ${result.recommendation}
          </div>
          <p style="color:var(--color-text-dim); font-size:0.9rem;">${result.reason}</p>
        </div>

        <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:12px; border-top:1px solid var(--color-border); padding-top:20px;">
          <div style="text-align:center;">
            <div style="font-family:var(--font-mono); font-size:0.68rem; color:var(--color-text-faint); text-transform:uppercase; margin-bottom:4px;">Soil Moisture</div>
            <div style="font-family:var(--font-display); font-size:1.2rem; font-weight:600;">${result.current_moisture}%</div>
          </div>
          <div style="text-align:center;">
            <div style="font-family:var(--font-mono); font-size:0.68rem; color:var(--color-text-faint); text-transform:uppercase; margin-bottom:4px;">Rain (2 days)</div>
            <div style="font-family:var(--font-display); font-size:1.2rem; font-weight:600;">${result.upcoming_rain_mm}mm</div>
          </div>
          <div style="text-align:center;">
            <div style="font-family:var(--font-mono); font-size:0.68rem; color:var(--color-text-faint); text-transform:uppercase; margin-bottom:4px;">Location</div>
            <div style="font-family:var(--font-display); font-size:0.9rem; font-weight:600;">${result.resolved_location || result.location}</div>
          </div>
        </div>

        ${result.weather_used ? '<p style="font-family:var(--font-mono); font-size:0.68rem; color:var(--color-text-faint); text-align:center; margin-top:16px;">⚡ Live weather data used</p>' : ''}
      </div>
    `;
  } catch (err) {
    resultEl.innerHTML = `<div class="card empty-state"><span class="empty-state-icon">⚠️</span><h2>Couldn't get recommendation</h2><p>${err.message}</p></div>`;
  } finally {
    btn.disabled = false;
    btn.textContent = "Get Recommendation";
  }
});
async function loadYieldOptions() {
  try {
    const { areas, crops } = await YieldAPI.options();
    document.getElementById("yieldArea").innerHTML = areas.map(a => `<option value="${a}">${a}</option>`).join("");
    document.getElementById("yieldCrop").innerHTML = crops.map(c => `<option value="${c}">${c}</option>`).join("");
  } catch (err) {
    console.error("Failed to load yield options:", err);
  }
}

document.getElementById("yieldForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const btn = document.getElementById("yieldSubmitBtn");
  const resultEl = document.getElementById("yieldResult");

  const payload = {
    area: document.getElementById("yieldArea").value,
    item: document.getElementById("yieldCrop").value,
    year: document.getElementById("yieldYear").value,
    avg_temp: document.getElementById("yieldTemp").value,
    rainfall: document.getElementById("yieldRainfall").value,
    pesticides: document.getElementById("yieldPesticides").value
  };

  btn.disabled = true;
  btn.textContent = "Predicting...";
  resultEl.innerHTML = "";

  try {
    const result = await YieldAPI.predict(payload);
    const tonnesPerHectare = (result.predicted_yield_hg_per_ha / 10000).toFixed(2);

    resultEl.innerHTML = `
      <div class="card fade-in-up" style="padding:32px; max-width:640px; text-align:center;">
        <div style="font-family:var(--font-mono); font-size:0.75rem; text-transform:uppercase; color:var(--color-text-faint); letter-spacing:0.06em; margin-bottom:12px;">Predicted Yield</div>
        <div style="font-family:var(--font-display); font-size:2.2rem; font-weight:600; color:var(--color-green); margin-bottom:8px;">
          📊 ${tonnesPerHectare} tonnes/ha
        </div>
        <div style="color:var(--color-text-dim); font-size:0.9rem;">(${result.predicted_yield_hg_per_ha.toLocaleString()} hg/ha)</div>
      </div>
    `;
  } catch (err) {
    resultEl.innerHTML = `<div class="card empty-state"><span class="empty-state-icon">⚠️</span><h2>Couldn't predict yield</h2><p>${err.message}</p></div>`;
  } finally {
    btn.disabled = false;
    btn.textContent = "Predict Yield";
  }
});
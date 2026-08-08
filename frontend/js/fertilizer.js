async function loadFertilizerOptions() {
  try {
    const { soil_types, crop_types } = await FertilizerAPI.options();

    document.getElementById("soilType").innerHTML = soil_types.map(s => `<option value="${s}">${s}</option>`).join("");
    document.getElementById("cropType").innerHTML = crop_types.map(c => `<option value="${c}">${c}</option>`).join("");
  } catch (err) {
    console.error("Failed to load fertilizer options:", err);
  }
}

document.getElementById("fertilizerForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const btn = document.getElementById("fertilizerSubmitBtn");
  const resultEl = document.getElementById("fertilizerResult");

  const payload = {
    soil_type: document.getElementById("soilType").value,
    crop_type: document.getElementById("cropType").value,
    temperature: document.getElementById("fTemperature").value,
    humidity: document.getElementById("fHumidity").value,
    moisture: document.getElementById("fMoisture").value,
    nitrogen: document.getElementById("fNitrogen").value,
    potassium: document.getElementById("fPotassium").value,
    phosphorous: document.getElementById("fPhosphorous").value
  };

  btn.disabled = true;
  btn.textContent = "Analyzing...";
  resultEl.innerHTML = "";

  try {
    const result = await FertilizerAPI.recommend(payload);

    resultEl.innerHTML = `
      <div class="card fade-in-up" style="padding:32px; max-width:640px; text-align:center;">
        <div style="font-family:var(--font-mono); font-size:0.75rem; text-transform:uppercase; color:var(--color-text-faint); letter-spacing:0.06em; margin-bottom:12px;">Recommended Fertilizer</div>
        <div style="font-family:var(--font-display); font-size:2.2rem; font-weight:600; color:var(--color-green); margin-bottom:12px;">
          🧪 ${result.recommended_fertilizer}
        </div>
        <div style="color:var(--color-text-dim); font-size:0.9rem;">${result.confidence}% model confidence</div>
      </div>
    `;
  } catch (err) {
    resultEl.innerHTML = `<div class="card empty-state"><span class="empty-state-icon">⚠️</span><h2>Couldn't get a recommendation</h2><p>${err.message}</p></div>`;
  } finally {
    btn.disabled = false;
    btn.textContent = "Get Recommendation";
  }
});
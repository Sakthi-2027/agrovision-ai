document.getElementById("cropForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const btn = document.getElementById("cropSubmitBtn");
  const resultEl = document.getElementById("cropResult");

  const payload = {
    nitrogen: document.getElementById("nitrogen").value,
    phosphorus: document.getElementById("phosphorus").value,
    potassium: document.getElementById("potassium").value,
    temperature: document.getElementById("temperature").value,
    humidity: document.getElementById("humidity").value,
    ph: document.getElementById("ph").value,
    rainfall: document.getElementById("rainfall").value
  };

  btn.disabled = true;
  btn.textContent = "Analyzing...";
  resultEl.innerHTML = "";

  try {
    const result = await CropAPI.recommend(payload);

    resultEl.innerHTML = `
      <div class="card fade-in-up" style="padding:32px; max-width:640px; text-align:center;">
        <div style="font-family:var(--font-mono); font-size:0.75rem; text-transform:uppercase; color:var(--color-text-faint); letter-spacing:0.06em; margin-bottom:12px;">Recommended Crop</div>
        <div style="font-family:var(--font-display); font-size:2.2rem; font-weight:600; color:var(--color-green); text-transform:capitalize; margin-bottom:12px;">
          🌾 ${result.recommended_crop}
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
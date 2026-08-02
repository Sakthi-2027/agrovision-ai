function formatDayLabel(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleDateString(undefined, { weekday: "short" });
}

function renderWeather(data) {
  const { resolved_location, current, daily } = data;

  const dailyCards = daily.time.map((date, i) => `
    <div class="card weather-day-card">
      <div class="day-label">${formatDayLabel(date)}</div>
      <div class="day-temps">
        <span class="max">${Math.round(daily.temperature_2m_max[i])}°</span> /
        <span class="min">${Math.round(daily.temperature_2m_min[i])}°</span>
      </div>
      <div class="day-rain">💧 ${daily.precipitation_sum[i]}mm</div>
    </div>
  `).join("");

  document.getElementById("weatherResults").innerHTML = `
    <div class="card weather-current fade-in-up">
      <div class="weather-current-temp">${Math.round(current.temperature_2m)}°C</div>
      <div>
        <div class="weather-current-location">${resolved_location}</div>
        <div class="weather-current-meta">
          <span>💧 ${current.relative_humidity_2m}% humidity</span>
          <span>🌬️ ${current.wind_speed_10m} km/h wind</span>
          <span>🌧️ ${current.precipitation}mm now</span>
        </div>
      </div>
    </div>
    <div class="weather-daily-grid fade-in-up">${dailyCards}</div>
  `;
}

async function fetchWeather(location) {
  const resultsEl = document.getElementById("weatherResults");
  resultsEl.innerHTML = `<div class="card empty-state"><p>Loading forecast...</p></div>`;

  try {
    const data = await WeatherAPI.get(location);
    renderWeather(data);
  } catch (err) {
    resultsEl.innerHTML = `<div class="card empty-state"><span class="empty-state-icon">⚠️</span><h2>Couldn't load forecast</h2><p>${err.message}</p></div>`;
  }
}

document.getElementById("weatherForm").addEventListener("submit", (e) => {
  e.preventDefault();
  const location = document.getElementById("locationInput").value.trim();
  if (location) fetchWeather(location);
});

// Load a default forecast on page open
window.addEventListener("DOMContentLoaded", () => fetchWeather("Tindivanam"));
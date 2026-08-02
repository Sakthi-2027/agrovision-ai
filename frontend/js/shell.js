const NAV_ITEMS = [
  { section: null, key: "dashboard", label: "Dashboard", icon: "▦", href: "dashboard.html" },
  { section: null, key: "farm-records", label: "Farm Records", icon: "◎", href: "farm-records.html" },
  { section: null, key: "analytics", label: "Analytics", icon: "◍", href: "analytics.html" },

  { section: "AI Modules", key: "crop-recommendation", label: "Crop Recommendation", icon: "✦", href: "crop-recommendation.html" },
  { section: "AI Modules", key: "fertilizer-recommendation", label: "Fertilizer Recommendation", icon: "✦", href: "fertilizer-recommendation.html" },
  { section: "AI Modules", key: "disease-detection", label: "Disease Detection", icon: "✦", href: "disease-detection.html" },
  { section: "AI Modules", key: "yield-prediction", label: "Yield Prediction", icon: "✦", href: "yield-prediction.html" },
  { section: "AI Modules", key: "irrigation", label: "Smart Irrigation", icon: "✦", href: "irrigation.html" },
  { section: "AI Modules", key: "pest-prediction", label: "Pest Prediction", icon: "✦", href: "pest-prediction.html" },
  { section: "AI Modules", key: "weather", label: "Weather Forecast", icon: "✦", href: "weather.html" },
  { section: "AI Modules", key: "market-prices", label: "Market Prices", icon: "✦", href: "market-prices.html" },
  { section: "AI Modules", key: "assistant", label: "AI Assistant", icon: "✦", href: "assistant.html" },

  { section: "Account", key: "profile", label: "Profile", icon: "◐", href: "profile.html" },
  { section: "Account", key: "notifications", label: "Notifications", icon: "◔", href: "notifications.html", badge: true },
  { section: "Account", key: "admin", label: "Admin Dashboard", icon: "⚙", href: "admin-dashboard.html" },
];

function renderSidebar(activeKey) {
  let html = `
    <div class="sidebar-brand">
      <div class="auth-brand-mark">AV</div>
      <span class="auth-brand-name">AgroVision AI</span>
    </div>
    <ul class="sidebar-nav">`;

  let lastSection = null;
  NAV_ITEMS.forEach(item => {
    if (item.section !== lastSection) {
      html += `<div class="sidebar-section-label">${item.section ?? "Main"}</div>`;
      lastSection = item.section;
    }
    const activeClass = item.key === activeKey ? "active" : "";
    const badgeHtml = item.badge ? `<span class="sidebar-badge" id="notifBadge" style="display:none;"></span>` : "";
    html += `<li class="sidebar-link ${activeClass}" onclick="window.location.href='${item.href}'">
      <span class="icon">${item.icon}</span> ${item.label} ${badgeHtml}
    </li>`;
  });

  html += `</ul>
    <div class="sidebar-footer">
      <div class="sidebar-avatar" id="userInitial">-</div>
      <div>
        <div class="sidebar-user-name" id="userName">Loading...</div>
        <div class="sidebar-user-role" id="userRole">-</div>
      </div>
      <button class="sidebar-logout" id="logoutBtn" title="Log out">⏻</button>
    </div>`;

  document.getElementById("sidebarMount").innerHTML = html;

  document.getElementById("logoutBtn").addEventListener("click", async () => {
    try { await AuthAPI.logout(); } catch (err) {}
    window.location.href = "login.html";
  });
}

async function initAppShell(activeKey) {
  renderSidebar(activeKey);

  // Fetch unread count for sidebar badge (fire and forget, don't block the page)
  NotificationAPI.list().then(data => {
    const badge = document.getElementById("notifBadge");
    if (badge) {
      badge.textContent = data.unread_count > 0 ? data.unread_count : "";
      badge.style.display = data.unread_count > 0 ? "inline-block" : "none";
    }
  }).catch(() => {});

  try {
    const user = await AuthAPI.me();
    document.getElementById("userName").textContent = user.full_name;
    document.getElementById("userRole").textContent = user.role;
    document.getElementById("userInitial").textContent = user.full_name.charAt(0).toUpperCase();
    return user;
  } catch (err) {
    window.location.href = "login.html";
    throw err;
  }
}
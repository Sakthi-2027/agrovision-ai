const CATEGORY_ICONS = {
  disease: "🔬",
  weather: "☁️",
  market: "📈",
  recommendation: "✦",
  system: "🔔"
};

function timeAgo(dateStr) {
  const seconds = Math.floor((new Date() - new Date(dateStr)) / 1000);
  if (seconds < 60) return "just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

async function loadNotifications() {
  const container = document.getElementById("notifList");

  try {
    const { unread_count, notifications } = await NotificationAPI.list();
    updateSidebarBadge(unread_count);

    if (notifications.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <span class="empty-state-icon">🔔</span>
          <h2>You're all caught up</h2>
          <p>Weather alerts, disease warnings, and market updates will show up here.</p>
        </div>`;
      return;
    }

    container.innerHTML = notifications.map(n => `
      <div class="notif-item ${n.is_read ? '' : 'unread'}" data-id="${n.id}">
        ${!n.is_read ? '<div class="unread-dot"></div>' : '<div style="width:8px;"></div>'}
        <div class="notif-icon ${n.category}">${CATEGORY_ICONS[n.category] || "🔔"}</div>
        <div style="flex:1;" onclick="handleNotifClick(${n.id}, ${n.is_read})">
          <div class="notif-title">${n.title}</div>
          <div class="notif-message">${n.message || ""}</div>
          <div class="notif-time">${timeAgo(n.created_at)}</div>
        </div>
        <button class="notif-delete" onclick="event.stopPropagation(); deleteNotif(${n.id})">🗑</button>
      </div>
    `).join("");
  } catch (err) {
    container.innerHTML = `<div class="empty-state"><p style="color:var(--color-rust);">Failed to load notifications.</p></div>`;
  }
}

async function handleNotifClick(id, alreadyRead) {
  if (alreadyRead) return;
  try {
    await NotificationAPI.markRead(id);
    loadNotifications();
  } catch (err) {
    console.error(err);
  }
}

async function deleteNotif(id) {
  try {
    await NotificationAPI.remove(id);
    loadNotifications();
  } catch (err) {
    console.error(err);
  }
}

function updateSidebarBadge(count) {
  const badgeMount = document.getElementById("notifBadge");
  if (!badgeMount) return;
  badgeMount.textContent = count > 0 ? count : "";
  badgeMount.style.display = count > 0 ? "inline-block" : "none";
}
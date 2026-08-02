let editingFarmId = null;

function farmCardHtml(farm) {
  return `
    <div class="card module-card" style="cursor:default;" data-farm-id="${farm.id}">
      <span class="module-icon">🚜</span>
      <h3>${farm.farm_name}</h3>
      <p>${farm.location || "No location set"}</p>
      <div class="farm-card-meta">
        <span>${farm.size_in_acres ? farm.size_in_acres + " acres" : "Size not set"}</span>
        <span>${farm.soil_type || "Soil not set"}</span>
      </div>
      <div class="farm-card-actions">
        <button class="btn btn-secondary" onclick="openDetailModal(${farm.id})">View</button>
        <button class="btn btn-secondary" onclick="openEditModal(${farm.id})">Edit</button>
        <button class="btn btn-secondary" onclick="confirmDeleteFarm(${farm.id})">Delete</button>
      </div>
    </div>`;
}

async function loadFarms() {
  const grid = document.getElementById("farmsGrid");
  const emptyState = document.getElementById("farmsEmptyState");

  try {
    const farms = await FarmAPI.list();

    if (farms.length === 0) {
      grid.innerHTML = "";
      emptyState.style.display = "flex";
      return;
    }

    emptyState.style.display = "none";
    grid.innerHTML = farms.map(farmCardHtml).join("");
    window._farmsCache = farms; // used by edit modal to prefill values
  } catch (err) {
    console.error("Failed to load farms:", err);
  }
}

function openAddModal() {
  editingFarmId = null;
  document.getElementById("modalTitle").textContent = "Add Farm";
  document.getElementById("farmForm").reset();
  document.getElementById("modalStatus").textContent = "";
  document.getElementById("farmModal").style.display = "flex";
}

function openEditModal(farmId) {
  const farm = window._farmsCache.find(f => f.id === farmId);
  if (!farm) return;

  editingFarmId = farmId;
  document.getElementById("modalTitle").textContent = "Edit Farm";
  document.getElementById("farmName").value = farm.farm_name;
  document.getElementById("farmLocation").value = farm.location || "";
  document.getElementById("farmSize").value = farm.size_in_acres || "";
  document.getElementById("farmSoil").value = farm.soil_type || "";
  document.getElementById("modalStatus").textContent = "";
  document.getElementById("farmModal").style.display = "flex";
}

function closeModal() {
  document.getElementById("farmModal").style.display = "none";
}

async function confirmDeleteFarm(farmId) {
  const farm = window._farmsCache.find(f => f.id === farmId);
  const confirmed = confirm(`Delete "${farm.farm_name}"? This cannot be undone.`);
  if (!confirmed) return;

  try {
    await FarmAPI.remove(farmId);
    loadFarms();
  } catch (err) {
    alert("Failed to delete farm: " + err.message);
  }
}

document.getElementById("addFarmBtn").addEventListener("click", openAddModal);
document.getElementById("cancelModalBtn").addEventListener("click", closeModal);

document.getElementById("farmForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const saveBtn = document.getElementById("saveFarmBtn");
  const statusEl = document.getElementById("modalStatus");

  const payload = {
    farm_name: document.getElementById("farmName").value.trim(),
    location: document.getElementById("farmLocation").value.trim(),
    size_in_acres: parseFloat(document.getElementById("farmSize").value) || null,
    soil_type: document.getElementById("farmSoil").value.trim()
  };

  saveBtn.disabled = true;
  saveBtn.textContent = "Saving...";

  try {
    if (editingFarmId) {
      await FarmAPI.update(editingFarmId, payload);
    } else {
      await FarmAPI.create(payload);
    }
    closeModal();
    loadFarms();
  } catch (err) {
    statusEl.textContent = err.message;
    statusEl.className = "auth-status error";
  } finally {
    saveBtn.disabled = false;
    saveBtn.textContent = "Save Farm";
  }
});

let currentDetailFarmId = null;
let currentTab = "crop";

async function openDetailModal(farmId) {
  currentDetailFarmId = farmId;
  currentTab = "crop";

  const farm = window._farmsCache.find(f => f.id === farmId);
  document.getElementById("detailFarmName").textContent = farm.farm_name;

  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.tab === "crop");
  });

  document.getElementById("detailModal").style.display = "flex";
  await renderTabContent();
}

function closeDetailModal() {
  document.getElementById("detailModal").style.display = "none";
}

function switchTab(tab) {
  currentTab = tab;
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.tab === tab);
  });
  renderTabContent();
}

const TAB_CONFIG = {
  crop: {
    list: () => HistoryAPI.cropList(currentDetailFarmId),
    create: (data) => HistoryAPI.cropCreate(currentDetailFarmId, data),
    remove: (id) => HistoryAPI.cropDelete(currentDetailFarmId, id),
    mainField: "crop_name",
    metaFields: ["season", "planting_date"],
    formFields: [
      { key: "crop_name", placeholder: "Crop name", required: true },
      { key: "season", placeholder: "Season (e.g. Kharif)" },
      { key: "planting_date", placeholder: "Planting date", type: "date" }
    ]
  },
  fertilizer: {
    list: () => HistoryAPI.fertilizerList(currentDetailFarmId),
    create: (data) => HistoryAPI.fertilizerCreate(currentDetailFarmId, data),
    remove: (id) => HistoryAPI.fertilizerDelete(currentDetailFarmId, id),
    mainField: "fertilizer_name",
    metaFields: ["quantity", "unit"],
    formFields: [
      { key: "fertilizer_name", placeholder: "Fertilizer name", required: true },
      { key: "quantity", placeholder: "Quantity", type: "number" },
      { key: "unit", placeholder: "Unit (e.g. kg)" }
    ]
  },
  disease: {
    list: () => HistoryAPI.diseaseList(currentDetailFarmId),
    create: (data) => HistoryAPI.diseaseCreate(currentDetailFarmId, data),
    remove: (id) => HistoryAPI.diseaseDelete(currentDetailFarmId, id),
    mainField: "disease_name",
    metaFields: ["crop_affected", "severity"],
    formFields: [
      { key: "disease_name", placeholder: "Disease name", required: true },
      { key: "crop_affected", placeholder: "Crop affected" },
      { key: "severity", placeholder: "Severity (Low/Medium/High)" }
    ]
  }
};

async function renderTabContent() {
  const config = TAB_CONFIG[currentTab];
  const container = document.getElementById("tabContent");
  container.innerHTML = "<p style='color:var(--color-text-faint); font-size:0.85rem;'>Loading...</p>";

  try {
    const records = await config.list();

    const rowsHtml = records.length === 0
      ? `<p style="color:var(--color-text-faint); font-size:0.85rem; padding:12px 0;">No records yet.</p>`
      : records.map(r => `
          <div class="history-row">
            <div>
              <div class="history-row-main">${r[config.mainField] || "-"}</div>
              <div class="history-row-meta">${config.metaFields.map(f => r[f]).filter(Boolean).join(" · ") || "-"}</div>
            </div>
            <button class="history-row-delete" onclick="deleteHistoryRecord(${r.id})">🗑</button>
          </div>
        `).join("");

    const formHtml = `
      <form class="quick-add-form" onsubmit="return submitHistoryForm(event)">
        ${config.formFields.map(f => `
          <input class="field-input" type="${f.type || 'text'}" name="${f.key}" placeholder="${f.placeholder}" ${f.required ? "required" : ""}>
        `).join("")}
        <button type="submit" class="btn btn-primary">Add</button>
      </form>
    `;

    container.innerHTML = rowsHtml + formHtml;
  } catch (err) {
    container.innerHTML = `<p style="color:var(--color-rust); font-size:0.85rem;">Failed to load: ${err.message}</p>`;
  }
}

async function submitHistoryForm(event) {
  event.preventDefault();
  const form = event.target;
  const config = TAB_CONFIG[currentTab];

  const payload = {};
  config.formFields.forEach(f => {
    const value = form.elements[f.key].value.trim();
    if (value) payload[f.key] = value;
  });

  try {
    await config.create(payload);
    await renderTabContent();
  } catch (err) {
    alert("Failed to add record: " + err.message);
  }
  return false;
}

async function deleteHistoryRecord(recordId) {
  const config = TAB_CONFIG[currentTab];
  if (!confirm("Delete this record?")) return;

  try {
    await config.remove(recordId);
    await renderTabContent();
  } catch (err) {
    alert("Failed to delete: " + err.message);
  }
}
const API_BASE = "http://127.0.0.1:5000/api";

async function apiRequest(path, method = "GET", body = null) {
  const options = {
    method,
    headers: { "Content-Type": "application/json" },
    credentials: "include" // sends/receives the session cookie
  };
  if (body) options.body = JSON.stringify(body);

  const response = await fetch(`${API_BASE}${path}`, options);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Something went wrong");
  }
  return data;
}

const AuthAPI = {
  register: (fullName, email, password) =>
    apiRequest("/auth/register", "POST", { full_name: fullName, email, password }),

  login: (email, password) =>
    apiRequest("/auth/login", "POST", { email, password }),

  logout: () => apiRequest("/auth/logout", "POST"),

  me: () => apiRequest("/auth/me", "GET")
};
const FarmAPI = {
  list: () => apiRequest("/farms", "GET"),
  create: (farm) => apiRequest("/farms", "POST", farm),
  update: (id, farm) => apiRequest(`/farms/${id}`, "PUT", farm),
  remove: (id) => apiRequest(`/farms/${id}`, "DELETE")
};
const WeatherAPI = {
  get: (location) => apiRequest(`/weather?location=${encodeURIComponent(location)}`, "GET")
};
const HistoryAPI = {
  cropList: (farmId) => apiRequest(`/farms/${farmId}/crop-history`, "GET"),
  cropCreate: (farmId, data) => apiRequest(`/farms/${farmId}/crop-history`, "POST", data),
  cropDelete: (farmId, id) => apiRequest(`/farms/${farmId}/crop-history/${id}`, "DELETE"),

  fertilizerList: (farmId) => apiRequest(`/farms/${farmId}/fertilizer-history`, "GET"),
  fertilizerCreate: (farmId, data) => apiRequest(`/farms/${farmId}/fertilizer-history`, "POST", data),
  fertilizerDelete: (farmId, id) => apiRequest(`/farms/${farmId}/fertilizer-history/${id}`, "DELETE"),

  diseaseList: (farmId) => apiRequest(`/farms/${farmId}/disease-history`, "GET"),
  diseaseCreate: (farmId, data) => apiRequest(`/farms/${farmId}/disease-history`, "POST", data),
  diseaseDelete: (farmId, id) => apiRequest(`/farms/${farmId}/disease-history/${id}`, "DELETE")
};
const NotificationAPI = {
  list: () => apiRequest("/notifications", "GET"),
  markRead: (id) => apiRequest(`/notifications/${id}/read`, "PATCH"),
  remove: (id) => apiRequest(`/notifications/${id}`, "DELETE")
};
const AnalyticsAPI = {
  get: () => apiRequest("/analytics", "GET")
};
const AdminAPI = {
  stats: () => apiRequest("/admin/stats", "GET"),
  farmers: () => apiRequest("/admin/farmers", "GET"),
  datasets: () => apiRequest("/admin/datasets", "GET")
};
const MarketAPI = {
  get: (state, commodity) => {
    const params = new URLSearchParams();
    if (state) params.append("state", state);
    if (commodity) params.append("commodity", commodity);
    return apiRequest(`/market-prices?${params.toString()}`, "GET");
  }
};
AuthAPI.updateProfile = (payload) => apiRequest("/auth/profile", "PUT", payload);
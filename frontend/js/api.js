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
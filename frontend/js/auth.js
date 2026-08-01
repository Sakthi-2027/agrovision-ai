function showStatus(message, type = "error") {
  const el = document.getElementById("statusMsg");
  el.textContent = message;
  el.className = `auth-status ${type}`;
}

function setLoading(button, isLoading, idleText) {
  button.disabled = isLoading;
  button.textContent = isLoading ? "Please wait..." : idleText;
}

// ---- LOGIN ----
const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const btn = document.getElementById("loginBtn");

    setLoading(btn, true, "Log in");
    showStatus("", "error");

    try {
      await AuthAPI.login(email, password);
      showStatus("Login successful — redirecting...", "success");
      setTimeout(() => { window.location.href = "dashboard.html"; }, 600);
    } catch (err) {
      showStatus(err.message, "error");
      setLoading(btn, false, "Log in");
    }
  });
}

// ---- REGISTER ----
const registerForm = document.getElementById("registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fullName = document.getElementById("full_name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const btn = document.getElementById("registerBtn");

    setLoading(btn, true, "Create account");
    showStatus("", "error");

    try {
      await AuthAPI.register(fullName, email, password);
      showStatus("Account created — redirecting to login...", "success");
      setTimeout(() => { window.location.href = "login.html"; }, 900);
    } catch (err) {
      showStatus(err.message, "error");
      setLoading(btn, false, "Create account");
    }
  });
}
(async function initDashboard() {
  try {
    const user = await AuthAPI.me();

    document.getElementById("welcomeHeading").textContent = `Welcome back, ${user.full_name.split(" ")[0]}`;
    document.getElementById("userName").textContent = user.full_name;
    document.getElementById("userRole").textContent = user.role;
    document.getElementById("userInitial").textContent = user.full_name.charAt(0).toUpperCase();

  } catch (err) {
    
    window.location.href = "login.html";
  }
})();

document.getElementById("logoutBtn").addEventListener("click", async () => {
  try {
    await AuthAPI.logout();
  } catch (err) {
    
  }
  window.location.href = "login.html";
});
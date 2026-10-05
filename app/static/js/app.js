document.addEventListener("DOMContentLoaded", () => {
  const toastElement = document.getElementById("appToast");
  const toastTitle = document.getElementById("toastTitle");
  const toastContent = document.getElementById("toastContent");

  const toneClasses = {
    success: "text-bg-success",
    danger: "text-bg-danger",
    warning: "text-bg-warning",
    info: "text-bg-primary",
  };

  const showToast = (title, message, type = "info") => {
    if (!toastElement || !toastTitle || !toastContent || !window.bootstrap?.Toast) return;

    const safeType = toneClasses[type] ? type : "info";
    toastElement.className = "toast show";
    toastElement.classList.add(toneClasses[safeType]);
    toastTitle.textContent = title;
    toastContent.textContent = message;

    const toast = bootstrap.Toast.getOrCreateInstance(toastElement);
    toast.show();
  };

  const alertTone = (alert) => {
    if (alert.classList.contains("alert-success")) return "success";
    if (alert.classList.contains("alert-danger")) return "danger";
    if (alert.classList.contains("alert-warning")) return "warning";
    return "info";
  };

  const alertTitle = (type) => {
    if (type === "success") return "Success";
    if (type === "danger") return "Action needed";
    if (type === "warning") return "Warning";
    return "Notice";
  };

  document.querySelectorAll(".alert").forEach((alert) => {
    const message = alert.textContent.replace(/\s+/g, " ").trim();
    if (!message || alert.dataset.toastified === "true") return;

    alert.dataset.toastified = "true";
    const type = alertTone(alert);
    const title = alertTitle(type);
    setTimeout(() => showToast(title, message, type), 150);
  });

  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", () => {
      const submitButtons = form.querySelectorAll("button[type='submit'], input[type='submit']");
      submitButtons.forEach((button) => {
        button.disabled = true;
        button.setAttribute("aria-busy", "true");
      });
    });
  });
});

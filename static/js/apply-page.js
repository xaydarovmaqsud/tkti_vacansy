(function () {
  "use strict";

  function loadVacancies() {
    var el = document.getElementById("vacancies-data");
    if (!el) return [];
    try {
      return JSON.parse(el.textContent);
    } catch {
      return [];
    }
  }

  function formatDate(iso) {
    if (!iso) return "—";
    try {
      return new Date(iso + "T12:00:00").toLocaleDateString(undefined, {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    } catch {
      return iso;
    }
  }

  function vacancyById(id, list) {
    if (id == null || id === "") return null;
    return (
      list.find(function (v) {
        return String(v.id) === String(id);
      }) || null
    );
  }

  function escapeHtml(text) {
    if (text == null) return "";
    var div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  function initApplyPage() {
    var select = document.getElementById("vacancy-select");
    var sidebarSummary = document.getElementById("sidebar-summary");
    var detailsBlock = document.getElementById("role-details");
    if (!select || !sidebarSummary) return;

    var vacancies = loadVacancies();

    function updateSidebar() {
      var v = vacancyById(select.value, vacancies);
      if (!v) {
        sidebarSummary.innerHTML = "<p>Tafsilotlarni ko'rish uchun bo'sh ish o'rnini tanlang.</p>";
        return;
      }
      var typeLabel = v.type === "higher" ? "Oliy ta'lim" : "Kasbiy ta'lim";
      var badgeClass = v.type === "higher" ? "badge--he" : "badge--prof";
      sidebarSummary.innerHTML =
        "<strong>" +
        escapeHtml(v.title) +
        "</strong>" +
        "<p style=\"margin:0 0 0.5rem;color:var(--color-text-muted);font-size:0.88rem;\">" +
        escapeHtml(v.institution) +
        "</p>" +
        "<p style=\"margin:0;font-size:0.85rem;\"><span class=\"badge " +
        badgeClass +
        "\">" +
        typeLabel +
        "</span></p>" +
        "<div class=\"vacancy-summary\">" +
        "<p><strong>Bo'lim:</strong> " +
        escapeHtml(v.department) +
        "</p>" +
        "<p><strong>Ish bilan ta'minish:</strong> " +
        escapeHtml(v.employment) +
        "</p>" +
        "<p><strong>Joylashuv:</strong> " +
        escapeHtml(v.location) +
        "</p>" +
        "<p><strong>Topshirish muddati:</strong> " +
        formatDate(v.deadline) +
        "</p>" +
        "</div>";
    }

    function updateDetails() {
      if (!detailsBlock) return;
      var v = vacancyById(select.value, vacancies);
      if (!v) {
        detailsBlock.innerHTML = "";
        return;
      }
      detailsBlock.innerHTML =
        "<h2 id=\"details\">Ish tavsifi</h2>" +
        "<p style=\"margin-top:0.5rem;color:var(--color-text-muted);\">" +
        escapeHtml(v.description) +
        "</p>";
    }

    select.addEventListener("change", function () {
      updateSidebar();
      updateDetails();
    });
    updateSidebar();
    updateDetails();

    if (window.location.hash === "#details") {
      var el = document.getElementById("details");
      if (el) el.scrollIntoView({ behavior: "smooth" });
    }
  }

  document.addEventListener("DOMContentLoaded", initApplyPage);
})();

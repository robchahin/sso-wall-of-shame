(function () {
  function filterTables(query) {
    var q = query.toLowerCase().trim();
    var tables = document.querySelectorAll("table.sortable");
    tables.forEach(function (table) {
      var rows = table.querySelectorAll("tbody tr");
      var visible = 0;
      rows.forEach(function (row) {
        var nameCell = row.querySelector("td:first-child");
        if (!nameCell) return;
        var match = !q || nameCell.textContent.toLowerCase().indexOf(q) !== -1;
        row.style.display = match ? "" : "none";
        if (match) visible++;
      });
      var empty = table.nextElementSibling;
      if (empty && empty.classList.contains("search-empty")) {
        empty.style.display = visible === 0 && q ? "" : "none";
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var input = document.getElementById("vendor-search");
    if (!input) return;
    input.addEventListener("input", function () {
      filterTables(this.value);
    });
  });
})();

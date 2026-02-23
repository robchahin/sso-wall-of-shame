(function () {
  // Column indices (0-based)
  var COL_VENDOR   = 0;
  var COL_BASE     = 1;
  var COL_SSO      = 2;
  var COL_PCT      = 3;
  var COL_SOURCE   = 4;
  var COL_DATE     = 5;

  function extractNumber(text) {
    var m = text.replace(/,/g, '').match(/[\d.]+/);
    return m ? parseFloat(m[0]) : -Infinity;
  }

  function cellValue(td, colIndex) {
    var text = td.textContent.trim();
    if (colIndex === COL_BASE || colIndex === COL_SSO || colIndex === COL_PCT) {
      return extractNumber(text);
    }
    // Date column is YYYY-MM-DD — lexicographic sort is correct
    return text.toLowerCase();
  }

  function sortTable(table, colIndex, ascending) {
    var tbody = table.querySelector('tbody');
    var rows = Array.prototype.slice.call(tbody.querySelectorAll('tr'));

    rows.sort(function (a, b) {
      var aCells = a.querySelectorAll('td');
      var bCells = b.querySelectorAll('td');
      if (!aCells[colIndex] || !bCells[colIndex]) return 0;
      var aVal = cellValue(aCells[colIndex], colIndex);
      var bVal = cellValue(bCells[colIndex], colIndex);
      if (aVal < bVal) return ascending ? -1 : 1;
      if (aVal > bVal) return ascending ? 1 : -1;
      return 0;
    });

    rows.forEach(function (row) { tbody.appendChild(row); });
  }

  function updateIndicators(headers, activeIndex, ascending) {
    headers.forEach(function (th, i) {
      th.removeAttribute('aria-sort');
      var indicator = th.querySelector('.sort-indicator');
      if (indicator) indicator.textContent = '';
      if (i === activeIndex) {
        th.setAttribute('aria-sort', ascending ? 'ascending' : 'descending');
        if (indicator) indicator.textContent = ascending ? ' ▲' : ' ▼';
      }
    });
  }

  function initTable(table) {
    var headers = Array.prototype.slice.call(table.querySelectorAll('thead th'));
    var sortState = { col: -1, ascending: true };

    headers.forEach(function (th, colIndex) {
      // Add indicator span
      var indicator = document.createElement('span');
      indicator.className = 'sort-indicator';
      indicator.setAttribute('aria-hidden', 'true');
      th.appendChild(indicator);

      th.style.cursor = 'pointer';
      th.setAttribute('role', 'button');
      th.setAttribute('tabindex', '0');

      function doSort() {
        var ascending = sortState.col === colIndex ? !sortState.ascending : true;
        sortState.col = colIndex;
        sortState.ascending = ascending;
        sortTable(table, colIndex, ascending);
        updateIndicators(headers, colIndex, ascending);
      }

      th.addEventListener('click', doSort);
      th.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          doSort();
        }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var tables = document.querySelectorAll('table.sortable');
    tables.forEach(initTable);
  });
})();

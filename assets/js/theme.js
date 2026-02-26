function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
  syncButtons();
}

function syncButtons() {
  var stored = localStorage.getItem('theme');
  var effective = stored ||
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.querySelectorAll('.theme-btn').forEach(function(btn) {
    btn.classList.toggle('theme-btn--active', btn.dataset.theme === effective);
  });
}

document.addEventListener('DOMContentLoaded', function() {
  syncButtons();

  document.querySelectorAll('.theme-btn').forEach(function(btn) {
    btn.addEventListener('click', function() { setTheme(btn.dataset.theme); });
  });

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function() {
    if (!localStorage.getItem('theme')) syncButtons();
  });
});

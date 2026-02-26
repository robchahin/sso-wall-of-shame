function getEffectiveTheme() {
  var stored = localStorage.getItem('theme');
  return stored || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
}

function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('theme-toggle-btn').addEventListener('click', function() {
    setTheme(getEffectiveTheme() === 'dark' ? 'light' : 'dark');
  });
});

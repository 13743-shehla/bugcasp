/* Apply before paint; storage is optional (private browsing may block it). */
(() => {
  const key = 'bugcasp-theme';
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  let preference;
  try { preference = localStorage.getItem(key); } catch (_) {}
  if (!['light', 'dark'].includes(preference)) preference = null;
  const apply = theme => {
    document.documentElement.dataset.theme = theme;
    const button = document.getElementById('theme-toggle');
    if (button) {
      const dark = theme === 'dark';
      button.textContent = dark ? '☀ Açıq rejim' : '☾ Qaranlıq rejim';
      button.setAttribute('aria-label', dark ? 'Açıq rejimə keç' : 'Qaranlıq rejimə keç');
      button.setAttribute('aria-pressed', String(dark));
    }
  };
  apply(preference || (system.matches ? 'dark' : 'light'));
  document.addEventListener('DOMContentLoaded', () => {
    apply(document.documentElement.dataset.theme);
    document.getElementById('theme-toggle').addEventListener('click', () => {
      preference = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      apply(preference);
      try { localStorage.setItem(key, preference); } catch (_) {}
    });
  });
  system.addEventListener('change', event => { if (!preference) apply(event.matches ? 'dark' : 'light'); });
  window.addEventListener('storage', event => {
    if (event.key !== key && event.key !== null) return;
    preference = ['light', 'dark'].includes(event.newValue) ? event.newValue : null;
    apply(preference || (system.matches ? 'dark' : 'light'));
  });
})();

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('wifi-form');
  form.addEventListener('submit', () => {
    setTimeout(() => alert('Configuration Wi‑Fi enregistrée.'), 100);
  });
});
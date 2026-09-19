(() => {
  const input = document.querySelector('[data-search]');
  if (!input) return;
  const cards = [...document.querySelectorAll('[data-card]')];
  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase();
    cards.forEach(card => {
      card.hidden = q && !card.textContent.toLowerCase().includes(q);
    });
  });
})();

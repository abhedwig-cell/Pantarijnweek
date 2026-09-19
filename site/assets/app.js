(() => {
  const ALL = (() => {
    const el = document.getElementById('offerings-data');
    if (!el) return [];
    try { return JSON.parse(el.textContent || '[]'); } catch { return []; }
  })();

  const savedKey = 'pantarijnweek-saved-v2';
  const getSaved = () => {
    try { return JSON.parse(localStorage.getItem(savedKey) || '[]'); } catch { return []; }
  };
  const setSaved = ids => localStorage.setItem(savedKey, JSON.stringify([...new Set(ids)]));

  function updateSavedButtons() {
    const saved = new Set(getSaved());
    document.querySelectorAll('[data-save]').forEach(btn => {
      const active = saved.has(btn.dataset.save);
      btn.classList.toggle('saved', active);
      btn.textContent = active ? '✓ Bewaard' : '♡ Bewaar';
    });
    const count = document.querySelector('[data-saved-count]');
    if (count) count.textContent = saved.size;
  }

  document.addEventListener('click', e => {
    const save = e.target.closest('[data-save]');
    if (save) {
      const ids = getSaved();
      const id = save.dataset.save;
      setSaved(ids.includes(id) ? ids.filter(x => x !== id) : [...ids, id]);
      updateSavedButtons();
      renderSavedPage();
      return;
    }

    const detail = e.target.closest('[data-detail]');
    if (detail) {
      const item = ALL.find(o => o.offering_id === detail.dataset.detail);
      const dialog = document.getElementById('detail-dialog');
      if (!item || !dialog) return;
      dialog.querySelector('[data-dialog-title]').textContent = item.title || '';
      dialog.querySelector('[data-dialog-description]').textContent = item.description || item.short || '';
      dialog.querySelector('[data-dialog-audience]').textContent = item.audience || 'Nog te bepalen';
      dialog.querySelector('[data-dialog-location]').textContent = item.location || 'Nog te bepalen';
      dialog.querySelector('[data-dialog-category]').textContent = item.category || 'Overig';
      dialog.querySelector('[data-dialog-tags]').textContent = (item.tags || []).join(', ') || 'Geen bijzonderheden';
      const saveBtn = dialog.querySelector('[data-dialog-save]');
      saveBtn.dataset.save = item.offering_id;
      dialog.showModal();
      updateSavedButtons();
      return;
    }

    if (e.target.closest('[data-close-dialog]')) {
      document.getElementById('detail-dialog')?.close();
      return;
    }

    const filter = e.target.closest('[data-filter]');
    if (filter) {
      const root = filter.closest('[data-filter-root]') || document;
      root.querySelectorAll('[data-filter]').forEach(b => b.classList.toggle('active', b === filter));
      root.dataset.activeFilter = filter.dataset.filter;
      applyFilters(root);
    }
  });

  document.addEventListener('input', e => {
    if (!e.target.matches('[data-search]')) return;
    const root = e.target.closest('[data-filter-root]') || document;
    applyFilters(root);
  });

  function applyFilters(root) {
    const q = (root.querySelector('[data-search]')?.value || '').trim().toLowerCase();
    const active = root.dataset.activeFilter || 'all';
    root.querySelectorAll('[data-card]').forEach(card => {
      const text = card.textContent.toLowerCase();
      const audience = (card.dataset.audience || '').toLowerCase();
      const category = (card.dataset.category || '').toLowerCase();
      const tags = (card.dataset.tags || '').toLowerCase();
      const matchesQuery = !q || text.includes(q);
      const matchesFilter =
        active === 'all' ||
        audience.includes(active.toLowerCase()) ||
        category === active.toLowerCase() ||
        tags.includes(active.toLowerCase());
      card.hidden = !(matchesQuery && matchesFilter);
    });
  }

  function renderSavedPage() {
    const host = document.querySelector('[data-saved-list]');
    if (!host) return;
    const saved = getSaved();
    const items = saved.map(id => ALL.find(o => o.offering_id === id)).filter(Boolean);
    if (!items.length) {
      host.innerHTML = '<div class="empty">Je hebt nog niets bewaard. Gebruik “♡ Bewaar” bij een workshop om hier jouw voorlopige lijst te maken.</div>';
      return;
    }
    host.innerHTML = items.map(item => `
      <article class="saved-row">
        <div class="icon">${item.icon || '✦'}</div>
        <div><b>${escapeHtml(item.title || '')}</b><div class="meta">${escapeHtml(item.audience || '')} · ${escapeHtml(item.location || '')}</div></div>
        <button class="button secondary" data-save="${escapeHtml(item.offering_id)}">Verwijder</button>
      </article>`).join('');
    updateSavedButtons();
  }

  function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  }

  updateSavedButtons();
  renderSavedPage();
})();
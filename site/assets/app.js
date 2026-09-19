(() => {
  const dataEl = document.getElementById('offerings-data');
  let all = [];
  try { all = JSON.parse(dataEl?.textContent || '[]'); } catch {}
  const key = 'pantarijnweek-saved-v3';

  const saved = () => {
    try { return JSON.parse(localStorage.getItem(key) || '[]'); } catch { return []; }
  };
  const setSaved = ids => localStorage.setItem(key, JSON.stringify([...new Set(ids)]));

  function syncSaved() {
    const ids = new Set(saved());
    document.querySelectorAll('[data-save]').forEach(btn => {
      const on = ids.has(btn.dataset.save);
      btn.classList.toggle('saved', on);
      btn.textContent = on ? '✓ Bewaard' : '♡ Bewaar';
    });
    document.querySelectorAll('[data-saved-count]').forEach(el => el.textContent = ids.size);
    renderSaved();
  }

  function renderSaved() {
    const host = document.querySelector('[data-saved-list]');
    if (!host) return;
    const items = saved().map(id => all.find(x => x.offering_id === id)).filter(Boolean);
    if (!items.length) {
      host.innerHTML = '<div class="empty">Je hebt nog geen workshops bewaard. Open een workshop en kies “Bewaar”.</div>';
      return;
    }
    host.innerHTML = items.map(item => `
      <article class="saved-row">
        <div class="icon">${escapeHtml(item.icon || '✦')}</div>
        <div class="grow"><b>${escapeHtml(item.title)}</b><br><small>${escapeHtml(item.audience || '')} · ${escapeHtml(item.location || '')}</small></div>
        <button class="button secondary" data-save="${escapeHtml(item.offering_id)}">Verwijder</button>
      </article>`).join('');
  }

  function openDetail(id) {
    const item = all.find(x => x.offering_id === id);
    const d = document.getElementById('detail-dialog');
    if (!item || !d) return;
    d.querySelector('[data-dialog-title]').textContent = item.title || '';
    d.querySelector('[data-dialog-description]').textContent = item.description || item.short || '';
    d.querySelector('[data-dialog-audience]').textContent = item.audience || 'Nog te bepalen';
    d.querySelector('[data-dialog-location]').textContent = item.location || 'Nog te bepalen';
    d.querySelector('[data-dialog-special]').textContent = (item.tags || []).join(', ') || 'Geen bijzonderheden';
    const saveBtn = d.querySelector('[data-dialog-save]');
    saveBtn.dataset.save = item.offering_id;
    d.showModal();
    syncSaved();
  }

  function applySearch(root) {
    const q = (root.querySelector('[data-search]')?.value || '').toLowerCase().trim();
    const audience = root.dataset.audienceFilter || 'all';
    root.querySelectorAll('[data-card]').forEach(card => {
      const text = card.textContent.toLowerCase();
      const cardAudience = (card.dataset.audience || '').toLowerCase();
      const matchesText = !q || text.includes(q);
      const matchesAudience = audience === 'all' || cardAudience.includes(audience.toLowerCase());
      card.hidden = !(matchesText && matchesAudience);
    });
  }

  document.addEventListener('click', e => {
    const card = e.target.closest('[data-detail]');
    if (card && !e.target.closest('[data-save]')) {
      openDetail(card.dataset.detail);
      return;
    }
    const save = e.target.closest('[data-save]');
    if (save) {
      const ids = saved();
      const id = save.dataset.save;
      setSaved(ids.includes(id) ? ids.filter(x => x !== id) : [...ids, id]);
      syncSaved();
      return;
    }
    if (e.target.closest('[data-close-dialog]')) {
      document.getElementById('detail-dialog')?.close();
      return;
    }
    const seg = e.target.closest('[data-audience-filter]');
    if (seg) {
      const root = seg.closest('[data-search-root]');
      if (!root) return;
      root.dataset.audienceFilter = seg.dataset.audienceFilter;
      root.querySelectorAll('[data-audience-filter]').forEach(b => b.classList.toggle('active', b === seg));
      applySearch(root);
    }
  });

  document.addEventListener('input', e => {
    if (!e.target.matches('[data-search]')) return;
    const root = e.target.closest('[data-search-root]');
    if (root) applySearch(root);
  });

  function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  }

  syncSaved();
})();
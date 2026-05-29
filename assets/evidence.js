/**
 * Registro de evidencias EVID-P01…P06 — localStorage + IndexedDB
 */
(function () {
  'use strict';

  const META_KEY = 'guia-evidence-meta';
  const DB_NAME = 'guia-evidence-files';
  const DB_VERSION = 1;
  const STORE = 'files';
  const MAX_FILE_MB = 8;

  const MODULES = [
    { id: 'P01', label: 'P01 — Definición', items: ['spec-v1.md', 'threat-model.md', 'checklist-pre-IA'] },
    { id: 'P02', label: 'P02 — Validación', items: ['review-report.md', 'test-plan.md', 'salida de tests'] },
    { id: 'P03', label: 'P03 — Seguridad', items: ['owasp-audit.md', 'npm-audit.txt', 'lista secrets'] },
    { id: 'P04', label: 'P04 — Supervisión', items: ['ADR', 'log-supervision.md'] },
    { id: 'P05', label: 'P05 — Ética', items: ['declaracion-ia.pdf', 'LICENSES.md'] },
    { id: 'P06', label: 'P06 — Pensamiento crítico', items: ['autoeval-sesion', 'plan-practica.md'] },
  ];

  function openDb() {
    return new Promise((resolve, reject) => {
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onerror = () => reject(req.error);
      req.onsuccess = () => resolve(req.result);
      req.onupgradeneeded = (e) => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains(STORE)) {
          db.createObjectStore(STORE, { keyPath: 'id' });
        }
      };
    });
  }

  function loadMeta() {
    try {
      const raw = localStorage.getItem(META_KEY);
      return raw ? JSON.parse(raw) : { project: '', records: [] };
    } catch {
      return { project: '', records: [] };
    }
  }

  function saveMeta(data) {
    localStorage.setItem(META_KEY, JSON.stringify(data));
  }

  function uid() {
    return 'ev_' + Date.now() + '_' + Math.random().toString(36).slice(2, 9);
  }

  async function saveFileBlob(id, blob, name, type) {
    const db = await openDb();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE, 'readwrite');
      tx.objectStore(STORE).put({ id, blob, name, type, savedAt: Date.now() });
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
  }

  async function getFileBlob(id) {
    const db = await openDb();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE, 'readonly');
      const req = tx.objectStore(STORE).get(id);
      req.onsuccess = () => resolve(req.result || null);
      req.onerror = () => reject(req.error);
    });
  }

  async function deleteFileBlob(id) {
    const db = await openDb();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE, 'readwrite');
      tx.objectStore(STORE).delete(id);
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
  }

  function formatSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  }

  function renderList(meta) {
    const list = document.getElementById('evidenceList');
    const empty = document.getElementById('evidenceEmpty');
    if (!list) return;

    const moduleFilter = document.getElementById('evidenceModuleFilter')?.value || '';
    const rows = meta.records.filter((r) => !moduleFilter || r.module === moduleFilter);

    if (!rows.length) {
      list.innerHTML = '';
      if (empty) empty.hidden = false;
      return;
    }
    if (empty) empty.hidden = true;

    list.innerHTML = rows
      .map(
        (r) => `
      <article class="evidence-card" data-id="${r.id}">
        <div class="evidence-card-head">
          <span class="evidence-module-badge">EVID-${r.module}</span>
          <strong>${escapeHtml(r.title)}</strong>
        </div>
        <p class="evidence-card-meta">${escapeHtml(r.description || '')}</p>
        <div class="evidence-card-files">
          ${(r.files || [])
            .map(
              (f) =>
                `<span class="evidence-file-chip">${escapeHtml(f.name)} · ${formatSize(f.size || 0)}</span>`
            )
            .join('')}
          ${r.url ? `<a href="${escapeHtml(r.url)}" target="_blank" rel="noopener">Enlace externo</a>` : ''}
        </div>
        <div class="evidence-card-actions">
          <button type="button" class="btn btn-secondary btn-sm" data-dl="${r.id}">Descargar adjuntos</button>
          <button type="button" class="btn btn-secondary btn-sm evidence-delete" data-del="${r.id}">Eliminar</button>
        </div>
        <time class="evidence-date">${new Date(r.createdAt).toLocaleString('es-CO')}</time>
      </article>`
      )
      .join('');

    list.querySelectorAll('.evidence-delete').forEach((btn) => {
      btn.addEventListener('click', () => deleteRecord(btn.dataset.del));
    });
    list.querySelectorAll('[data-dl]').forEach((btn) => {
      btn.addEventListener('click', () => downloadRecord(btn.dataset.dl));
    });
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  async function deleteRecord(id) {
    if (!confirm('¿Eliminar esta evidencia y sus archivos?')) return;
    const meta = loadMeta();
    const rec = meta.records.find((r) => r.id === id);
    if (rec && rec.files) {
      for (const f of rec.files) {
        if (f.storeId) await deleteFileBlob(f.storeId);
      }
    }
    meta.records = meta.records.filter((r) => r.id !== id);
    saveMeta(meta);
    renderList(meta);
    updateStats(meta);
  }

  async function downloadRecord(id) {
    const meta = loadMeta();
    const rec = meta.records.find((r) => r.id === id);
    if (!rec || !rec.files?.length) return;
    for (const f of rec.files) {
      if (!f.storeId) continue;
      const stored = await getFileBlob(f.storeId);
      if (!stored?.blob) continue;
      const url = URL.createObjectURL(stored.blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = stored.name || f.name;
      a.click();
      URL.revokeObjectURL(url);
    }
  }

  function updateStats(meta) {
    const el = document.getElementById('evidenceStats');
    if (!el) return;
    const byMod = {};
    meta.records.forEach((r) => {
      byMod[r.module] = (byMod[r.module] || 0) + 1;
    });
    el.innerHTML = MODULES.map(
      (m) => `<span class="evidence-stat">${m.id}: <strong>${byMod[m.id] || 0}</strong></span>`
    ).join('');
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const module = form.module.value;
    const title = form.title.value.trim();
    const description = form.description.value.trim();
    const url = form.url.value.trim();
    const fileInput = form.files;

    if (!title) {
      alert('Indica un título para la evidencia.');
      return;
    }

    const filesMeta = [];
    if (fileInput?.files?.length) {
      for (const file of fileInput.files) {
        if (file.size > MAX_FILE_MB * 1024 * 1024) {
          alert('Archivo demasiado grande (máx. ' + MAX_FILE_MB + ' MB): ' + file.name);
          return;
        }
        const storeId = uid();
        await saveFileBlob(storeId, file, file.name, file.type);
        filesMeta.push({ name: file.name, size: file.size, storeId });
      }
    }

    const meta = loadMeta();
    meta.project = document.getElementById('evidenceProject')?.value?.trim() || meta.project;
    meta.records.unshift({
      id: uid(),
      module,
      title,
      description,
      url,
      files: filesMeta,
      createdAt: Date.now(),
    });
    saveMeta(meta);
    form.reset();
    renderList(meta);
    updateStats(meta);
    const msg = document.getElementById('evidenceFormMsg');
    if (msg) {
      msg.textContent = 'Evidencia registrada correctamente.';
      setTimeout(() => { msg.textContent = ''; }, 3000);
    }
  }

  function initModuleFilter() {
    const sel = document.getElementById('evidenceModuleFilter');
    if (!sel) return;
    MODULES.forEach((m) => {
      const o = document.createElement('option');
      o.value = m.id;
      o.textContent = m.label;
      sel.appendChild(o);
    });
    sel.addEventListener('change', () => renderList(loadMeta()));
  }

  function preselectModule() {
    const mod = new URLSearchParams(window.location.search).get('module');
    const formMod = document.querySelector('#evidenceForm [name="module"]');
    if (!mod || !formMod) return;
    const n = mod.replace(/\D/g, '').padStart(2, '0');
    if (n) formMod.value = 'P' + n;
  }

  document.addEventListener('DOMContentLoaded', () => {
    const meta = loadMeta();
    const projectInput = document.getElementById('evidenceProject');
    if (projectInput) {
      projectInput.value = meta.project || '';
      projectInput.addEventListener('change', () => {
        meta.project = projectInput.value.trim();
        saveMeta(meta);
      });
    }
    const form = document.getElementById('evidenceForm');
    if (form) form.addEventListener('submit', handleSubmit);
    initModuleFilter();
    preselectModule();
    renderList(meta);
    updateStats(meta);
  });

  window.GuiaEvidence = { loadMeta, MODULES };
})();

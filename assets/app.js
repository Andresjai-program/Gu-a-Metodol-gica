/**
 * Guía Metodológica — scripts compartidos
 */
(function () {
  'use strict';

  const STORAGE_THEME = 'guia-theme';

  function getStoredTheme() {
    try {
      return localStorage.getItem(STORAGE_THEME);
    } catch {
      return null;
    }
  }

  function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    const resolved = theme === 'dark' || theme === 'light' ? theme : getSystemTheme();
    document.documentElement.setAttribute('data-theme', resolved);
    document.querySelectorAll('.theme-toggle').forEach((btn) => {
      btn.setAttribute('aria-label', resolved === 'dark' ? 'Activar modo claro' : 'Activar modo oscuro');
      btn.setAttribute('title', resolved === 'dark' ? 'Modo claro' : 'Modo oscuro');
    });
  }

  function initTheme() {
    const stored = getStoredTheme();
    applyTheme(stored || getSystemTheme());

    document.querySelectorAll('.theme-toggle').forEach((btn) => {
      btn.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme') || getSystemTheme();
        const next = current === 'dark' ? 'light' : 'dark';
        try {
          localStorage.setItem(STORAGE_THEME, next);
        } catch { /* ignore */ }
        applyTheme(next);
      });
    });
  }

  function initLucide() {
    if (typeof lucide !== 'undefined' && lucide.createIcons) {
      lucide.createIcons({ attrs: { 'aria-hidden': 'true' } });
    }
  }

  function updateProgress() {
    const bar = document.getElementById('progress-bar');
    const scrollTop = document.getElementById('scrollTop');
    const sbFill = document.getElementById('sbFill');
    const readPct = document.getElementById('readPct');

    const scrolled = window.scrollY;
    const total = document.documentElement.scrollHeight - window.innerHeight;
    const pct = total > 0 ? (scrolled / total) * 100 : 0;

    if (bar) bar.style.width = pct + '%';
    if (sbFill) sbFill.style.width = pct + '%';
    if (readPct) readPct.textContent = Math.round(pct) + '%';
    if (scrollTop) {
      scrollTop.classList.toggle('visible', scrolled > 400);
      scrollTop.classList.toggle('vis', scrolled > 400);
    }
  }

  function initScrollProgress() {
    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
  }

  function initScrollSpy() {
    const sections = document.querySelectorAll('section[id]');
    const links = document.querySelectorAll('.sb-link[href^="#"]');
    if (!sections.length || !links.length) return;

    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            const id = e.target.id;
            links.forEach((l) => {
              l.classList.toggle('active', l.getAttribute('href') === '#' + id);
            });
          }
        });
      },
      { rootMargin: '-20% 0px -70% 0px' }
    );

    sections.forEach((s) => obs.observe(s));
  }

  function initSmoothAnchors() {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener('click', (e) => {
        const href = anchor.getAttribute('href');
        if (!href || href === '#') return;
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  window.toggleAcc = function toggleAcc(btn) {
    btn.classList.toggle('open');
    const body = btn.nextElementSibling;
    if (body) body.classList.toggle('open');
  };

  window.copyP = window.copyPrompt = function copyPrompt(btn) {
    const block = btn.closest('.prompt-block');
    const body = block && block.querySelector('.prompt-body');
    if (!body) return;
    navigator.clipboard.writeText(body.innerText).then(() => {
      const prev = btn.textContent;
      btn.textContent = 'Copiado';
      btn.classList.add('ok');
      setTimeout(() => {
        btn.textContent = prev === 'Copiado' ? 'Copiar' : prev;
        btn.classList.remove('ok');
      }, 2000);
    });
  };

  window.toggleCl = window.toggleCheck = function toggleCheck(li) {
    const box = li.querySelector('.cl-box') || li.querySelector('.checklist-box');
    if (box) box.classList.toggle('done');
    li.classList.toggle('checked');
  };

  window.toggleChar = function toggleChar(head) {
    const body = head.nextElementSibling;
    if (!body) return;
    const isOpen = body.classList.contains('open') || body.style.display === 'block';
    body.classList.toggle('open', !isOpen);
    body.style.display = isOpen ? 'none' : 'block';
    head.setAttribute('aria-expanded', String(!isOpen));
  };

  document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initLucide();
    initScrollProgress();
    initScrollSpy();
    initSmoothAnchors();
  });
})();

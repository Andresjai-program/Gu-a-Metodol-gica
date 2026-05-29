/**
 * Platform navigation — shell unificado (header + sidebar + breadcrumbs)
 */
(function () {
  'use strict';

  const FRAMEWORK_NAME = 'IA Governance Framework';
  const VERSION = 'v2.0';
  const COPYRIGHT_YEAR = '2026';

  const TOP_NAV = [
    { id: 'index', label: 'Inicio', href: 'index.html' },
    { id: 'framework', label: 'Framework', href: 'framework.html' },
    { id: 'handbook', label: 'Handbook', href: 'guide_IA.html' },
    { id: 'governance', label: 'Gobernanza HITL', href: 'governance.html' },
    { id: 'iso', label: 'Evaluación ISO', href: 'iso-evaluation.html' },
    { id: 'architecture', label: 'Arquitectura', href: 'framework.html' },
  ];

  const PAGE_META = {
    index: {
      topActive: 'index',
      section: 'Inicio',
      sidebarTitle: 'Plataforma metodológica',
      crumbs: [{ label: 'Inicio', href: '' }],
    },
    framework: {
      topActive: 'architecture',
      section: 'Arquitectura',
      sidebarTitle: 'Arquitectura del framework',
      crumbs: [
        { label: 'Inicio', href: 'index.html' },
        { label: 'Arquitectura', href: '' },
      ],
    },
    governance: {
      topActive: 'governance',
      section: 'Gobernanza HITL',
      sidebarTitle: 'Gobernanza Human-in-the-Loop',
      crumbs: [
        { label: 'Inicio', href: 'index.html' },
        { label: 'Gobernanza HITL', href: '' },
      ],
    },
    handbook: {
      topActive: 'handbook',
      section: 'Handbook metodológico',
      sidebarTitle: 'Handbook metodológico',
      crumbs: [
        { label: 'Inicio', href: 'index.html' },
        { label: 'Handbook metodológico', href: '' },
      ],
      scrollSpy: true,
    },
    iso: {
      topActive: 'iso',
      section: 'Evaluación ISO 25010',
      sidebarTitle: 'Evaluación ISO 25010',
      crumbs: [
        { label: 'Inicio', href: 'index.html' },
        { label: 'Evaluación ISO 25010', href: '' },
      ],
      scrollSpy: true,
    },
    evidence: {
      topActive: 'handbook',
      section: 'Registro de evidencias',
      sidebarTitle: 'Evidencias EVID-P01–P06',
      crumbs: [
        { label: 'Inicio', href: 'index.html' },
        { label: 'Evidencias', href: '' },
      ],
    },
  };

  /** Sidebar unificada — misma estructura en todas las páginas */
  const SIDEBAR_GROUPS = [
    {
      label: 'Introducción',
      links: [
        { label: 'Inicio', href: 'index.html', page: 'index' },
        { label: 'Objetivos', href: 'index.html#objetivos', page: 'index', hash: 'objetivos' },
        { label: 'Riesgos IA', href: 'governance.html#riesgos-ia', page: 'governance', hash: 'riesgos-ia' },
      ],
    },
    {
      label: 'Framework',
      links: [
        { label: 'Arquitectura', href: 'framework.html', page: 'framework' },
        { label: 'HITL', href: 'governance.html#hitl', page: 'governance', hash: 'hitl' },
        { label: 'Trazabilidad', href: 'framework.html#matriz', page: 'framework', hash: 'matriz' },
      ],
    },
    {
      label: 'Protocolo P01–P06',
      links: [
        { label: 'P01 Definición', href: 'guide_IA.html#paso1', page: 'handbook', hash: 'paso1' },
        { label: 'P02 Validación', href: 'guide_IA.html#paso2', page: 'handbook', hash: 'paso2' },
        { label: 'P03 Seguridad', href: 'guide_IA.html#paso3', page: 'handbook', hash: 'paso3' },
        { label: 'P04 Supervisión', href: 'guide_IA.html#paso4', page: 'handbook', hash: 'paso4' },
        { label: 'P05 Ética', href: 'guide_IA.html#paso5', page: 'handbook', hash: 'paso5' },
        { label: 'P06 Pensamiento crítico', href: 'guide_IA.html#paso6', page: 'handbook', hash: 'paso6' },
      ],
    },
    {
      label: 'Aseguramiento',
      links: [
        { label: 'ISO 25010', href: 'iso-evaluation.html', page: 'iso' },
        { label: 'OWASP', href: 'guide_IA.html#paso3', page: 'handbook', hash: 'paso3' },
        { label: 'Métricas', href: 'iso-evaluation.html#metricas', page: 'iso', hash: 'metricas' },
        { label: 'Evidencias', href: 'evidencias.html', page: 'evidence' },
        { label: 'Matriz comparativa', href: 'guide_IA.html#comparativa', page: 'handbook', hash: 'comparativa' },
      ],
    },
  ];

  const HANDBOOK_SCROLL_SECTIONS = [
    'intro', 'gobernanza', 'como-usar',
    'paso1', 'paso2', 'paso3', 'paso4', 'paso5', 'paso6',
    'iso-eval', 'comparativa', 'normativa',
    'iso-adec', 'iso-efic', 'iso-compat', 'iso-inter', 'iso-fiab', 'iso-seg', 'iso-mant', 'iso-flex', 'iso-prot',
  ];

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function renderBreadcrumb(crumbs) {
    return crumbs
      .map((c, i) => {
        const isLast = i === crumbs.length - 1;
        const sep = i > 0 ? '<span class="platform-breadcrumb-sep" aria-hidden="true">/</span>' : '';
        if (isLast || !c.href) {
          return `${sep}<span class="platform-breadcrumb-current">${escapeHtml(c.label)}</span>`;
        }
        return `${sep}<a href="${escapeHtml(c.href)}">${escapeHtml(c.label)}</a>`;
      })
      .join('');
  }

  function renderTopNav(activeId) {
    return TOP_NAV.map((item) => {
      const cls = item.id === activeId ? ' class="is-active"' : '';
      const aria = item.id === activeId ? ' aria-current="page"' : '';
      return `<a href="${item.href}"${cls}${aria}>${escapeHtml(item.label)}</a>`;
    }).join('');
  }

  function isLinkActive(link, pageId) {
    if (link.page !== pageId) return false;
    const hash = window.location.hash.replace('#', '');
    if (link.hash) return hash === link.hash;
    return !hash;
  }

  function renderSidebar(pageId, meta) {
    const groups = SIDEBAR_GROUPS.map((g) => {
      const links = g.links
        .map((l) => {
          const active = isLinkActive(l, pageId);
          const cls = active ? 'nav-link is-active' : 'nav-link';
          const isAnchor = l.href.includes('#');
          const dataHash = l.hash ? ` data-nav-hash="${l.hash}"` : '';
          return `<a class="${cls}" href="${l.href}"${dataHash}${isAnchor ? ' data-nav-anchor' : ''}>
            <span class="nav-link-dot" aria-hidden="true"></span>${escapeHtml(l.label)}
          </a>`;
        })
        .join('');
      return `<div class="nav-group"><div class="nav-group-label">${escapeHtml(g.label)}</div>${links}</div>`;
    }).join('');

    return `
      <aside class="platform-sidebar" id="platform-sidebar" aria-label="Navegación contextual">
        <div class="platform-sidebar-inner">
          <div class="platform-sidebar-meta">
            <div class="label">Sección</div>
            <div class="title">${escapeHtml(meta.sidebarTitle)}</div>
          </div>
          <nav class="platform-sidebar-nav">${groups}</nav>
        </div>
        <div class="platform-sidebar-footer">
          <div class="platform-sidebar-progress">
            <div class="platform-sidebar-progress-label">
              <span>Progreso</span><span id="readPct">0%</span>
            </div>
            <div class="platform-sidebar-progress-track">
              <div class="platform-sidebar-progress-fill" id="sbFill"></div>
            </div>
          </div>
          <div style="margin-top:var(--sp-3)">${FRAMEWORK_NAME} · ${VERSION} · ${COPYRIGHT_YEAR}</div>
        </div>
      </aside>`;
  }

  function renderSiteFooter() {
    return `
      <footer class="site-footer" id="site-footer" role="contentinfo">
        <div class="site-footer-inner">
          <div class="site-footer-grid">
            <div class="site-footer-brand">
              <a href="index.html" class="site-footer-logo">
                <span class="platform-brand-mark" aria-hidden="true"></span>
                ${escapeHtml(FRAMEWORK_NAME)}
              </a>
              <p class="site-footer-tagline">
                Guía metodológica integral para integración ética, segura y verificable de IA en el desarrollo de software.
              </p>
              <p class="site-footer-version">${escapeHtml(FRAMEWORK_NAME)} · ${VERSION}</p>
            </div>
            <div class="site-footer-col">
              <h4>Documentación</h4>
              <ul>
                <li><a href="index.html">Inicio</a></li>
                <li><a href="guide_IA.html">Handbook metodológico</a></li>
                <li><a href="framework.html">Arquitectura</a></li>
                <li><a href="governance.html">Gobernanza HITL</a></li>
                <li><a href="pasos.html">Resumen P01–P06</a></li>
              </ul>
            </div>
            <div class="site-footer-col">
              <h4>Aseguramiento</h4>
              <ul>
                <li><a href="iso-evaluation.html">Evaluación ISO 25010</a></li>
                <li><a href="evidencias.html">Registro de evidencias</a></li>
                <li><a href="guide_IA.html#paso3">Auditoría OWASP (P03)</a></li>
                <li><a href="normativa.html">Marco normativo</a></li>
              </ul>
            </div>
            <div class="site-footer-col">
              <h4>Institucional</h4>
              <ul>
                <li><span>Universidad Libre · Seccional Cúcuta</span></li>
                <li><span>Ingeniería en TIC</span></li>
                <li><span>Andrés Felipe Jaimes Carrillo</span></li>
                <li><span>PhD. Jesús Álvarez Guerrero</span></li>
                <li><span>Ing. Alix Ospino</span></li>
              </ul>
            </div>
          </div>
          <div class="site-footer-legal">
            <p><strong>Elaboración propia (${COPYRIGHT_YEAR}).</strong> Fundamentada en ISO/IEC 25010:2023, NIST AI RMF, Reglamento UE 2024/1689, Ley 1581 de 2012, Ley 23 de 1982, CONPES 4144 de 2025 e IEEE 7000:2021.</p>
          </div>
          <div class="site-footer-bottom">
            <p class="site-footer-credit">
              Framework metodológico · Universidad Libre seccional Cúcuta · Ing. en TIC · Andrés Felipe Jaimes Carrillo · ${COPYRIGHT_YEAR}
            </p>
            <p class="site-footer-directors">
              Directores: PhD. Jesús Álvarez Guerrero · Ing. Alix Ospino
            </p>
          </div>
        </div>
      </footer>`;
  }

  function mountSiteFooter(container) {
    document.querySelectorAll('footer.footer, footer.page-footer, footer.site-footer').forEach((el) => {
      el.remove();
    });
    const wrap = document.createElement('div');
    wrap.innerHTML = renderSiteFooter().trim();
    const footer = wrap.firstElementChild;
    if (footer && container) {
      container.appendChild(footer);
    }
  }

  function renderNavSheet(activeId) {
    return TOP_NAV.map((item) => {
      const cls = item.id === activeId ? ' class="is-active"' : '';
      const aria = item.id === activeId ? ' aria-current="page"' : '';
      return `<a href="${item.href}"${cls}${aria}>${escapeHtml(item.label)}</a>`;
    }).join('');
  }

  function renderHeader(meta, topActive) {
    return `
      <header class="platform-header" id="platform-header">
        <div class="platform-header-inner">
          <div class="platform-brand">
            <a href="index.html" class="platform-brand-link">
              <span class="platform-brand-mark" aria-hidden="true"></span>
              <span>${escapeHtml(FRAMEWORK_NAME)}</span>
            </a>
            <nav class="platform-breadcrumb" aria-label="Ruta">${renderBreadcrumb(meta.crumbs)}</nav>
          </div>
          <nav class="platform-nav" aria-label="Navegación global">${renderTopNav(topActive)}</nav>
          <div class="platform-actions">
            <button type="button" class="platform-sidebar-toggle" id="sidebarToggle" aria-label="Abrir navegación lateral" aria-expanded="false" aria-controls="platform-sidebar">
              <i data-lucide="menu" class="icon-md"></i>
            </button>
            <button type="button" class="platform-nav-toggle" id="navToggle" aria-label="Abrir menú principal" aria-expanded="false" aria-controls="platform-nav-sheet">
              <i data-lucide="layout-grid" class="icon-md"></i>
            </button>
            <div class="platform-quick" aria-label="Accesos rápidos">
              <a href="governance.html#hitl" title="Gobernanza HITL">HITL</a>
              <a href="iso-evaluation.html" title="Evaluación ISO 25010">ISO</a>
            </div>
            <span class="platform-version" title="Versión del framework">${VERSION}</span>
            <button type="button" class="theme-toggle" aria-label="Cambiar tema" aria-pressed="false">
              <i data-lucide="moon" class="icon-md theme-icon-dark" aria-hidden="true"></i>
              <i data-lucide="sun" class="icon-md theme-icon-light" aria-hidden="true"></i>
            </button>
          </div>
        </div>
        <nav class="platform-nav-sheet" id="platform-nav-sheet" aria-label="Menú principal" aria-hidden="true">
          ${renderNavSheet(topActive)}
        </nav>
      </header>`;
  }

  function removeLegacyChrome() {
    document.querySelectorAll('.header:not(.platform-header)').forEach((el) => el.remove());
    document.querySelectorAll('.doc-mobile-nav').forEach((el) => el.remove());
    document.querySelectorAll('.shell > .sidebar, .shell > nav.sidebar').forEach((el) => el.remove());
    document.querySelectorAll('main .breadcrumb, .main-container > .breadcrumb').forEach((el) => el.remove());
    const shell = document.querySelector('.shell');
    if (shell) {
      shell.classList.remove('shell');
    }
  }

  function buildPlatform() {
    const pageId = document.body.getAttribute('data-page');
    if (!pageId || !PAGE_META[pageId]) return;

    const meta = PAGE_META[pageId];
    removeLegacyChrome();

    let contentEl =
      document.querySelector('[data-platform-content]') ||
      document.querySelector('main.main, main.main-container') ||
      document.querySelector('main');

    if (!contentEl) return;

    const scrollTop = document.getElementById('scrollTop');
    const progressBar = document.getElementById('progress-bar');

    const platform = document.createElement('div');
    platform.className = 'platform';
    platform.innerHTML = renderHeader(meta, meta.topActive);

    const bodyWrap = document.createElement('div');
    bodyWrap.className = 'platform-body';
    bodyWrap.innerHTML = renderSidebar(pageId, meta);

    const contentWrap = document.createElement('div');
    contentWrap.className = 'platform-content';
    contentWrap.id = 'platform-content';

    const parent = contentEl.parentNode;
    parent.insertBefore(platform, contentEl);
    platform.appendChild(bodyWrap);

    bodyWrap.appendChild(contentWrap);
    contentWrap.appendChild(contentEl);

    mountSiteFooter(contentWrap);

    const overlay = document.createElement('div');
    overlay.className = 'platform-overlay';
    overlay.id = 'platform-overlay';
    overlay.setAttribute('aria-hidden', 'true');
    platform.appendChild(overlay);

    if (progressBar && !document.body.contains(progressBar)) {
      document.body.prepend(progressBar);
    }
    if (scrollTop) {
      document.body.appendChild(scrollTop);
    }

    document.body.classList.add('platform-active', 'platform-ready');

    if (typeof lucide !== 'undefined' && lucide.createIcons) {
      lucide.createIcons({ attrs: { 'aria-hidden': 'true' } });
    }

    initDrawerNavigation();
    if (meta.scrollSpy) {
      initPlatformScrollSpy(pageId);
    }
    window.addEventListener('hashchange', () => refreshSidebarActive(pageId));
    window.addEventListener('resize', debounce(closeAllDrawers, 150));
  }

  function debounce(fn, ms) {
    let t;
    return function () {
      clearTimeout(t);
      t = setTimeout(fn, ms);
    };
  }

  function isDrawerViewport() {
    return window.matchMedia('(max-width: 1023px)').matches;
  }

  function closeAllDrawers() {
    document.body.classList.remove('sidebar-open', 'nav-open');
    const sidebarBtn = document.getElementById('sidebarToggle');
    const navBtn = document.getElementById('navToggle');
    const navSheet = document.getElementById('platform-nav-sheet');
    if (sidebarBtn) sidebarBtn.setAttribute('aria-expanded', 'false');
    if (navBtn) navBtn.setAttribute('aria-expanded', 'false');
    if (navSheet) navSheet.setAttribute('aria-hidden', 'true');
  }

  function initDrawerNavigation() {
    const sidebarBtn = document.getElementById('sidebarToggle');
    const navBtn = document.getElementById('navToggle');
    const overlay = document.getElementById('platform-overlay');
    const navSheet = document.getElementById('platform-nav-sheet');

    const closeSidebar = () => {
      document.body.classList.remove('sidebar-open');
      sidebarBtn?.setAttribute('aria-expanded', 'false');
    };

    const closeNav = () => {
      document.body.classList.remove('nav-open');
      navBtn?.setAttribute('aria-expanded', 'false');
      if (navSheet) navSheet.setAttribute('aria-hidden', 'true');
    };

    const closeAll = () => {
      closeSidebar();
      closeNav();
    };

    sidebarBtn?.addEventListener('click', () => {
      const willOpen = !document.body.classList.contains('sidebar-open');
      closeNav();
      document.body.classList.toggle('sidebar-open', willOpen);
      sidebarBtn.setAttribute('aria-expanded', String(willOpen));
      if (navSheet && willOpen) navSheet.setAttribute('aria-hidden', 'true');
    });

    navBtn?.addEventListener('click', () => {
      const willOpen = !document.body.classList.contains('nav-open');
      closeSidebar();
      document.body.classList.toggle('nav-open', willOpen);
      navBtn.setAttribute('aria-expanded', String(willOpen));
      if (navSheet) navSheet.setAttribute('aria-hidden', String(!willOpen));
    });

    overlay?.addEventListener('click', closeAll);

    document.querySelectorAll('.platform-sidebar .nav-link').forEach((a) => {
      a.addEventListener('click', () => {
        if (isDrawerViewport()) closeSidebar();
      });
    });

    navSheet?.querySelectorAll('a').forEach((a) => {
      a.addEventListener('click', () => {
        if (isDrawerViewport()) closeNav();
      });
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeAll();
    });
  }

  function refreshSidebarActive(pageId) {
    document.querySelectorAll('.platform-sidebar .nav-link').forEach((el) => {
      const href = el.getAttribute('href') || '';
      const hash = href.includes('#') ? href.split('#')[1] : '';
      const linkPage =
        href.startsWith('index') ? 'index'
        : href.startsWith('framework') ? 'framework'
        : href.startsWith('governance') ? 'governance'
        : href.startsWith('guide_IA') ? 'handbook'
        : href.startsWith('iso-evaluation') ? 'iso'
        : href.startsWith('evidencias') ? 'evidence'
        : '';
      const active =
        linkPage === pageId &&
        (hash ? window.location.hash === '#' + hash : !window.location.hash);
      el.classList.toggle('is-active', active);
      if (!active) el.classList.remove('is-active-scroll');
    });
  }

  function initPlatformScrollSpy(pageId) {
    const sectionIds =
      pageId === 'handbook'
        ? HANDBOOK_SCROLL_SECTIONS
        : ['metricas', 'iso-adec', 'iso-efic', 'iso-compat', 'iso-inter', 'iso-fiab', 'iso-seg', 'iso-mant', 'iso-flex', 'iso-prot'];

    const sections = sectionIds
      .map((id) => document.getElementById(id))
      .filter(Boolean);

    const sidebarLinks = document.querySelectorAll('.platform-sidebar .nav-link[data-nav-hash]');

    if (!sections.length) return;

    const byHash = new Map();
    sidebarLinks.forEach((link) => {
      const h = link.getAttribute('data-nav-hash');
      if (h) byHash.set(h, link);
    });

    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          const id = e.target.id;
          sidebarLinks.forEach((l) => {
            l.classList.remove('is-active-scroll');
          });
          document.querySelectorAll('.platform-sidebar .nav-link.is-active').forEach((l) => {
            if (!l.dataset.navHash) l.classList.remove('is-active');
          });
          const link = byHash.get(id);
          if (link) {
            link.classList.add('is-active-scroll');
            link.classList.add('is-active');
          }
        });
      },
      { rootMargin: '-15% 0px -65% 0px', threshold: 0 }
    );

    sections.forEach((s) => obs.observe(s));

    document.querySelectorAll('section[id]').forEach((s) => {
      if (!sectionIds.includes(s.id)) obs.observe(s);
    });
  }

  function patchPageCopy() {
    document.querySelectorAll('a[href="guide_IA.html"]').forEach((a) => {
      if (/guía completa|handbook completo/i.test(a.textContent)) {
        a.textContent = 'Handbook metodológico';
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      buildPlatform();
      patchPageCopy();
    });
  } else {
    buildPlatform();
    patchPageCopy();
  }
})();

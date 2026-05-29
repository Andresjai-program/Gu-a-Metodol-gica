# -*- coding: utf-8 -*-
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HEAD = """  <link rel="stylesheet" href="assets/styles.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js" defer></script>
"""

HEADER_ACTIONS = """
    <div class="header-actions">
      <button type="button" class="theme-toggle" aria-label="Cambiar tema">
        <i data-lucide="sun-moon" class="icon-md"></i>
      </button>
    </div>"""

def patch_file(name, current_page):
    path = ROOT / name
    c = path.read_text(encoding="utf-8")
    c = re.sub(r"<style>.*?</style>\s*", "", c, flags=re.DOTALL)
    c = re.sub(
        r'<link rel="preconnect" href="https://fonts.googleapis.com">.*?rel="stylesheet">\s*',
        "",
        c,
        count=1,
        flags=re.DOTALL,
    )
    if "assets/styles.css" not in c.split("</title>")[1][:500]:
        c = c.replace("</title>", "</title>\n" + HEAD, 1)

    c = c.replace(
        '<div class="header-logo">\n      <span></span>\n      <span>Guía Metodológica</span>\n    </div>',
        '<a href="index.html" class="header-logo"><span class="header-logo-mark" aria-hidden="true"></span><span>Guía Metodológica</span></a>',
    )
    c = c.replace(
        '<div class="header-logo">\n      <span></span>\n      <span>Guía Metodológica 2025</span>\n    </div>',
        '<a href="index.html" class="header-logo"><span class="header-logo-mark" aria-hidden="true"></span><span>Guía Metodológica 2025</span></a>',
    )

    if "header-actions" not in c:
        c = c.replace("</nav>\n  </div>\n</header>", f'      <a href="guide_IA.html">Guía completa</a>\n    </nav>{HEADER_ACTIONS}\n  </div>\n</header>')

    for href, label in [
        ("index.html", "Inicio"),
        ("pasos.html", "Los 6 pasos"),
        ("iso-evaluation.html", "Evaluación ISO 25010"),
        ("normativa.html", "Normativa"),
    ]:
        if href == current_page:
            c = re.sub(
                rf'<a href="{re.escape(href)}">[^<]*</a>',
                f'<a href="{href}" aria-current="page">{label}</a>',
                c,
                count=1,
            )

    c = c.replace('<span>/</span>', '<span class="breadcrumb-sep" aria-hidden="true">/</span>')
    c = c.replace('<div class="hero-eyebrow">\n      <span>●</span>\n      <span>', '<div class="hero-eyebrow"><span>')
    c = c.replace("paso-tags", "tags")
    c = c.replace("paso-tag paso-tag-risk", "tag tag-risk")
    c = c.replace("paso-tag paso-tag-iso", "tag tag-iso")
    c = c.replace("paso-tag paso-tag-norm", "tag tag-norm")
    c = re.sub(r'<span class="tag tag-risk">⚠ ', '<span class="tag tag-risk">', c)
    c = c.replace('class="numbered-list"', 'class="nsteps"')
    c = re.sub(r"(<button class=\"acc-trigger\"[^>]*><span>)[🎯🔍🔒⚖️🧠📋]\s*", r"\1", c)
    c = c.replace('<span class="acc-arrow">▼</span>', '<span class="acc-arrow" aria-hidden="true"><i data-lucide="chevron-down" class="icon-sm"></i></span>')
    c = c.replace(">copiar</button>", ">Copiar</button>")

    if "assets/app.js" not in c:
        c = re.sub(
            r"<script>[\s\S]*?</script>\s*</body>",
            '<script src="assets/app.js"></script>\n<script src="assets/iso-eval.js"></script>\n</body>'
            if "iso-eval" in name or "iso-evaluation" in name
            else '<script src="assets/app.js"></script>\n</body>',
            c,
            count=1,
        )

    c = c.replace(
        '<button class="scroll-top" id="scrollTop" onclick="window.scrollTo({top:0,behavior:\'smooth\'})">↑</button>',
        '<button type="button" class="scroll-top" id="scrollTop" aria-label="Volver arriba" onclick="window.scrollTo({top:0,behavior:\'smooth\'})"><i data-lucide="arrow-up" class="icon-md"></i></button>',
    )

    for i in range(1, 7):
        c = c.replace(
            f'<div class="paso-card" id="paso{i}">',
            f'<article class="paso-card" data-step="{i}" id="paso{i}">',
            1,
        )
        c = c.replace(
            f'<div class="paso-num-badge">0{i}</div>',
            f'<div class="paso-num-badge" data-step="{i}">0{i}</div>',
            1,
        )

    iso_map = {
        "🎯": "target",
        "⚡": "zap",
        "🔗": "link-2",
        "🖥️": "monitor",
        "🛡️": "shield",
        "🔧": "wrench",
        "⚠️": "alert-triangle",
    }
    for em, icon in iso_map.items():
        c = c.replace(
            f'<div class="iso-char-icon">{em}</div>',
            f'<div class="iso-char-icon"><i data-lucide="{icon}" class="icon-lg"></i></div>',
        )

    path.write_text(c, encoding="utf-8")
    print("patched", name)


patch_file("pasos.html", "pasos.html")
patch_file("iso-evaluation.html", "iso-evaluation.html")
patch_file("normativa.html", "normativa.html")

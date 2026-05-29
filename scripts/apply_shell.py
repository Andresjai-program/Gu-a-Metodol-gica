#!/usr/bin/env python3
"""Aplica atributos de plataforma y limpia chrome legacy en HTML principales."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SHELL_LINKS = """  <script src="assets/theme-init.js"></script>
  <link rel="stylesheet" href="assets/shell.css">
  <link rel="stylesheet" href="assets/responsive.css">
  <style>body[data-page]:not(.platform-ready){visibility:hidden}</style>"""

THEME_INIT = """  <script src="assets/theme-init.js"></script>"""

NAV_SCRIPT = """<script src="assets/nav.js"></script>
<script src="assets/app.js"></script>"""

EXTRA_SCRIPTS = {
    "iso-evaluation.html": '<script src="assets/iso-eval.js"></script>',
    "guide_IA.html": '<script src="assets/iso-eval.js"></script>',
    "evidencias.html": '<script src="assets/evidence.js"></script>',
}

PAGES = {
    "index.html": "index",
    "framework.html": "framework",
    "governance.html": "governance",
    "guide_IA.html": "handbook",
    "iso-evaluation.html": "iso",
    "evidencias.html": "evidence",
    "pasos.html": "handbook",
    "normativa.html": "handbook",
}


def ensure_shell_css(head: str) -> str:
    if "theme-init.js" not in head:
        head = head.replace("<head>", "<head>\n" + THEME_INIT, 1)
    if "shell.css" not in head:
        head = head.replace("</head>", SHELL_LINKS.replace(THEME_INIT, "").strip() + "\n</head>", 1)
    elif "responsive.css" not in head:
        head = head.replace(
            'href="assets/shell.css">',
            'href="assets/shell.css">\n  <link rel="stylesheet" href="assets/responsive.css">',
            1,
        )
    return head


def strip_legacy_header(body: str) -> str:
    body = re.sub(
        r"<header class=\"header\">.*?</header>\s*",
        "",
        body,
        count=1,
        flags=re.DOTALL,
    )
    body = re.sub(
        r"<nav class=\"doc-mobile-nav\".*?</nav>\s*",
        "",
        body,
        count=1,
        flags=re.DOTALL,
    )
    body = re.sub(
        r"<div class=\"shell\">\s*<!--.*?SIDEBAR.*?-->\s*<nav class=\"sidebar\">.*?</nav>\s*<!--.*?MAIN.*?-->\s*",
        "",
        body,
        count=1,
        flags=re.DOTALL,
    )
    body = re.sub(r"<nav class=\"breadcrumb\".*?</nav>\s*", "", body, count=1, flags=re.DOTALL)
    body = re.sub(r"<div class=\"breadcrumb\">.*?</div>\s*", "", body, count=1, flags=re.DOTALL)
    return body


def set_body_page(html: str, page_id: str) -> str:
    if re.search(r"data-page=", html):
        return re.sub(r'data-page="[^"]*"', f'data-page="{page_id}"', html, count=1)
    return re.sub(r"<body(\s[^>]*)?>", f'<body data-page="{page_id}"\\1>', html, count=1)


def set_platform_content(html: str) -> str:
    html = re.sub(
        r"<main(\s+class=\"[^\"]+\")>",
        r'<main\1 data-platform-content>',
        html,
        count=1,
    )
    if "data-platform-content" not in html:
        html = html.replace("<main>", '<main data-platform-content>', 1)
    return html


def fix_scripts(html: str, filename: str) -> str:
    if "nav.js" not in html:
        block = NAV_SCRIPT
    else:
        block = ""
        if "app.js" not in html:
            html = html.replace(
                '<script src="assets/nav.js"></script>',
                NAV_SCRIPT,
                1,
            )
    extra = EXTRA_SCRIPTS.get(filename, "")
    if extra and extra not in html:
        html = html.replace("</body>", extra + "\n</body>", 1)
    if "nav.js" not in html:
        html = html.replace("</body>", NAV_SCRIPT + "\n" + extra + "\n</body>", 1)
    return html


def fix_guide(html: str) -> str:
    html = re.sub(
        r'<link rel="stylesheet" href="assets/framework\.css">\s*<link rel="stylesheet" href="assets/framework\.css">',
        '<link rel="stylesheet" href="assets/framework.css">',
        html,
    )
    html = re.sub(
        r"<title>.*?</title>",
        "<title>Handbook metodológico — IA Governance Framework</title>",
        html,
        count=1,
    )
    html = re.sub(r"</main>\s*</div>\s*(?=<button)", "</main>\n", html, count=1)
    return html


def fix_index_sections(html: str) -> str:
    if 'id="framework"' not in html:
        html = html.replace(
            '<section class="section">\n    <header class="section-header">\n      <p class="section-eyebrow">Qué es este framework</p>',
            '<section class="section" id="framework">\n    <header class="section-header">\n      <p class="section-eyebrow">Qué es este framework</p>',
            1,
        )
    if 'id="objetivos"' not in html:
        html = html.replace(
            '  <section class="hero">',
            '  <section class="hero" id="objetivos">',
            1,
        )
    html = html.replace("Handbook completo", "Handbook metodológico")
    html = html.replace("Handbook integral", "Handbook metodológico")
    html = html.replace(
        "<title>Framework IA — Desarrollo y auditoría de software</title>",
        "<title>Inicio — IA Governance Framework</title>",
    )
    return html


def fix_iso(html: str) -> str:
    html = re.sub(
        r"<title>.*?</title>",
        "<title>Evaluación ISO 25010 — IA Governance Framework</title>",
        html,
        count=1,
    )
    if 'id="metricas"' not in html:
        html = html.replace(
            '<div class="score-dashboard"',
            '<div class="score-dashboard" id="metricas"',
            1,
        )
    return html


def process_file(name: str, page_id: str) -> None:
    path = ROOT / name
    if not path.exists():
        print(f"skip {name}")
        return
    html = path.read_text(encoding="utf-8")
    html = ensure_shell_css(html)
    html = strip_legacy_header(html)
    html = set_body_page(html, page_id)
    html = set_platform_content(html)
    html = fix_scripts(html, name)
    if name == "guide_IA.html":
        html = fix_guide(html)
    if name == "index.html":
        html = fix_index_sections(html)
    if name == "iso-evaluation.html":
        html = fix_iso(html)
    path.write_text(encoding="utf-8", data=html)
    print(f"ok {name}")


def main():
    for name, pid in PAGES.items():
        process_file(name, pid)


if __name__ == "__main__":
    main()

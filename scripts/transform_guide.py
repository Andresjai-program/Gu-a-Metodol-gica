# -*- coding: utf-8 -*-
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
path = ROOT / "guide_IA.html"
content = path.read_text(encoding="utf-8")

content = re.sub(r"<style>.*?</style>\s*", "", content, count=1, flags=re.DOTALL)

head_links = """  <link rel="stylesheet" href="assets/styles.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js" defer></script>
"""

content = re.sub(
    r'<link rel="preconnect" href="https://fonts.googleapis.com">.*?rel="stylesheet">\s*',
    "",
    content,
    count=1,
    flags=re.DOTALL,
)

if "assets/styles.css" not in content:
    content = content.replace("</title>", "</title>\n" + head_links, 1)

mobile_nav = """
<nav class="doc-mobile-nav" aria-label="Secciones">
  <a href="#intro">Inicio</a>
  <a href="#paso1">Pasos</a>
  <a href="#iso-eval">ISO</a>
  <a href="#normativa">Normativa</a>
</nav>
"""
if "doc-mobile-nav" not in content:
    content = content.replace('<div class="shell">', mobile_nav + '\n<div class="shell">', 1)

content = content.replace(
    '<div class="alert-icon">ℹ️</div>',
    '<div class="alert-icon"><i data-lucide="info" class="icon-md"></i></div>',
)
content = content.replace(
    '<div class="alert-icon">⚠️</div>',
    '<div class="alert-icon"><i data-lucide="alert-triangle" class="icon-md"></i></div>',
)

content = re.sub(r'<span class="tag tag-risk">⚠ ', '<span class="tag tag-risk">', content)

for i in range(1, 7):
    old = f'<div class="paso-num-badge" style="background:var(--p{i}d);color:var(--p{i})">'
    new = f'<div class="paso-card" data-step="{i}">\n  <div class="paso-head">\n    <div class="paso-num-badge" data-step="{i}">'
    # Fix: only add data-step to card once
    content = content.replace(
        f'<div class="paso-card">\n  <div class="paso-head">\n    {old}',
        new,
        1,
    )

for i in range(1, 7):
    content = content.replace(
        f'<tr><td class="td-step" style="color:var(--p{i})">',
        f'<tr><td class="td-step" data-step="{i}">',
    )

content = re.sub(
    r'(<button class="acc-trigger[^"]*" onclick="toggleAcc\(this\)"><span>)[🎯🔍🔒⚖️🧠📋]\s*',
    r"\1",
    content,
)

content = content.replace(
    '<span class="acc-arrow">▼</span>',
    '<span class="acc-arrow" aria-hidden="true"><i data-lucide="chevron-down" class="icon-sm"></i></span>',
)

content = content.replace(
    """<button class="scroll-top" id="scrollTop" onclick="window.scrollTo({top:0,behavior:'smooth'})">↑</button>""",
    """<button class="scroll-top" id="scrollTop" type="button" aria-label="Volver arriba" onclick="window.scrollTo({top:0,behavior:'smooth'})"><i data-lucide="arrow-up" class="icon-md"></i></button>""",
)

iso_icons = {
    "🎯": "target",
    "⚡": "zap",
    "🔗": "link-2",
    "🖥️": "monitor",
    "🛡️": "shield",
    "🔧": "wrench",
    "⚠️": "alert-triangle",
}

for em, icon in iso_icons.items():
    content = re.sub(
        rf'<div class="iso-char-icon"[^>]*>{re.escape(em)}</div>',
        f'<div class="iso-char-icon"><i data-lucide="{icon}" class="icon-lg"></i></div>',
        content,
    )

content = re.sub(
    r"<script>[\s\S]*?</script>\s*</body>",
    '<script src="assets/app.js"></script>\n<script src="assets/iso-eval.js"></script>\n</body>',
    content,
    count=1,
)

path.write_text(content, encoding="utf-8")
print("OK", path, "lines:", len(content.splitlines()))

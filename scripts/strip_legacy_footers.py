#!/usr/bin/env python3
"""Elimina footers legacy del HTML; nav.js inyecta site-footer global."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FOOTER_RE = re.compile(
    r"\s*<footer class=\"(?:footer|page-footer)\".*?</footer>\s*",
    re.DOTALL,
)


def main():
    for path in ROOT.glob("*.html"):
        text = path.read_text(encoding="utf-8")
        new, n = FOOTER_RE.subn("\n", text)
        if n:
            path.write_text(new, encoding="utf-8")
            print(f"stripped {n} footer(s) from {path.name}")


if __name__ == "__main__":
    main()

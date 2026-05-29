#!/usr/bin/env python3
"""Corrige labels anidados inválidos en opciones ISO."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERN = re.compile(
    r'<label class="q-opt"><input type="radio" name="([^"]+)" value="(\d)"(?:\s+onchange="updateDashboard\(\)")?><label>([^<]+)</label></label>'
)


def fix(html: str) -> str:
    def repl(m):
        name, val, text = m.group(1), m.group(2), m.group(3)
        uid = f"{name}_v{val}"
        return (
            f'<span class="q-opt"><input type="radio" name="{name}" value="{val}" '
            f'id="{uid}" onchange="updateDashboard()">'
            f'<label for="{uid}">{text}</label></span>'
        )

    return PATTERN.sub(repl, html)


def main():
    for name in ("iso-evaluation.html", "guide_IA.html"):
        path = ROOT / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new = fix(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print(f"fixed {name}")
        else:
            print(f"no changes {name}")


if __name__ == "__main__":
    main()

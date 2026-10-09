#!/usr/bin/env python3
"""Inject the HTWG-IN favicon into every Marp-generated HTML file.

The icon is the HTWG-IN mark (HTWG Konstanz, Fakultät Informatik) as used on
the title slides. favicon.ico holds hand-tuned 16/32/48 px frames (bolder at
16 px for legibility), so no SVG favicon is linked (browsers would prefer it
over the tuned small frames).

Marp CLI has no option to add <link> tags to the HTML <head>, so the
GitHub Pages workflow runs this script after the Marp build. Each HTML
file gets <link rel="icon"> tags that point via a *relative* path to the
favicon files in the repository root, so they work both on GitHub Pages
(project site under /<repo>/) and when a deck is opened locally.

Usage:  python3 themes/tools/add_favicon.py [ROOT] [HTML files ...]
        (default: ROOT = repo root, all *.html files below it)
The script is idempotent: files that already contain the marker are skipped.
"""
import os
import sys
from pathlib import Path

MARKER = "<!-- htwg-favicon -->"
SKIP_DIRS = {".git", "node_modules", "out", ".cache", ".codex-temp"}


def favicon_tags(prefix: str) -> str:
    return (
        f'{MARKER}'
        f'<link rel="icon" href="{prefix}favicon.ico" sizes="any">'
        f'<link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">'
    )


def process(html: Path, root: Path) -> bool:
    text = html.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    idx = text.find("</head>")
    if idx < 0:
        return False
    rel = os.path.relpath(root, html.parent).replace(os.sep, "/")
    prefix = "" if rel == "." else rel + "/"
    html.write_text(text[:idx] + favicon_tags(prefix) + text[idx:], encoding="utf-8")
    return True


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]).resolve()
    if len(sys.argv) > 2:
        files = [Path(f).resolve() for f in sys.argv[2:]]
    else:
        files = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            files += [Path(dirpath) / f for f in filenames if f.endswith(".html")]
    changed = sum(process(f, root) for f in files)
    print(f"add_favicon: {changed} of {len(files)} HTML file(s) updated")


if __name__ == "__main__":
    main()

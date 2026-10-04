#!/usr/bin/env python3
"""Embed the slide background PNGs as data-URIs into themes/htwg.css.

Why: marp-cli inlines the theme CSS into every generated HTML/PDF, so a
relative url('htwgin-xyz.png') in the theme would be resolved relative to the
slide deck (or dropped), not relative to the CSS file. Data-URIs work locally,
in PDF export and in the GitHub Pages build.

Usage (from repo root, stdlib only):  python3 themes/tools/embed_backgrounds.py
"""
import base64, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
THEMES = os.path.dirname(HERE)
CSS = os.path.join(THEMES, 'htwg.css')
CLASSES = ['kapitel', 'kapitel-dunkel', 'inhalt', 'aufgabe', 'zitat', 'abschluss']
# extra classes that reuse a background (see themes/BACKGROUNDS.md)
ALIASES = {'kapitel': ['tools']}
BEGIN = '/* BEGIN generated backgrounds (themes/tools/embed_backgrounds.py) - do not edit */'
END = '/* END generated backgrounds */'

rules = []
for c in CLASSES:
    with open(os.path.join(THEMES, f'htwgin-{c}.png'), 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    sel = ',\n'.join(f'section.{x}' for x in [c] + ALIASES.get(c, []))
    rules.append(f'{sel} {{\n    background-image: url("data:image/png;base64,{b64}");\n}}')
block = BEGIN + '\n' + '\n'.join(rules) + '\n' + END

css = open(CSS, encoding='utf-8').read()
if BEGIN in css:
    css = re.sub(re.escape(BEGIN) + r'.*?' + re.escape(END), lambda m: block, css, flags=re.S)
else:
    css = css.rstrip('\n') + '\n\n' + block + '\n'
open(CSS, 'w', encoding='utf-8').write(css)
print(f'embedded {len(CLASSES)} backgrounds into {CSS} ({len(css)//1024} KB)')

"""Generate HTWG-IN slide background proposals matching themes/htwgin-titel.png.
Palette (sampled from htwgin-titel.png and the HTWG Google Slides master):
  teal #009B91, slate #334152, light #D9E5EC, black, white.
Grid: 133.4 px pitch, origin (188.5, 155.5) in a 1980x1114 canvas.
"""
from PIL import Image, ImageDraw
import numpy as np, os, sys

# Usage (from repo root): python3 themes/tools/make_bgs.py  [src_title_png] [out_dir]
# Requires Pillow + numpy. After regenerating, run themes/tools/embed_backgrounds.py
# to refresh the data-URIs in themes/htwg.css.
HERE = os.path.dirname(os.path.abspath(__file__))
THEMES = os.path.dirname(HERE)
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(THEMES, 'htwgin-titel.png')
OUT = sys.argv[2] if len(sys.argv) > 2 else THEMES
os.makedirs(OUT, exist_ok=True)
W, H = 1980, 1114
S = 3  # supersampling
TEAL = (0, 155, 145); SLATE = (51, 65, 82); LIGHT = (217, 229, 236)
BLACK = (0, 0, 0); WHITE = (255, 255, 255)
GX = [188.5 + 133.42 * k for k in range(13)]
GY = [155.5 + 133.4 * j for j in range(7)]
DOT_R = 2.3

# ---- header strip (logo + "Hochschule Konstanz / Fakultät Informatik") from the original
orig = np.array(Image.open(SRC).convert('RGB')).astype(float)
HEAD_H = 330
strip = orig[:HEAD_H].copy()
# erase everything except logo (x<350) and faculty text (x 1510..1730, y<190)
keep = np.zeros(strip.shape[:2], bool)
keep[100:320, 150:350] = True
keep[110:195, 1505:1735] = True
strip[~keep] = 255
# decompose into alpha + colour class (black ink vs teal ink over white)
r, g, b = strip[..., 0], strip[..., 1], strip[..., 2]
is_teal = (g - r) > 25
alpha = np.where(is_teal, 1 - r / 255.0, 1 - (r + g + b) / 765.0)
alpha = np.clip(alpha, 0, 1)

def paste_header(img, ink=BLACK, accent=TEAL):
    a = np.array(img).astype(float)
    reg = a[:HEAD_H]
    for cls, col in ((~is_teal, ink), (is_teal, accent)):
        m = (alpha * cls)[..., None]
        reg[:] = reg * (1 - m) + np.array(col, float) * m
    a[:HEAD_H] = reg
    return Image.fromarray(a.round().astype(np.uint8))

class Canvas:
    def __init__(self, bg):
        self.im = Image.new('RGB', (W * S, H * S), bg)
        self.d = ImageDraw.Draw(self.im)
    def circle(self, cx, cy, r, fill):
        self.d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=fill)
    def rect(self, x0, y0, x1, y1, fill, radius=0):
        self.d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=radius * S, fill=fill)
    def line(self, pts, fill, w):
        self.d.line([(x * S, y * S) for x, y in pts], fill=fill, width=int(w * S))
    def poly(self, pts, fill):
        self.d.polygon([(x * S, y * S) for x, y in pts], fill=fill)
    def pill(self, p0, p1, r, fill):
        """capsule from p0 to p1 with radius r (HTWG 'drop/pill' shape)"""
        (x0, y0), (x1, y1) = p0, p1
        v = np.array([x1 - x0, y1 - y0], float); n = np.array([-v[1], v[0]]) / np.linalg.norm(v) * r
        self.poly([(x0 + n[0], y0 + n[1]), (x1 + n[0], y1 + n[1]), (x1 - n[0], y1 - n[1]), (x0 - n[0], y0 - n[1])], fill)
        self.circle(x0, y0, r, fill); self.circle(x1, y1, r, fill)
    def grid(self, col, rows=range(7), cols=range(13), skip=()):
        for j in rows:
            for k in cols:
                if (k, j) in skip: continue
                self.circle(GX[k], GY[j], DOT_R, col)
    def header_dots(self, col):
        # dots of rows 0/1 as in the title background (free of logo/text area)
        skip = {(0, 0), (1, 0), (1, 1), (10, 0), (11, 0), (12, 0)}
        self.grid(col, rows=[0, 1], skip=skip)
    def done(self, name, ink=BLACK, accent=TEAL):
        im = self.im.resize((W, H), Image.LANCZOS)
        im = paste_header(im, ink, accent)
        # flat graphics -> 64-colour palette PNG (~15-25 KB, visually identical),
        # keeps the data-URIs embedded in htwg.css small
        im = im.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        p = os.path.join(OUT, name); im.save(p, dpi=(149, 149), optimize=True); print(p)

def dot(c, k, j, r, col):
    c.circle(GX[k], GY[j], r, col)

# 1) Aufgabe / Übung: light CD tone, white rounded work panel, teal "connected dots" motif
c = Canvas(LIGHT)
c.header_dots(BLACK)
c.rect(-60, 335, 1560, 1082, WHITE, radius=110)          # work panel (left, where text goes)
c.grid(BLACK, rows=range(2, 7), cols=[12])              # dot column at right
c.grid(BLACK, rows=[6], cols=[11])
path = [(12, 2), (12, 3), (11, 4), (12, 5)]
c.line([(GX[k], GY[j]) for k, j in path], BLACK, 3)
dot(c, 12, 2, 10, BLACK); dot(c, 12, 3, 30, TEAL); dot(c, 11, 4, 52, TEAL); dot(c, 12, 5, 16, BLACK)
dot(c, 11, 6, 22, SLATE)
c.done('htwgin-aufgabe.png')

# 2) Kapitel / Zwischenfolie (hell): white, big teal quarter circle bottom right, grid rows 5-6
c = Canvas(WHITE)
c.header_dots(BLACK)
c.circle(1980 + 60, 1114 + 80, 520, TEAL)
c.circle(1440, 1114 - 20, 120, LIGHT)
c.grid(BLACK, rows=[5, 6], cols=range(0, 13))
c.line([(GX[9], GY[5]), (GX[10], GY[5]), (GX[10], GY[6])], BLACK, 3)
c.grid(WHITE, rows=[5, 6], cols=range(11, 13))          # dots visible on the teal shape
dot(c, 9, 5, 12, BLACK); dot(c, 10, 6, 7, BLACK); dot(c, 8, 6, 26, SLATE)
c.circle(GX[11], GY[3], 44, LIGHT)
c.done('htwgin-kapitel.png')

# 3) Kapitel dunkel: slate bg, white logo text, big teal disc + light disc (like 'Titel dark')
c = Canvas(SLATE)
c.header_dots(WHITE)
c.circle(1760, 190, 610, TEAL)
c.circle(1380, 1010, 250, LIGHT)
dot(c, 9, 6, 60, SLATE)
c.grid(WHITE, rows=[2, 3, 4, 5, 6], cols=range(0, 13),
       skip={(k, j) for k in range(0, 8) for j in (2, 3, 4)})  # keep text zone calm
dot(c, 2, 0, 26, TEAL); dot(c, 1, 6, 18, TEAL)
c.line([(GX[11], GY[4]), (GX[11], GY[6])], BLACK, 3)
dot(c, 11, 4, 8, BLACK); dot(c, 11, 5, 14, BLACK); dot(c, 11, 6, 8, BLACK)
c.circle(GX[12], GY[2], 40, WHITE)
c.done('htwgin-kapitel-dunkel.png', ink=WHITE, accent=TEAL)

# 4) Abschluss / Fragen / Danke: white, circle cluster in right column (like 'letzte Folie')
c = Canvas(WHITE)
c.header_dots(BLACK)
c.circle(-120, 1250, 470, LIGHT)
c.grid(BLACK, rows=range(2, 7), cols=[10, 11, 12])
dot(c, 12, 3, 60, LIGHT); dot(c, 12, 5, 86, TEAL); dot(c, 10, 5, 46, SLATE)
dot(c, 10, 6, 17, BLACK); dot(c, 11, 6, 9, SLATE); dot(c, 11, 2, 7, BLACK)
c.line([(GX[10], GY[5]), (GX[12], GY[5])], BLACK, 3)
c.circle(GX[10], GY[5], 46, SLATE); c.circle(GX[12], GY[5], 86, TEAL)
c.grid(BLACK, rows=range(2, 7), cols=[10, 11, 12], skip={(10, 5), (12, 5), (12, 3)})
c.done('htwgin-abschluss.png')

# 5) Inhalt / Agenda / Zusammenfassung: white, vertical 'timeline' of connected dots at right
c = Canvas(WHITE)
c.header_dots(BLACK)
c.grid(BLACK, rows=range(2, 7), cols=[12])
c.line([(GX[12], GY[1]), (GX[12], GY[6])], BLACK, 3)
for j, (r, col) in zip(range(2, 7), [(14, BLACK), (22, TEAL), (14, BLACK), (22, TEAL), (14, BLACK)]):
    dot(c, 12, j, r, col)
c.circle(1980 + 40, 640, 150, LIGHT)
for j in range(2, 7): dot(c, 12, j, [14, 22, 14, 22, 14][j - 2], [BLACK, TEAL, BLACK, TEAL, BLACK][j - 2])
# (no bottom dot row: keeps the list area free)
c.done('htwgin-inhalt.png')

# 6) Zitat / Merksatz: light full bg with a big white 'pill' (as in 'Titel dots invers')
c = Canvas(LIGHT)
c.header_dots(BLACK)
c.grid(BLACK, rows=range(2, 7), cols=range(0, 13))
c.pill((-200, 800), (1200, 640), 390, WHITE)
dot(c, 11, 5, 58, TEAL); dot(c, 9, 6, 34, TEAL); dot(c, 10, 6, 10, BLACK); dot(c, 12, 2, 12, BLACK)
c.done('htwgin-zitat.png')

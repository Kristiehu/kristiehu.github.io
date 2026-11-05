"""Hero for post 8 (SmartTrace): raw work-order input on the left, the report and the
KML trace it becomes on the right.

Illustrative only: every ID, count and length is made up. A quiet palette of its own
(paper, slate and teal) so the card sits among the light covers without shouting.

    python3 scripts/render-post8-hero.py  ->  src/content/blog/img/p8_hero.png

Needs Pillow and fontTools (with brotli) to read the site's own fonts.
"""
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src/content/blog/img/p8_hero.png"
FONTS = ROOT / "node_modules/@fontsource-variable"

S = 2
W, H = 1600, 960

PAPER = (244, 242, 238)
CARD = (255, 255, 255)
EDGE = (222, 217, 208)
SLATE = (61, 74, 92)
MUTED = (128, 136, 148)
FAINT = (190, 194, 200)
TEAL = (47, 127, 122)
TEAL_SOFT = (214, 233, 230)
SAND = (217, 203, 176)
GRID = (236, 233, 227)


def ttf(woff2, name):
    out = Path(tempfile.gettempdir()) / name
    if not out.exists():
        f = TTFont(str(FONTS / woff2))
        f.flavor = None
        f.save(str(out))
    return out


SANS = ttf("source-sans-3/files/source-sans-3-latin-wght-normal.woff2", "source-sans-3-var.ttf")
MONO = ttf("source-code-pro/files/source-code-pro-latin-wght-normal.woff2", "source-code-pro-var.ttf")


def font(path, size, weight=400):
    ft = ImageFont.truetype(str(path), size * S)
    try:
        ft.set_variation_by_axes([weight])
    except Exception:
        pass
    return ft


im = Image.new("RGB", (W * S, H * S), PAPER)
d = ImageDraw.Draw(im)


def s(*v):
    return [x * S for x in v]


def rrect(x0, y0, x1, y1, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(s(x0, y0, x1, y1), radius=r * S, fill=fill, outline=outline, width=int(width * S))


def text(x, y, t, size, color, weight=400, face=SANS, anchor="la"):
    d.text((x * S, y * S), t, font=font(face, size, weight), fill=color, anchor=anchor)


def seg_text(x, y, segs, size, face=MONO):
    """draw a line made of (text, colour, weight) pieces"""
    for t, c, w in segs:
        ft = font(face, size, w)
        d.text((x * S, y * S), t, font=ft, fill=c)
        x += ft.getlength(t) / S


# ---------- left: raw input ----------
rrect(80, 130, 560, 830, 16, fill=CARD, outline=EDGE, width=2)
text(108, 156, "WO.csv  +  circuit.json", 24, SLATE, 600)
text(108, 190, "raw input", 20, MUTED, 400)

TOK = (TEAL, 600)
RAW = (FAINT, 400)
RAW2 = (MUTED, 400)
raw_lines = [
    [("Connections", RAW2[0], 500), ("<COLON>", *TOK)],
    [("DEMO-FOSC-07", RAW2[0], 400), ("<COMMA>", *TOK), ("fib", *RAW)],
    [("res", *RAW), ("<COLON>", *TOK), ("[1-12]", RAW2[0], 400), ("<COMMA>", *TOK)],
    [("cable", *RAW), ("<COLON>", *TOK), ("DEMO-CBL-3", RAW2[0], 400)],
    [("1", RAW2[0], 400), ("<COMMA>", *TOK), ("len", *RAW), ("<COLON>", *TOK), ("812m", RAW2[0], 400)],
    [("<COMMA>", *TOK), ("otdr", *RAW), ("<COLON>", *TOK), ("845m", RAW2[0], 400)],
    [("<COMMA>", *TOK), ("SS", *RAW), ("<COLON>", *TOK), ("coil-02", RAW2[0], 400)],
    [("<COMMA>", *TOK), ("DEMO-FOSC-11", RAW2[0], 400), ("<COLON>", *TOK)],
    [("splice", *RAW), ("<COLON>", *TOK), ("13-24", RAW2[0], 400), ("<COMMA>", *TOK)],
    [("break", *RAW), ("<COLON>", *TOK), ("1", RAW2[0], 400), ("<COMMA>", *TOK), ("mm", *RAW)],
    [("<COLON>", *TOK), ("0412", RAW2[0], 400), ("<COMMA>", *TOK), ("lat", *RAW)],
    [("<COLON>", *TOK), ("43.6", RAW2[0], 400), ("<COMMA>", *TOK), ("lon", *RAW)],
    [("<COLON>", *TOK), ("-79.4", RAW2[0], 400), ("<COMMA>", *TOK), ("...", *RAW)],
]
y = 246
for segs in raw_lines:
    seg_text(108, y, segs, 21)
    y += 42

# ---------- middle: the tool ----------
mx = 640
d.line(s(568, 480, 714, 480), fill=FAINT, width=3 * S)
d.polygon(s(714, 468, 734, 480, 714, 492), fill=FAINT)
rrect(586, 430, 716, 470, 20, fill=SLATE)
text(651, 450, "SmartTrace", 20, CARD, 600, anchor="mm")
text(651, 512, "parse · count · format", 17, MUTED, 400, anchor="mm")

# ---------- right top: the Excel report ----------
rx0, rx1 = 760, 1520
rrect(rx0, 130, rx1, 560, 16, fill=CARD, outline=EDGE, width=2)
tabs = ["Cover Page", "Fibre Trace", "Activity Overview", "Error Report"]
tx = rx0 + 24
for i, t in enumerate(tabs):
    ft = font(SANS, 19, 600 if i == 1 else 450)
    w = ft.getlength(t) / S + 28
    rrect(tx, 152, tx + w, 188, 8, fill=TEAL_SOFT if i == 1 else GRID)
    text(tx + w / 2, 170, t, 19, TEAL if i == 1 else MUTED, 600 if i == 1 else 450, anchor="mm")
    tx += w + 10

metrics = [("Fibre breaks", "1"), ("Splices", "7"), ("Cable length", "2.41 km"), ("OTDR length", "2.58 km")]
mw = (rx1 - rx0 - 48 - 3 * 14) / 4
for i, (k, v) in enumerate(metrics):
    x0 = rx0 + 24 + i * (mw + 14)
    rrect(x0, 212, x0 + mw, 312, 10, fill=PAPER)
    text(x0 + 16, 232, k, 18, MUTED, 450)
    text(x0 + 16, 262, v, 32, SLATE, 650)

# action / description / SAP table
cols = [rx0 + 24, rx0 + 190, rx0 + 560]
text(cols[0], 340, "ACTION", 16, MUTED, 650)
text(cols[1], 340, "DESCRIPTION", 16, MUTED, 650)
text(cols[2], 340, "SAP", 16, MUTED, 650)
d.line(s(rx0 + 24, 366, rx1 - 24, 366), fill=EDGE, width=2 * S)
rows = [("Splice", 0.78, 0.5), ("Splice", 0.62, 0.42), ("Break", 0.7, 0.55), ("Splice", 0.55, 0.38)]
yy = 386
for a, w1, w2 in rows:
    text(cols[0], yy, a, 19, TEAL if a == "Break" else SLATE, 600)
    rrect(cols[1], yy + 6, cols[1] + 330 * w1, yy + 18, 6, fill=GRID)
    rrect(cols[2], yy + 6, cols[2] + 150 * w2, yy + 18, 6, fill=GRID)
    yy += 40

# ---------- right bottom: the KML trace ----------
rrect(rx0, 590, rx1, 830, 16, fill=CARD, outline=EDGE, width=2)
text(rx0 + 24, 610, "KML trace", 20, SLATE, 600)
# faint street blocks
for bx in range(rx0 + 24, rx1 - 60, 120):
    for by in (650, 728):
        rrect(bx, by, bx + 100, by + 62, 8, fill=GRID)
route = [(rx0 + 60, 720), (rx0 + 210, 720), (rx0 + 330, 642), (rx0 + 560, 642), (rx0 + 640, 720), (rx1 - 60, 720)]
d.line([c * S for p in route for c in p], fill=TEAL, width=6 * S, joint="curve")
for i, (x, y2) in enumerate(route):
    if i in (0, len(route) - 1):
        d.ellipse(s(x - 13, y2 - 13, x + 13, y2 + 13), fill=SLATE)
        text(x, y2 + 1, "A" if i == 0 else "Z", 16, CARD, 700, anchor="mm")
    else:
        d.ellipse(s(x - 9, y2 - 9, x + 9, y2 + 9), fill=CARD, outline=TEAL, width=4 * S)

text(rx1, 872, "Illustration · simulated data", 20, MUTED, 450, anchor="ra")

out = im.resize((W, H), Image.LANCZOS)
out.save(OUT, optimize=True)
print(f"wrote {OUT.relative_to(ROOT)} ({W}x{H})")

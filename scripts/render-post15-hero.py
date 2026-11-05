"""Hero for post 15: inside plant and outside plant capacity in one picture.

Left, a hub with two pieces of equipment drawn as port grids (used, free, and one
nearly full). Right, the cables leaving the hub through a street grid, past structures
and splice closures, each with a bar for how much of its fibre is in use. Everything is
illustrative: no real equipment, counts or routes.

    python3 scripts/render-post15-hero.py   ->  src/content/blog/img/p15_main.png

Needs Pillow and fontTools (with brotli) to read the site's own Source Sans 3.
"""
import os
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src/content/blog/img/p15_main.png"
WOFF2 = ROOT / "node_modules/@fontsource-variable/source-sans-3/files/source-sans-3-latin-wght-normal.woff2"

S = 2  # draw at 2x, then scale down for clean edges
W, H = 1600, 960

BLUE = (78, 122, 178)
RED = (216, 58, 31)
INK = (15, 18, 25)
GRAY = (96, 115, 159)
PALE = (214, 222, 234)
BLOCK = (238, 241, 245)
WALL = (150, 160, 176)
HUB_FILL = (248, 249, 251)
WHITE = (255, 255, 255)

# the site's UI face, converted once to a temporary TTF Pillow can read
_ttf = Path(tempfile.gettempdir()) / "source-sans-3-var.ttf"
if not _ttf.exists():
    f = TTFont(str(WOFF2))
    f.flavor = None
    f.save(str(_ttf))


def font(size, weight=400):
    ft = ImageFont.truetype(str(_ttf), size * S)
    try:
        ft.set_variation_by_axes([weight])
    except Exception:
        pass
    return ft


im = Image.new("RGB", (W * S, H * S), WHITE)
d = ImageDraw.Draw(im)


def s(*v):
    return [x * S for x in v]


def rrect(x0, y0, x1, y1, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(s(x0, y0, x1, y1), radius=r * S, fill=fill, outline=outline, width=int(width * S))


def line(points, color, width):
    d.line([c * S for p in points for c in p], fill=color, width=int(width * S), joint="curve")


def text(x, y, t, size, color=INK, weight=400, anchor="la", spacing=0.0):
    ft = font(size, weight)
    if spacing:
        cx = x
        for ch in t:
            d.text((cx * S, y * S), ch, font=ft, fill=color, anchor=anchor)
            cx += ft.getlength(ch) / S + spacing
        return
    d.text((x * S, y * S), t, font=ft, fill=color, anchor=anchor)


# ---------- section labels ----------
text(90, 88, "INSIDE PLANT", 28, GRAY, 650, spacing=2.4)
text(308, 88, "·  weekly", 28, GRAY, 400)
text(700, 88, "OUTSIDE PLANT", 28, GRAY, 650, spacing=2.4)
text(950, 88, "·  monthly", 28, GRAY, 400)

# ---------- outside plant: street blocks ----------
xs = [(700, 800), (840, 1020), (1060, 1240), (1280, 1440), (1480, 1540)]
ys = [(160, 310), (350, 500), (540, 670), (710, 820)]
for x0, x1 in xs:
    for y0, y1 in ys:
        rrect(x0, y0, x1, y1, 10, fill=BLOCK)

# ---------- inside plant: the hub and its equipment ----------
rrect(90, 150, 640, 830, 18, fill=HUB_FILL, outline=WALL, width=3)
text(116, 168, "Hub", 24, GRAY, 600)


def rack(y, name, used, total=48, cols=12):
    hot = used / total >= 0.85
    accent = RED if hot else BLUE
    rrect(130, y, 600, y + 268, 12, fill=WHITE, outline=PALE, width=2)
    text(156, y + 24, name, 32, INK, 650)
    text(574, y + 30, f"{used} / {total} in use", 26, accent, 600, anchor="ra")
    size, gap = 28, 8
    gx = 130 + (470 - (cols * size + (cols - 1) * gap)) / 2
    for i in range(total):
        r, c = divmod(i, cols)
        x0 = gx + c * (size + gap)
        y0 = y + 92 + r * (size + gap)
        rrect(x0, y0, x0 + size, y0 + size, 5, fill=accent if i < used else PALE)


rack(214, "Access", 34)
rack(530, "Core", 44)

# ---------- cables leaving the hub ----------
CABLES = [
    # route, share of fibre in use
    ([(640, 330), (1460, 330), (1460, 250)], 0.62),
    ([(640, 520), (1460, 520)], 0.91),
    ([(640, 690), (1260, 690), (1260, 760)], 0.45),
]
for route, used in CABLES:
    line(route, RED if used >= 0.85 else BLUE, 7)

# structures (small squares) and splice closures (rings) along the routes
for x, y in [(820, 330), (1260, 330), (820, 520), (1260, 520), (820, 690), (1040, 690)]:
    rrect(x - 9, y - 9, x + 9, y + 9, 3, fill=WHITE, outline=WALL, width=3)
for (x, y), hot in [((1040, 330), False), ((1460, 330), False), ((1040, 520), True),
                    ((1460, 520), True), ((1260, 690), False)]:
    c = RED if hot else BLUE
    d.ellipse(s(x - 15, y - 15, x + 15, y + 15), fill=WHITE, outline=c, width=5 * S)

# end buildings for the two branches
for x, y in [(1460, 236), (1260, 774)]:
    rrect(x - 22, y - 16, x + 22, y + 16, 5, fill=WHITE, outline=WALL, width=3)

# fibre-in-use bar above each cable, in the first block's gap
for (route, used), y in zip(CABLES, [330, 520, 690]):
    hot = used >= 0.85
    c = RED if hot else BLUE
    bx, by = 862, y - 40
    rrect(bx, by, bx + 120, by + 14, 7, fill=PALE)
    rrect(bx, by, bx + 120 * used, by + 14, 7, fill=c)
    text(bx + 132, by - 8, f"{round(used * 100)}% fibre in use", 24, c, 600)

# ---------- legend ----------
lx, ly = 90, 884
items = [
    ("sq", BLUE, "in use"),
    ("sq", PALE, "free"),
    ("sq", RED, "85% or more"),
    ("ring", BLUE, "splice closure"),
    ("box", WALL, "structure"),
]
for kind, c, label in items:
    if kind == "sq":
        rrect(lx, ly - 11, lx + 22, ly + 11, 4, fill=c)
    elif kind == "ring":
        d.ellipse(s(lx, ly - 11, lx + 22, ly + 11), fill=WHITE, outline=c, width=4 * S)
    else:
        rrect(lx + 2, ly - 9, lx + 20, ly + 9, 3, fill=WHITE, outline=c, width=3)
    text(lx + 32, ly, label, 24, GRAY, 450, anchor="lm")
    lx += 32 + font(24, 450).getlength(label) / S + 44

# say plainly that none of it is real
text(1540, 884, "Illustration · simulated data", 22, GRAY, 500, anchor="rm")

out = im.resize((W, H), Image.LANCZOS)
out.save(OUT, optimize=True)
print(f"wrote {OUT.relative_to(ROOT)} ({W}x{H})")

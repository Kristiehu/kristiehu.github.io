"""Hero for post 16: one day's reconciliation run, as it looks in a terminal.

A simulated run: the script name, file name, times and counts are made up, and there is
no real host, user or path in it. Its look is deliberately its own (a dark terminal in
the site's code face) rather than the red-and-blue illustrations of posts 14 and 15.

    python3 scripts/render-post16-hero.py  ->  src/content/blog/img/16-cross-team-alignment-hero.png

Needs Pillow and fontTools (with brotli) to read the site's own Source Code Pro.
"""
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src/content/blog/img/16-cross-team-alignment-hero.png"
FONTS = ROOT / "node_modules/@fontsource-variable"

S = 2
W, H = 1600, 960

BACKDROP = (232, 228, 221)
WINDOW = (30, 33, 39)
TITLEBAR = (42, 46, 54)
TEXT = (215, 218, 224)
DIM = (127, 135, 150)
GREEN = (139, 196, 138)
AMBER = (229, 181, 103)
CYAN = (111, 179, 201)
WHITE = (240, 242, 245)


def ttf(woff2_name, out_name):
    out = Path(tempfile.gettempdir()) / out_name
    if not out.exists():
        f = TTFont(str(FONTS / woff2_name))
        f.flavor = None
        f.save(str(out))
    return out


MONO = ttf("source-code-pro/files/source-code-pro-latin-wght-normal.woff2", "source-code-pro-var.ttf")
SANS = ttf("source-sans-3/files/source-sans-3-latin-wght-normal.woff2", "source-sans-3-var.ttf")


def font(path, size, weight=400):
    ft = ImageFont.truetype(str(path), size * S)
    try:
        ft.set_variation_by_axes([weight])
    except Exception:
        pass
    return ft


im = Image.new("RGB", (W * S, H * S), BACKDROP)

# window shadow
wx0, wy0, wx1, wy1 = 150, 110, 1450, 860
shadow = Image.new("L", im.size, 0)
ImageDraw.Draw(shadow).rounded_rectangle(
    [(wx0 + 6) * S, (wy0 + 22) * S, (wx1 + 6) * S, (wy1 + 26) * S], radius=22 * S, fill=110
)
shadow = shadow.filter(ImageFilter.GaussianBlur(28 * S))
im.paste(Image.new("RGB", im.size, (120, 112, 100)), mask=shadow)

d = ImageDraw.Draw(im)
d.rounded_rectangle([wx0 * S, wy0 * S, wx1 * S, wy1 * S], radius=16 * S, fill=WINDOW)
# title bar
d.rounded_rectangle([wx0 * S, wy0 * S, wx1 * S, (wy0 + 56) * S], radius=16 * S, fill=TITLEBAR)
d.rectangle([wx0 * S, (wy0 + 40) * S, wx1 * S, (wy0 + 56) * S], fill=TITLEBAR)
for i, c in enumerate([(237, 106, 94), (245, 191, 79), (98, 197, 84)]):
    cx, cy = wx0 + 32 + i * 30, wy0 + 28
    d.ellipse([(cx - 8) * S, (cy - 8) * S, (cx + 8) * S, (cy + 8) * S], fill=c)
d.text(((wx0 + wx1) / 2 * S, (wy0 + 28) * S), "reconcile — daily run (simulated)",
       font=font(SANS, 20, 500), fill=DIM, anchor="mm")

def lead(label, width=38):
    """label, then dot leaders, so the status words line up in one column"""
    return label + " " + "." * (width - len(label) - 2) + " "


def col(label, width=29):
    """indented label padded so the counts line up"""
    return ("  " + label).ljust(width)


# terminal lines: list of (segments), each segment (text, colour, weight)
LINES = [
    [("$ ", GREEN, 600), ("./reconcile_daily.sh", TEXT, 500)],
    [],
    [("[17:30:02] ", DIM, 400), ("pull     ", CYAN, 600), (lead("GIS records"), TEXT, 400), ("ok", GREEN, 600)],
    [("[17:30:09] ", DIM, 400), ("pull     ", CYAN, 600), (lead("operational records"), TEXT, 400), ("ok", GREEN, 600)],
    [("[17:30:31] ", DIM, 400), ("compare  ", CYAN, 600), ("circuits across 4 regions", TEXT, 400)],
    [("           ", DIM, 400), (col("status not in sync"), TEXT, 400), ("18", AMBER, 700)],
    [("           ", DIM, 400), (col("entry error"), TEXT, 400), (" 3", AMBER, 700)],
    [("           ", DIM, 400), ("  ----------------------------", DIM, 400)],
    [("           ", DIM, 400), (col("differences to send"), WHITE, 600), ("21", AMBER, 700)],
    [("[17:30:33] ", DIM, 400), ("write    ", CYAN, 600), ("reconciliation_2026-06-19.xlsx", TEXT, 400)],
    [("[17:30:34] ", DIM, 400), ("connect  ", CYAN, 600), (lead("sftp, ssh key -> exchange folder"), TEXT, 400), ("ok", GREEN, 600)],
    [("[17:30:35] ", DIM, 400), ("send     ", CYAN, 600), (lead("reconciliation_2026-06-19.xlsx"), TEXT, 400), ("done", GREEN, 600)],
    [("[17:30:35] ", DIM, 400), ("next     ", CYAN, 600), ("tomorrow, 17:30", DIM, 400)],
    [],
    [("$ ", GREEN, 600)],
]

size = 25
line_h = 43
x0, y = wx0 + 52, wy0 + 98
for segs in LINES:
    x = x0
    for t, c, wgt in segs:
        ft = font(MONO, size, wgt)
        d.text((x * S, y * S), t, font=ft, fill=c)
        x += ft.getlength(t) / S
    last_x, last_y = x, y
    y += line_h

# cursor after the final prompt
d.rectangle([(last_x + 2) * S, (last_y + 3) * S, (last_x + 16) * S, (last_y + 31) * S], fill=TEXT)

out = im.resize((W, H), Image.LANCZOS)
out.save(OUT, optimize=True)
print(f"wrote {OUT.relative_to(ROOT)} ({W}x{H})")

"""Draw the Lab direction covers (src/assets/covers/*.jpg) in the style of the point-cloud art:
a flat background in the dark page colour (no glow, so nothing frames the scene), 30-degree
isometric view, grey dots, and semantic classes picked out in red / blue / green. Output is
1200 x 900 (4:3), drawn at 2x and downsampled.

    pip install numpy pillow scipy
    python scripts/render-covers.py                     # earth-observation + data-systems
    python scripts/render-covers.py lidar path/to/art.png   # crop the original art for 01
    python scripts/render-covers.py light               # make the light-theme versions (*-light.jpg)

The scenes are illustrations, not data. Keep new covers in the same palette and scale.
"""
import math
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 2400, 1800  # 2x supersampled canvas
C30, S30 = math.cos(math.radians(30)), 0.5

BG_EDGE = np.array([10, 12, 16])  # the dark theme's page colour (#0a0c10)

GREY = np.array([100, 107, 115])
RED = np.array([206, 62, 36])
BLUE = np.array([86, 156, 190])
GREEN = np.array([76, 158, 120])
ORANGE = np.array([222, 146, 86])


def background(seed=0):
    """The page colour with a little grain."""
    img = np.zeros((H, W, 3), np.float64) + BG_EDGE[None, None, :]
    rng = np.random.default_rng(seed)
    img += rng.normal(0, 0.9, img.shape)
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


class Scene:
    def __init__(self, scale, cx=W / 2, cy=H / 2, seed=1):
        self.S, self.cx, self.cy = scale, cx, cy
        self.pts = []  # (x, y, z, r, (R,G,B))
        self.rng = np.random.default_rng(seed)

    def add(self, x, y, z, color, r=4.2):
        self.pts.append((x, y, z, r, tuple(int(v) for v in np.clip(color, 0, 255))))

    def proj(self, x, y, z):
        return (self.cx + (x - y) * C30 * self.S, self.cy + (x + y) * S30 * self.S - z * self.S)

    def grey(self, lo=-22, hi=40, dim=1.0):
        """A grey dot with the art's brightness spread (mostly mid, a few bright)."""
        k = self.rng.normal(0, 1)
        v = GREY + np.clip(k * 14, lo, hi)
        if self.rng.random() < 0.06:
            v = GREY + self.rng.uniform(45, 95)
        bg = BG_EDGE + 6
        return bg + (v - bg) * dim

    def tint(self, base, spread=14, dim=1.0):
        v = base + self.rng.normal(0, spread, 3) * np.array([1, 0.6, 0.6])
        bg = BG_EDGE + 6
        return bg + (v - bg) * dim

    def render(self, bg, out, size=(1200, 900)):
        img = bg.copy()
        dr = ImageDraw.Draw(img)
        order = sorted(self.pts, key=lambda p: p[0] + p[1] + p[2])
        for x, y, z, r, col in order:
            sx, sy = self.proj(x, y, z)
            dr.ellipse((sx - r, sy - r, sx + r, sy + r), fill=col)
        img = img.filter(ImageFilter.GaussianBlur(0.4))
        img = img.resize(size, Image.LANCZOS)
        img.save(out, optimize=True)
        print("wrote", out, len(self.pts), "points")


# ---------------------------------------------------------------- helpers
def line(sc, a, b, step, color_fn, r=3.9):
    a, b = np.array(a, float), np.array(b, float)
    n = max(2, int(np.linalg.norm(b - a) / step))
    for t in np.linspace(0, 1, n):
        p = a + (b - a) * t
        sc.add(*p, color_fn(), r=r)


def smooth_noise(n, rng, octaves=((4, 1.0), (9, 0.5), (18, 0.25))):
    """Cheap value noise on an n x n grid, roughly in [0, 1]."""
    out = np.zeros((n, n))
    for cells, amp in octaves:
        g = rng.random((cells + 1, cells + 1))
        xs = np.linspace(0, cells, n)
        i = np.floor(xs).astype(int).clip(0, cells - 1)
        f = xs - i
        f = f * f * (3 - 2 * f)
        a = g[i][:, i]
        b = g[i + 1][:, i]
        c = g[i][:, i + 1]
        d = g[i + 1][:, i + 1]
        fy, fx = f[:, None], f[None, :]
        out += amp * (a * (1 - fy) * (1 - fx) + b * fy * (1 - fx) + c * (1 - fy) * fx + d * fy * fx)
    out -= out.min()
    return out / out.max()


# ---------------------------------------------------------------- EO cover
def eo_cover(out):
    """A terrain block seen from orbit, sampled on a regular raster grid: a ridge with a
    mine on its slope venting a methane plume (red, drifting downwind), a river (blue)
    and crop parcels (green) on the plain."""
    a = 13.0
    n = 50
    sc = Scene(scale=41, cy=H / 2 + 70, seed=7)
    rng = sc.rng
    noise = smooth_noise(n, rng, octaves=((3, 1.0), (7, 0.55), (15, 0.25)))
    noise2 = smooth_noise(n, rng, octaves=((5, 1.0), (11, 0.4)))
    xs = np.linspace(-a, a, n)

    def smoothstep(e0, e1, v):
        t = np.clip((v - e0) / (e1 - e0), 0, 1)
        return t * t * (3 - 2 * t)

    X, Y = np.meshgrid(xs, xs, indexing="ij")
    T = (X + Y) / (2 * a)            # -1 = back (top of image), +1 = front
    Q = (X - Y) / (2 * a)            # -1 = screen left, +1 = screen right
    peaks = [(-0.50, -0.62, 3.6, 0.30), (0.02, -0.78, 4.6, 0.26), (0.46, -0.52, 3.2, 0.24), (-0.15, -0.40, 1.6, 0.18)]
    ridge = np.zeros_like(X)
    for pq, pt, ph, pw in peaks:
        ridge += ph * np.exp(-(((Q - pq) / (pw * 1.3)) ** 2 + ((T - pt) / pw) ** 2))
    ridge *= 0.75 + 0.5 * noise
    rugged = 1 - np.abs(2 * smooth_noise(n, rng, octaves=((6, 1.0), (13, 0.5), (26, 0.2))) - 1)
    ridge += 1.3 * rugged * np.clip(ridge / 2.5, 0, 1)
    ridge *= smoothstep(0.12, -0.15, T)  # keep the plain flat
    Z = ridge + 0.30 * noise2

    # river along the valley floor, meandering left to right
    river_c = 0.20 + 0.09 * np.sin(Q * 4.2 + 0.4) + 0.03 * np.sin(Q * 11)
    river = np.abs(T - river_c) < 0.032 + 0.008 * np.sin(Q * 7)
    Z = np.where(river, Z - 0.25, Z)
    Z = np.where(T > river_c + 0.04, Z * 0.35, Z)  # flatten the plain in front of the river

    # mine bench on the slope: flattened patch
    mine_q, mine_t = 0.40, -0.27
    mine = (np.abs(Q - mine_q) < 0.07) & (np.abs(T - mine_t) < 0.05)
    Z = np.where(mine, np.round(Z * 2) / 2, Z)

    # hillshade, light from the back-left
    gx, gy = np.gradient(Z, xs, xs)
    nx, ny, nz = -gx, -gy, np.ones_like(Z)
    nl = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    L = np.array([-0.62, 0.48, 0.62]); L = L / np.linalg.norm(L)  # from screen-left
    shade = np.clip((nx * L[0] + ny * L[1] + nz * L[2]) / nl, 0, 1)

    for i in range(n):
        for j in range(n):
            x, y, z = X[i, j], Y[i, j], Z[i, j]
            t, q = T[i, j], Q[i, j]
            col = None
            if river[i, j]:
                col = sc.tint(BLUE, 10, dim=0.85 + 0.15 * shade[i, j])
            elif t > river_c[i, j] + 0.07 and t < 0.92 and -0.86 < q < 0.70:
                # crop parcels on the plain, with lanes
                if (i % 6 != 0) and (j % 5 != 0):
                    h = ((i // 6) * 7 + (j // 5) * 3) % 6
                    if h in (0, 1, 3, 4):
                        col = sc.tint(GREEN, 9, dim=0.86 + 0.05 * h)
            elif mine[i, j]:
                col = sc.grey(lo=20, hi=60, dim=1.05)
            if col is None:
                col = sc.grey(dim=0.36 + 0.95 * shade[i, j] ** 2.4)
            sc.add(x, y, z, col, r=4.5)

    # block sides (front two faces): sparse dotted columns down to a base, like a block diagram
    base = -2.2
    for k in range(n):
        for (i, j) in ((n - 1, k), (k, n - 1)):
            x, y, z = X[i, j], Y[i, j], Z[i, j]
            m = max(2, int((z - base) / 0.42))
            for s in np.linspace(base, z, m)[:-1]:
                if rng.random() < 0.55:
                    sc.add(x + 0.001, y + 0.001, s, sc.grey(dim=0.55), r=3.6)
    for p, q2 in (((a, -a), (a, a)), ((-a, a), (a, a))):
        line(sc, (p[0], p[1], base), (q2[0], q2[1], base), 0.16, lambda: sc.grey(lo=10, hi=50), r=3.6)
    for ex, ey in ((a, -a), (a, a), (-a, a)):
        zi = Z[(np.abs(xs - ex)).argmin(), (np.abs(xs - ey)).argmin()]
        line(sc, (ex, ey, base), (ex, ey, zi), 0.16, lambda: sc.grey(lo=10, hi=50), r=3.6)

    # methane plume: 3D cloud of points rising and widening downwind from the mine
    mi = np.argwhere(mine)
    ci, cj = mi[len(mi) // 2]
    sx0, sy0, sz0 = X[ci, cj], Y[ci, cj], Z[ci, cj] + 0.15
    wind = np.array([-0.62, 0.78, 0.0]); wind /= np.linalg.norm(wind)  # drifts screen-left, over the slope
    side = np.array([-wind[1], wind[0], 0.0])
    Lp = 10.5
    for _ in range(620):
        s = Lp * rng.random() ** 1.25
        spread = 0.12 + 0.17 * s
        p = (np.array([sx0, sy0, sz0]) + wind * s + side * rng.normal(0, spread)
             + np.array([0, 0, 0.35 + 0.05 * s + abs(rng.normal(0, 0.12 + spread * 0.25))]))
        fade = (1 - s / Lp) ** 0.8
        if rng.random() > 0.20 + 0.80 * fade:
            continue
        sc.add(*p, sc.tint(RED, 12, dim=0.50 + 0.55 * fade), r=4.3)
    # vent: one bigger, brighter dot (like the red dot on the art's blue chair)
    sc.add(sx0, sy0, sz0 + 0.25, RED + 35, r=7.5)

    sc.render(background(seed=3), out)


# ---------------------------------------------------------------- Systems cover
def systems_cover(out):
    """A city block grid scanned as points, a fibre route (red) running from a hub (blue)
    along the streets to connected buildings (green), with drops up the walls."""
    a = 14.0
    sc = Scene(scale=43, cy=H / 2 + 20, seed=11)
    rng = sc.rng
    street = 7.0  # block pitch
    half_w = 0.75  # half street width

    def on_street(x, y):
        rx = (x + a) % street
        ry = (y + a) % street
        return min(rx, street - rx) < half_w or min(ry, street - ry) < half_w

    # ground: scattered points on the blocks, streets left dark
    n = 5200
    xs = rng.uniform(-a, a, n)
    ys = rng.uniform(-a, a, n)
    for x, y in zip(xs, ys):
        if on_street(x, y):
            continue
        sc.add(x, y, 0, sc.grey(dim=0.95), r=4.0)

    # street centre lines: faint, regular
    for k in range(5):
        c = -a + k * street
        if abs(c) > a + 1e-6:
            continue
        line(sc, (c, -a, 0), (c, a, 0), 0.55, lambda: sc.grey(lo=-10, hi=10, dim=0.45), r=2.6)
        line(sc, (-a, c, 0), (a, c, 0), 0.55, lambda: sc.grey(lo=-10, hi=10, dim=0.45), r=2.6)

    def box(x0, y0, x1, y1, h, color_fn, density=5.5):
        # visible faces only: +x, +y, top (keeps boxes readable)
        def scatter(n_pts, f):
            for _ in range(n_pts):
                sc.add(*f(rng.random(), rng.random()), color_fn(), r=4.3)
        top = (x1 - x0) * (y1 - y0)
        scatter(int(top * density), lambda s, t: (x0 + s * (x1 - x0), y0 + t * (y1 - y0), h))
        scatter(int((y1 - y0) * h * density * 0.8), lambda s, t: (x1, y0 + s * (y1 - y0), t * h))
        scatter(int((x1 - x0) * h * density * 0.8), lambda s, t: (x0 + s * (x1 - x0), y1, t * h))
        # crisp vertical edges
        for ex, ey in [(x1, y1), (x1, y0), (x0, y1)]:
            line(sc, (ex, ey, 0), (ex, ey, h), 0.2, color_fn, r=3.4)

    blocks = [(-a + i * street, -a + j * street) for i in range(4) for j in range(4)]
    hub = (1, 1)
    lit = {(3, 0), (0, 2), (2, 3)}
    plain = {(0, 0): 3.0, (1, 0): 4.5, (2, 1): 2.2, (3, 2): 5.5, (1, 3): 2.8, (2, 0): 1.6, (0, 3): 3.6}
    for (i, j), (bx, by) in zip([(i, j) for i in range(4) for j in range(4)], blocks):
        x0, y0 = bx + half_w + 0.9, by + half_w + 0.9
        x1, y1 = bx + street - half_w - 0.9, by + street - half_w - 0.9
        if (i, j) == hub:
            box(x0 + 0.6, y0 + 0.6, x1 - 0.6, y1 - 0.6, 6.5, lambda: sc.tint(BLUE, 12), density=6.5)
        elif (i, j) in lit:
            h = {(3, 0): 3.4, (0, 2): 4.2, (2, 3): 2.6}[(i, j)]
            box(x0 + 0.8, y0 + 0.8, x1 - 0.8, y1 - 0.8, h, lambda: sc.tint(GREEN, 10), density=6.5)
        elif (i, j) in plain:
            box(x0 + 1.0, y0 + 1.0, x1 - 1.0, y1 - 1.0, plain[(i, j)], lambda: sc.grey(dim=0.95), density=4.2)

    # fibre route: from the hub's street corner along streets to each lit building
    def sc_line(p, q):
        line(sc, (p[0], p[1], 0.05), (q[0], q[1], 0.05), 0.30, lambda: sc.tint(RED, 10), r=4.6)

    c = lambda k: -a + k * street  # street coordinate
    hub_pt = (c(2), c(2))
    routes = [
        [hub_pt, (c(2), c(1)), (c(4) - 0.01, c(1))],              # east then to (3,0)
        [hub_pt, (c(1), c(2)), (c(1), c(3))],                      # to (0,2)
        [hub_pt, (c(3), c(2)), (c(3), c(4) - 0.01)],               # to (2,3)
    ]
    for r_ in routes:
        for p, q in zip(r_, r_[1:]):
            sc_line(p, q)
    # drops: short red risers up the lit buildings' street-facing walls
    drops = [((c(3) + 3.5, c(1) - 0.0), 3.4), ((c(1) - 0.0, c(2) + 3.5), 4.2), ((c(3) - 0.0, c(3) + 3.5), 2.6)]
    for (dx, dy), h in drops:
        line(sc, (dx, dy, 0.05), (dx, dy, h * 0.8), 0.26, lambda: sc.tint(RED, 8), r=4.2)
    # hub splice point
    sc.add(hub_pt[0], hub_pt[1], 0.1, RED + 30, r=7.5)

    sc.render(background(seed=5), out)


# ---------------------------------------------------------------- LiDAR cover (Kristie's art)
def lidar_cover(out, art_path):
    art = Image.open(art_path).convert("RGB")  # the 1330 x 1060 crop of public/og-new.png's artwork
    crop = art.crop((0, 40, 1330, 1037))  # 4:3
    flatten(crop.resize((1200, 900), Image.LANCZOS)).save(out, quality=90, subsampling=0, optimize=True)
    print("wrote", out)


def flatten(img, size=31, sigma=60):
    """Take the art's soft glow out from behind the dots, so its background is the page colour too."""
    from scipy import ndimage as ndi

    a = np.asarray(img.convert("RGB")).astype(np.float32)
    # the background under the dots: darkest value nearby, smoothed
    floor = np.stack([ndi.gaussian_filter(ndi.minimum_filter(a[..., k], size), sigma) for k in range(3)], -1)
    a -= np.clip(floor - BG_EDGE, 0, None)
    return Image.fromarray(np.clip(a, 0, 255).round().astype(np.uint8))




# ---------------------------------------------------------------- light-theme versions
# Flip lightness in CIELAB and keep hue/colourfulness: the dark navy background becomes near-white,
# grey dots become slate, and the red/blue/green classes stay red/blue/green.
def light_version(src, dst, chroma=1.15, lift=5.0, contrast=1.25):
    from skimage import color  # pip install scikit-image

    rgb = np.asarray(Image.open(src).convert("RGB")).astype(np.float64) / 255.0
    lab = color.rgb2lab(rgb)
    flipped = np.clip(100.0 + lift - lab[..., 0] * contrast, 0, 100)
    lab2 = np.dstack([flipped, lab[..., 1] * chroma, lab[..., 2] * chroma])
    out = (np.clip(color.lab2rgb(lab2), 0, 1) * 255).round().astype(np.uint8)
    Image.fromarray(out).save(dst, quality=90, subsampling=0, optimize=True)
    print("wrote", dst)


if __name__ == "__main__":
    import os

    out_dir = os.path.join(os.path.dirname(__file__), "..", "src", "assets", "covers")
    args = sys.argv[1:]
    if args[:1] == ["light"]:
        for name in ("lidar", "earth-observation", "data-systems"):
            light_version(os.path.join(out_dir, name + ".jpg"), os.path.join(out_dir, name + "-light.jpg"))
    elif args[:1] == ["lidar"]:
        lidar_cover(os.path.join(out_dir, "lidar.jpg"), args[1])
    else:
        for name, fn in (("earth-observation", eo_cover), ("data-systems", systems_cover)):
            tmp = os.path.join(out_dir, name + ".png")
            fn(tmp)
            Image.open(tmp).convert("RGB").save(os.path.join(out_dir, name + ".jpg"), quality=90, subsampling=0, optimize=True)
            os.remove(tmp)

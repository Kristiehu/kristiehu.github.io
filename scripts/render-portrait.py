"""Turn the avatar drawing into the point-cloud portrait on Home and About.

    pip install numpy scipy scikit-image pillow
    python scripts/render-portrait.py              # source: src/assets/me_0.png
    python scripts/render-portrait.py preview      # also writes preview-{light,dark}.png to check by eye

Writes, in src/assets/portrait/:
  points.bin    the points: 3D position plus how bright the drawing is under each one.
                src/components/PointPortrait.astro draws them in either theme.
                Layout (little-endian): uint32 n, uint32 0 (unused); int16 x[n], y[n], z[n] in
                quarter pixels; uint8 refl[n], light[n], edge[n], fade[n], front[n].
  meta.json     point count, default view, frame, and where the lighter's flame starts
                (the component animates the flame; it is not part of the points).
  fallback.png  a still light-theme render, shown only when JavaScript is off.

How it works: the drawing's outline is "inflated" into a shallow 3D relief (deeper in the
middle, a rounder head, the hand held out in front), then sampled along horizontal scan lines,
like a LiDAR sweep. Each point keeps the brightness of the drawing under it (dark hair, light
face), which is what keeps the face and the frame readable. The outline is smoothed and traced
with an even row of dots, and the scan lines fade out just inside it, so the edge stays clean.

The part detection (hair / face / hand / flame) is tuned to this drawing; a new source image
needs the thresholds in `parts()` checked against `preview`.
"""
import json
import struct
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi
from skimage.color import rgb2hsv
from skimage import measure
from skimage.morphology import disk, opening

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src/assets/me_0.png"
OUT = ROOT / "src/assets/portrait"

ROW = 14.0  # scan-line spacing, source px
STEP = 5.5  # point spacing along a line, source px
VIEW = (8.0, -14.0)  # default yaw, pitch (degrees); the component tilts around this
TILT = (6.0, 4.0)  # most extra yaw, pitch as she turns toward the mouse; the frame leaves room for it
UNIT = 4  # positions are stored in quarter pixels
EDGE = 12.0  # scan lines fade out over this many px inside the outline

# Same numbers as THEMES in PointPortrait.astro (used here only for the still renders)
THEMES = {
    "dark": dict(gamma=0.8, floor=0.36, cap=1.0, rmax=1.05, rmin=0.25, ink=(238, 236, 230)),
    "light": dict(gamma=1.25, floor=0.14, cap=0.66, rmax=0.9, rmin=0.22, ink=(15, 18, 25)),
}
ACCENT = (78, 122, 178)  # --blue


def largest(m):
    lab, n = ndi.label(m)
    if n == 0:
        return m
    sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
    return lab == (1 + int(np.argmax(sizes)))


def parts(im):
    """Masks for the figure and its parts, from the drawing's colours."""
    H, W = im.shape[:2]
    rgb, alpha = im[..., :3], im[..., 3]
    h, s, v = np.moveaxis(rgb2hsv(rgb), -1, 0)
    yy, xx = np.mgrid[0:H, 0:W]
    figure = ndi.binary_fill_holes(alpha > 0.5)
    skin = figure & ((h < 0.13) | (h > 0.92)) & (s > 0.06) & (s < 0.65) & (v > 0.5)
    # the flame: bright yellow, next to the hand (lower left)
    flame = figure & (v > 0.78) & (h > 0.06) & (h < 0.2) & (s > 0.25) & (xx < 0.33 * W) & (yy > 0.59 * H) & (yy < 0.68 * H)
    lighter = figure & (xx > 0.18 * W) & (xx < 0.29 * W) & (yy > 0.66 * H) & (yy < 0.71 * H) & ~skin
    face = ndi.binary_closing(largest(skin & (yy < 0.54 * H)), iterations=6)
    hand = largest(skin & (yy > 0.59 * H) & (xx < 0.49 * W)) | lighter | ndi.binary_dilation(flame, iterations=2)
    hand = ndi.binary_closing(hand, iterations=5) & figure
    hair = largest(opening(figure & (v < 0.25), disk(4)))
    # the outline the points follow: smoothed, without the loose strands of hair
    smooth = largest(opening(ndi.gaussian_filter(figure.astype(float), 3) > 0.5, disk(5)))
    return dict(figure=figure, face=face, hand=hand, hair=hair, flame=flame, smooth=smooth)


def relief(im, P):
    """Depth (towards the viewer, source px) for every pixel of the figure."""
    H, W = im.shape[:2]
    M = P["figure"]
    yy, xx = np.mgrid[0:H, 0:W]
    Z = 8.0 * np.sqrt(ndi.distance_transform_edt(M))  # round cross-section
    fy, fx = np.nonzero(P["face"])
    ry, rx = np.ptp(fy) / 2, np.ptp(fx) / 2
    hy, hx = fy.mean() - 0.25 * ry, fx.mean()
    r2 = ((xx - hx) / (1.25 * rx)) ** 2 + ((yy - hy) / (1.35 * ry)) ** 2
    Z += 70 * np.sqrt(np.clip(1 - r2, 0, 1))  # the head is rounder than the body
    Z += 8 * ndi.gaussian_filter((P["hair"] & (r2 > 1)).astype(float), 5)  # hair lies on the shoulders
    d_hand = ndi.distance_transform_edt(P["hand"])
    Z = np.where(P["hand"], Z + 45 + 30 * np.sqrt(d_hand / max(d_hand.max(), 1)), Z)  # hand held out in front
    w = M.astype(float)
    Zs = ndi.gaussian_filter(Z * w, 3) / np.maximum(ndi.gaussian_filter(w, 3), 1e-6)
    Z = np.where(M, Zs, 0)
    return np.where(P["hand"], np.maximum(Z, Zs), Z)


def rotation(yaw, pitch):
    a, b = np.radians(yaw), np.radians(pitch)
    Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
    Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]])
    return Rx @ Ry  # yaw first, then pitch (PointPortrait.astro does the same)


def outline_points(mask, step):
    """Evenly spaced points along the smoothed outline."""
    m = ndi.gaussian_filter(mask.astype(float), 1.0)
    out = []
    for c in measure.find_contours(m, 0.5):
        if len(c) < 40:
            continue
        seg = np.hypot(*np.diff(c, axis=0).T)
        t = np.concatenate([[0], np.cumsum(seg)])
        s = np.arange(0, t[-1], step)
        out.append(np.stack([np.interp(s, t, c[:, 1]), np.interp(s, t, c[:, 0])], 1))
    return np.concatenate(out)


def flame_base(flame, Z):
    """Where the flame sits on the lighter (bottom centre) and how tall it is in the drawing."""
    fy, fx = np.nonzero(flame)
    x, y = fx.mean(), fy.max()
    z = float(ndi.map_coordinates(Z, [[y - 4], [x]], order=1)[0]) + 6
    return x, y, z, float(np.ptp(fy))


def build(outline=False):
    im = np.asarray(Image.open(SRC).convert("RGBA")).astype(np.float32) / 255
    H, W = im.shape[:2]
    P = parts(im)
    M, Z = P["smooth"], relief(im, P)
    rgb = im[..., :3]
    lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    # See-through pixels still hold the old white background (in the gaps between strands of hair),
    # which showed as white dots along the hair in the dark theme: take their brightness from the
    # nearest solid pixel instead.
    iy, ix = ndi.distance_transform_edt(im[..., 3] <= 0.9, return_distances=False, return_indices=True)
    refl = ndi.gaussian_filter(lum[iy, ix], 1.4)
    dist = ndi.distance_transform_edt(M)

    # scan lines, inside the smoothed outline
    rng = np.random.default_rng(3)
    xy = []
    for y in np.arange(3, H, ROW):
        xs = np.arange(0, W, STEP) + rng.uniform(-0.3, 0.3, int(np.ceil(W / STEP)))
        xy.append(np.stack([xs, np.full_like(xs, y)], 1))
    xy = np.concatenate(xy)
    xy = xy[(xy[:, 0] >= 0) & (xy[:, 0] <= W - 1)]
    xi, yi = np.round(xy[:, 0]).astype(int), np.round(xy[:, 1]).astype(int)
    keep = M[yi, xi] & ~ndi.binary_dilation(P["flame"], iterations=5)[yi, xi]
    xy, xi, yi = xy[keep], xi[keep], yi[keep]
    r = np.clip((refl[yi, xi] - 0.04) / 0.86, 0, 1)
    edge = np.clip(dist[yi, xi] / EDGE, 0, 1)
    edge = edge * edge * (3 - 2 * edge)  # 0 at the outline, 1 from EDGE px inside

    if outline:  # an even row of dots along the outline (off: the fade alone looked cleaner)
        ol = outline_points(M, STEP * 0.85)
        xy = np.concatenate([xy, ol])
        r = np.concatenate([r, np.full(len(ol), 0.5)])  # mid-tone: about the same weight in both themes
        edge = np.concatenate([edge, np.ones(len(ol))])
        xi, yi = np.round(xy[:, 0]).astype(int).clip(0, W - 1), np.round(xy[:, 1]).astype(int).clip(0, H - 1)
    z = ndi.map_coordinates(Z, [xy[:, 1], xy[:, 0]], order=1)

    # per-point brightness terms (theme-independent)
    gy, gx = np.gradient(ndi.gaussian_filter(Z, 2.0))
    N = np.stack([-gx, -gy, np.ones_like(Z)], -1)
    N = (N / np.linalg.norm(N, axis=-1, keepdims=True))[yi, xi]
    R0 = rotation(*VIEW)
    L = np.array((-0.4, -0.6, 0.7)); L /= np.linalg.norm(L)
    lam = np.clip((N @ R0.T) @ L, 0, 1)  # light from the upper left
    fade = np.clip((H * 0.97 - xy[:, 1]) / (H * 0.16), 0, 1) ** 1.2  # fade out at the bottom
    front = P["hand"][yi, xi].astype(float)  # the hand hides what is behind it when the view turns

    c = np.array([W / 2, H / 2])
    pts = np.column_stack([xy - c, z])
    order = np.argsort((pts @ R0.T)[:, 2])  # far to near, for the default view
    pts, r, lam, edge, fade, front = pts[order], r[order], lam[order], edge[order], fade[order], front[order]

    fx, fy, fz, fh = flame_base(P["flame"], Z)
    flame = dict(x=round(fx - c[0], 1), y=round(fy - c[1], 1), z=round(fz, 1), h=round(fh, 1))

    # frame: big enough for every view the tilt can reach
    x0 = y0 = np.inf; x1 = y1 = -np.inf
    tip = np.array([[flame["x"], flame["y"] - 2.2 * fh, flame["z"]]])  # top of the flame and its glow
    for dyaw in (-TILT[0], 0, TILT[0]):
        for dpitch in (-TILT[1], 0, TILT[1]):
            q = np.concatenate([pts, tip]) @ rotation(VIEW[0] + dyaw, VIEW[1] + dpitch).T
            x0, x1 = min(x0, q[:, 0].min()), max(x1, q[:, 0].max())
            y0, y1 = min(y0, q[:, 1].min()), max(y1, q[:, 1].max())
    pad = 4.0
    frame = dict(x0=round(x0 - pad, 1), y0=round(y0 - pad, 1), w=round(x1 - x0 + 2 * pad, 1), h=round(y1 - y0 + 2 * pad, 1))
    return dict(pts=pts, n=len(pts), refl=r, lam=lam, edge=edge, fade=fade, front=front, frame=frame, flame=flame,
                M=M, Z=Z, c=c)


def write(D):
    OUT.mkdir(parents=True, exist_ok=True)
    q = np.round(D["pts"] * UNIT).astype(np.int16)
    u8 = lambda a: np.clip(np.round(a * 255), 0, 255).astype(np.uint8)
    with open(OUT / "points.bin", "wb") as f:
        f.write(struct.pack("<II", D["n"], 0))
        for k in range(3):
            f.write(q[:, k].astype("<i2").tobytes())
        for a in (D["refl"], D["lam"], D["edge"], D["fade"], D["front"]):
            f.write(u8(a).tobytes())
    fr = D["frame"]
    meta = dict(
        n=int(D["n"]), unit=UNIT, row=ROW,
        view=dict(yaw=VIEW[0], pitch=VIEW[1]), tilt=dict(yaw=TILT[0], pitch=TILT[1]),
        frame=fr, aspect=round(fr["h"] / fr["w"], 4), flame=D["flame"],
    )
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"points.bin: {D['n']} points ({(OUT / 'points.bin').stat().st_size // 1024} KB); aspect {meta['aspect']}")


def alpha_size(D, T, dark):
    """Opacity and radius of each dot (PointPortrait.astro computes the same)."""
    t = (D["refl"] if dark else 1 - D["refl"]) ** T["gamma"]
    a = (T["floor"] + (1 - T["floor"]) * t) * (0.65 + 0.35 * D["lam"]) * D["fade"] * (0.12 + 0.88 * D["edge"])
    size = (T["rmin"] + (T["rmax"] - T["rmin"]) * t) * (0.7 + 0.3 * D["edge"])
    return np.minimum(a, T["cap"]), size


def still(D, theme, width=480, ss=4, transparent=False):
    """Render the default view the way the component does (with occlusion), for previews."""
    T = THEMES[theme]
    pts, fr = D["pts"], D["frame"]
    R = rotation(*VIEW)
    p = pts @ R.T
    s = width * ss / fr["w"]
    px, py = (p[:, 0] - fr["x0"]) * s, (p[:, 1] - fr["y0"]) * s
    Wd, Hd = width * ss, int(round(fr["h"] * s))
    # occlusion from the dense surface
    M, Z, c = D["M"], D["Z"], D["c"]
    yy, xx = np.nonzero(M)
    dense = np.column_stack([xx - c[0], yy - c[1], Z[yy, xx]]) @ R.T
    res = 2 * ss
    zb = np.full((Hd // res + 3, Wd // res + 3), -1e9)
    np.maximum.at(zb, (((dense[:, 1] - fr["y0"]) * s / res).astype(int), ((dense[:, 0] - fr["x0"]) * s / res).astype(int)), dense[:, 2])
    zb = np.where(zb < -1e8, ndi.maximum_filter(zb, 3), zb)
    vis = p[:, 2] >= zb[(py / res).astype(int), (px / res).astype(int)] - 5
    a, size = alpha_size(D, T, theme == "dark")
    k = ss * width / 240.0
    ink = Image.new("L", (Wd, Hd), 0)
    di = ImageDraw.Draw(ink)
    for i in range(D["n"]):
        if vis[i] and a[i] >= 0.03:
            rr = size[i] * k
            di.ellipse((px[i] - rr, py[i] - rr, px[i] + rr, py[i] + rr), fill=int(round(255 * a[i])))
    h = int(round(Hd / ss))
    ink = ink.resize((width, h), Image.LANCZOS)
    # a still flame: glow plus a teardrop of warm dots (the page animates it)
    f = D["flame"]
    fb = np.array([f["x"], f["y"], f["z"]]) @ R.T
    bx, by, fh = (fb[0] - fr["x0"]) * s / ss, (fb[1] - fr["y0"]) * s / ss, f["h"] * s / ss * 1.1
    fire = Image.new("RGBA", (width, h), (0, 0, 0, 0))
    glow = Image.new("L", (width, h), 0)
    ImageDraw.Draw(glow).ellipse((bx - fh * 1.1, by - fh * 1.55, bx + fh * 1.1, by + fh * 0.65), fill=110 if theme == "dark" else 80)
    glow = glow.filter(ImageFilter.GaussianBlur(float(fh * 0.5)))
    fire = Image.alpha_composite(fire, Image.merge("RGBA", (*Image.new("RGB", (width, h), (255, 150, 70)).split(), glow)))
    # core: a soft orange teardrop with a blue base, like the animated one
    core = Image.new("L", (width * 4, h * 4), 0)
    ImageDraw.Draw(core).ellipse(((bx - fh * 0.2) * 4, (by - fh) * 4, (bx + fh * 0.2) * 4, by * 4), fill=235)
    core = core.filter(ImageFilter.GaussianBlur(float(fh * 0.35)))
    base = Image.new("L", (width * 4, h * 4), 0)
    ImageDraw.Draw(base).ellipse(((bx - fh * 0.12) * 4, (by - fh * 0.2) * 4, (bx + fh * 0.12) * 4, by * 4), fill=210)
    base = base.filter(ImageFilter.GaussianBlur(float(fh * 0.25)))
    dots = Image.merge("RGBA", (*Image.new("RGB", core.size, (255, 140, 40) if theme == "light" else (255, 214, 140)).split(), core))
    dots = Image.alpha_composite(dots, Image.merge("RGBA", (*Image.new("RGB", core.size, (110, 150, 235)).split(), base)))
    fire = Image.alpha_composite(fire, dots.resize((width, h), Image.LANCZOS))
    if transparent:
        out = Image.new("RGBA", (width, h), T["ink"] + (0,))
        out.putalpha(ink)
        return Image.alpha_composite(out, fire)
    bg = (10, 12, 16) if theme == "dark" else (255, 255, 255)
    out = Image.composite(Image.new("RGB", (width, h), T["ink"]), Image.new("RGB", (width, h), bg), ink).convert("RGBA")
    return Image.alpha_composite(out, fire).convert("RGB")


if __name__ == "__main__":
    D = build()
    write(D)
    still(D, "light", transparent=True).quantize(160, method=Image.Quantize.FASTOCTREE).save(OUT / "fallback.png", optimize=True)
    if "preview" in sys.argv[1:]:
        for theme in ("light", "dark"):
            still(D, theme).save(f"preview-{theme}.png")
        print("wrote preview-light.png and preview-dark.png in the current folder")

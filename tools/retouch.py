#!/usr/bin/env python3
"""Retouch Alla's portfolio photos (non-generative: the garments are never altered).

    python3 tools/retouch.py <folder-with-originals>

For each photo:
  * trims phone-screenshot bars / white margins
  * optional crop (fractions of width/height)
  * on the red satin backdrop: recolours only the backdrop (the red region
    connected to the frame edge, plus tiny enclosed specks seen through lace)
    to a deep oxblood, keeping the satin's texture
  * gentle global tone: neutral white balance, soft contrast, light sharpening
Writes JPGs to assets-src/ named work-*.jpg.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from scipy import ndimage

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets-src"

# name: (source file stem, red backdrop?, crop (l, t, r, b) as fractions or None)
PHOTOS = {
    "work-rose-front":      ("75d8d017", True,  None),
    "work-rose-back":       ("1c2e68eb", True,  None),
    "work-rose-side":       ("93005965", True,  None),
    "work-rose-detail":     ("ec8c4161", True,  None),
    "work-rose-back-detail": ("3590a42e", True, None),
    "work-rose-profile":    ("ae34de5c", True,  None),
    "work-rose-inside":     ("5c41ca5d", False, None),
    "work-rose-lining":     ("e92063f3", True,  None),
    "work-grey-hat":        ("de79c770", False, None),
    "work-grey":            ("2a4547eb", False, None),
    "work-grey-side":       ("138300ce", False, None),
    "work-sage":            ("55f27cdd", True,  None),
    "work-sage-catalogue":  ("3a079941", False, None),
    "work-ivory-lace":      ("e3acddb8", True,  (0.0, 0.0, 0.5, 1.0)),
    "work-ivory-lace-2":    ("e3acddb8", True,  (0.5, 0.0, 1.0, 1.0)),
    "work-aqua":            ("04302932", False, None),
    "work-soutache":        ("639f04ab", False, None),
}

OXBLOOD = np.array([96, 30, 27], dtype=np.float32)


def trim(im, tol=10):
    a = np.asarray(im.convert("L"), dtype=np.float32)
    def flat(v):
        return v.std() < tol and (v.mean() < 40 or v.mean() > 225)
    t, b, l, r = 0, a.shape[0], 0, a.shape[1]
    while t < b - 1 and flat(a[t, l:r]): t += 1
    while b > t + 1 and flat(a[b - 1, l:r]): b -= 1
    while l < r - 1 and flat(a[t:b, l]): l += 1
    while r > l + 1 and flat(a[t:b, r - 1]): r -= 1
    pad = 4  # shave anti-aliased edge of bars
    return im.crop((l + pad if l else 0, t + pad if t else 0,
                    r - pad if r < a.shape[1] else r, b - pad if b < a.shape[0] else b))


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def backdrop_mask(rgb):
    hsv = np.asarray(Image.fromarray(rgb).convert("HSV"), dtype=np.float32)
    h, s, v = hsv[..., 0], hsv[..., 1] / 255, hsv[..., 2] / 255
    redhue = (h < 9) | (h > 244)
    strong = redhue & (s > 0.62) & (v > 0.18)
    # paler satin highlights: same hue, lower saturation. Opening with a wide
    # disk keeps broad backdrop bands but drops small garment motifs (roses).
    weak = ((h < 10) | (h > 242)) & (s > 0.44) & (v > 0.18)
    weak = ndimage.binary_opening(weak, structure=disk(9))
    cand = strong | weak
    lab, n = ndimage.label(cand)
    if n == 0:
        return np.zeros(cand.shape, np.float32)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    keep = np.zeros(n + 1, bool)
    keep[border] = True
    keep[0] = False
    m = keep[lab]
    m = ndimage.binary_closing(m, structure=disk(2))
    m = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))
    return np.asarray(m, dtype=np.float32) / 255


def recolour(rgb, mask):
    f = rgb.astype(np.float32)
    lum = (0.299 * f[..., 0] + 0.587 * f[..., 1] + 0.114 * f[..., 2]) / 255
    lum = np.clip((lum - 0.12) / 0.6, 0, 1)
    shade = (0.5 + 0.9 * lum)[..., None]
    target = np.clip(OXBLOOD * shade, 0, 255)
    out = f * (1 - mask[..., None]) + target * mask[..., None]
    return out.clip(0, 255).astype(np.uint8)


def tone(im):
    a = np.asarray(im, dtype=np.float32)
    # soft levels (luminance only, so garment colours stay true): 0.5th → 99.6th percentile
    lo, hi = np.percentile(a, 0.5), np.percentile(a, 99.6)
    a = (a - lo) / max(hi - lo, 1) * 255
    im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    im = ImageEnhance.Contrast(im).enhance(1.04)
    return im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=2))


def process(src_dir, name, stem, red, crop):
    im = Image.open(Path(src_dir) / f"{stem}-image.jpg").convert("RGB")
    im = trim(im)
    if crop:
        w, h = im.size
        im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
        im = trim(im)
    if red:
        rgb = np.asarray(im)
        im = Image.fromarray(recolour(rgb, backdrop_mask(rgb)))
    im = tone(im)
    OUT.mkdir(exist_ok=True)
    im.save(OUT / f"{name}.jpg", "JPEG", quality=92, optimize=True)
    print(name, im.size)


if __name__ == "__main__":
    src = sys.argv[1]
    only = sys.argv[2:]
    for name, (stem, red, crop) in PHOTOS.items():
        if not only or name in only:
            process(src, name, stem, red, crop)

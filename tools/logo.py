#!/usr/bin/env python3
"""Generate the Atelier Alla Mode logo set as outlined SVG (no font dependency).

    python3 tools/logo.py <google-fonts>/ofl [font-key]

Writes to site/assets/brand/:
  lockup.svg     primary: dress-form illustration above ATELIER / ALLA MODE / tagline
  wordmark.svg   ATELIER / ALLA MODE (no illustration)
  header.svg     compact lockup for the site header (illustration + wordmark)
  seal.svg       round heritage seal: illustration in the centre, name arched around
  emblem.svg     the illustration alone
  monogram.svg   AM in a double oval (favicon, labels, tissue seals)
Colours use currentColor so every mark inherits ink or ivory.
"""
import math
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "assets" / "brand"

FONTS = {
    "cormorant": ("cormorantsc/CormorantSC-SemiBold.ttf", {}),
    "cinzel": ("cinzel/Cinzel[wght].ttf", {"wght": 480}),
    "marcellus": ("marcellus/Marcellus-Regular.ttf", {}),
    "forum": ("forum/Forum-Regular.ttf", {}),
}
DEFAULT_FONT = "cinzel"
TAGLINE = "COUTURE FOR ANTIQUE DOLLS"


def load(path, **axes):
    f = TTFont(path)
    if "fvar" in f:
        f = instantiateVariableFont(f, axes or {}, inplace=False)
    return f


class Text:
    def __init__(self, font):
        self.font = font
        self.cmap = font.getBestCmap()
        self.gs = font.getGlyphSet()
        self.upm = font["head"].unitsPerEm
        self.hmtx = font["hmtx"]

    def glyph(self, ch, size):
        g = self.cmap[ord(ch)]
        scale = size / self.upm
        pen = SVGPathPen(self.gs)
        if ch != " ":
            self.gs[g].draw(TransformPen(pen, (scale, 0, 0, -scale, 0, 0)))
        return pen.getCommands(), self.hmtx[g][0] * scale

    def layout(self, text, size, tracking=0.0):
        scale = size / self.upm
        x = 0.0
        pen = SVGPathPen(self.gs)
        for i, ch in enumerate(text):
            g = self.cmap[ord(ch)]
            if ch != " ":
                self.gs[g].draw(TransformPen(pen, (scale, 0, 0, -scale, x, 0)))
            x += self.hmtx[g][0] * scale
            if i < len(text) - 1:
                x += tracking * size
        return pen.getCommands(), x

    def cap(self, size):
        h = getattr(self.font["OS/2"], "sCapHeight", 0) or self.upm * 0.7
        return h * size / self.upm


# ------------------------------------------------------------ illustration ---
# Antique dress form on a turned stand: engraved shading, a tape measure over
# the shoulders, a needle drawing thread through. Drawn on a 120 x 150 grid.
BODY = ("M53 17.6 C53.4 21.5 52.6 24.6 49 27 C43 30.6 35.5 30.8 33.2 36.4 "
        "C31.2 41.6 31.6 48.6 33.8 54.8 C35.8 60.4 40.4 64.8 41.2 72 "
        "C41.8 78.6 37.2 86.8 35.6 94.6 C35 97.8 35.4 100.2 36.2 101.6 "
        "Q60 108.4 83.8 101.6 "
        "C84.6 100.2 85 97.8 84.4 94.6 C82.8 86.8 78.2 78.6 78.8 72 "
        "C79.6 64.8 84.2 60.4 86.2 54.8 C88.4 48.6 88.8 41.6 86.8 36.4 "
        "C84.5 30.8 77 30.6 71 27 C67.4 24.6 66.6 21.5 67 17.6 Z")


def figure(uid):
    hatch = "".join(f'<path d="M{x:.1f} 14 L{x - 30:.1f} 112"/>' for x in [70 + i * 2.3 for i in range(16)])
    ticks_l = "".join(f'<path d="M{44.2 - i * .28:.2f} {33 + i * 4.2:.1f} l1.9 .25"/>' for i in range(9))
    ticks_r = "".join(f'<path d="M{75.4 + i * .3:.2f} {33 + i * 3.8:.1f} l-1.9 .25"/>' for i in range(8))
    return f"""
<defs><clipPath id="body-{uid}"><path d="{BODY}"/></clipPath></defs>
<g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
  <g clip-path="url(#body-{uid})" stroke-width=".42" opacity=".55">{hatch}</g>
  <path d="{BODY}" stroke-width="1.5"/>
  <circle cx="60" cy="7" r="2.5" stroke-width="1.2"/>
  <path d="M60 9.5 V13" stroke-width="1.2"/>
  <path d="M51.5 13.2 H68.5 Q69.6 13.2 69.4 14.4 L68.6 17.4 H51.4 L50.6 14.4 Q50.4 13.2 51.5 13.2 Z" stroke-width="1.2"/>
  <path d="M55.2 22 C51 36 47.6 50 50.8 70 C52.6 82 51 94 49.6 104.4" stroke-width=".7" stroke-dasharray="1.4 1.8"/>
  <path d="M64.8 22 C69 36 72.4 50 69.2 70 C67.4 82 69 94 70.4 104.4" stroke-width=".7" stroke-dasharray="1.4 1.8"/>
  <path d="M41.4 71.2 Q60 76.6 78.6 71.2" stroke-width=".9"/>
  <path d="M51 21.6 C47 25 45.2 29 44.6 34 C43.4 44 42.6 56 41.4 68" stroke-width=".8"/>
  <path d="M53.6 22.6 C50 26 48.2 30 47.6 34.6 C46.4 44.4 45.6 56.2 44.4 68.4" stroke-width=".8"/>
  <path d="M41.4 68 L44.4 68.4" stroke-width=".8"/>
  <path d="M69 21.6 C73 25 75 29.6 75.6 34.6 C76.8 43.6 77.6 52 78.4 60.6" stroke-width=".8"/>
  <path d="M66.4 22.6 C70 26 72 30.2 72.6 35 C73.8 44 74.6 52.4 75.4 61" stroke-width=".8"/>
  <path d="M78.4 60.6 L75.4 61" stroke-width=".8"/>
  <path d="M51 21.6 Q60 18.6 69 21.6" stroke-width=".8"/>
  <g stroke-width=".55">{ticks_l}{ticks_r}</g>
  <path d="M60 106 V113" stroke-width="1.5"/>
  <ellipse cx="60" cy="115.4" rx="3.6" ry="2.3" stroke-width="1.2"/>
  <path d="M60 117.7 V125.4" stroke-width="1.5"/>
  <path d="M56.4 125.8 Q60 123.2 63.6 125.8 Q60 128.6 56.4 125.8 Z" stroke-width="1.1"/>
  <path d="M60 127.4 V136" stroke-width="1.5"/>
  <path d="M60 136 Q50.5 138 42 144.6 M60 136 Q69.5 138 78 144.6 M60 136 V145.6" stroke-width="1.35"/>
  <circle cx="42" cy="144.6" r="1" fill="currentColor" stroke="none"/>
  <circle cx="78" cy="144.6" r="1" fill="currentColor" stroke="none"/>
  <path d="M100 19 L81 38" stroke-width="1.2"/>
  <ellipse cx="98.3" cy="20.7" rx="2.3" ry=".85" transform="rotate(-45 98.3 20.7)" stroke-width=".85"/>
  <path d="M97.5 21.6 C106.5 29 107.5 45 99.5 57 C92.6 67.4 96.4 82 103 92" stroke-width=".75"/>
</g>"""


FIG_W, FIG_H = 120, 150


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" '
            f'width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')


def place(d, x, y):
    return f'<path fill="currentColor" transform="translate({x:.2f} {y:.2f})" d="{d}"/>'


def rule_with_word(T, word, size, track, W, y, gap=14, line=46):
    d, w = T.layout(word, size, track)
    cap = T.cap(size)
    mid = y + cap / 2
    x0 = (W - w) / 2
    lines = (f'<path d="M{x0 - gap - line:.1f} {mid:.1f}h{line} M{x0 + w + gap:.1f} {mid:.1f}h{line}" '
             f'stroke="currentColor" stroke-width=".9"/>'
             f'<path d="M{x0 - gap - line - 4:.1f} {mid:.1f}l2.4 -2.4 2.4 2.4 -2.4 2.4z'
             f'M{x0 + w + gap + line + 4:.1f} {mid:.1f}l-2.4 -2.4 -2.4 2.4 2.4 2.4z" fill="currentColor"/>')
    return lines + place(d, x0, y + cap), cap


def arc_text(T, text, size, track, cx, cy, r, top=True):
    items = [T.glyph(ch, size) for ch in text]
    total = sum(a for _, a in items) + track * size * (len(items) - 1)
    span = total / r
    out, x = [], 0.0
    for d, adv in items:
        mid = x + adv / 2
        if top:
            th = -math.pi / 2 - span / 2 + mid / r
            rot = math.degrees(th) + 90
        else:
            th = math.pi / 2 + span / 2 - mid / r
            rot = math.degrees(th) - 90
        px, py = cx + r * math.cos(th), cy + r * math.sin(th)
        if d:
            out.append(f'<path fill="currentColor" transform="translate({px:.2f} {py:.2f}) rotate({rot:.2f}) '
                       f'translate({-adv / 2:.2f} 0)" d="{d}"/>')
        x += adv + track * size
    return "".join(out)


def main(ofl, font_key=DEFAULT_FONT):
    ofl = Path(ofl)
    rel, axes = FONTS[font_key]
    T = Text(load(ofl / rel, **axes))
    OUT.mkdir(parents=True, exist_ok=True)

    main_d, main_w = T.layout("ALLA MODE", 64, tracking=0.12)
    main_cap = T.cap(64)
    tag_d, tag_w = T.layout(TAGLINE, 13.5, tracking=0.3)
    tag_cap = T.cap(13.5)

    # primary lockup
    W = max(main_w, tag_w) + 16
    s = 1.05
    parts = [f'<g transform="translate({(W - FIG_W * s) / 2:.2f} 0) scale({s})">{figure("lockup")}</g>']
    y = FIG_H * s + 26
    rw, cap = rule_with_word(T, "ATELIER", 17, 0.5, W, y)
    parts.append(rw)
    y += cap + 16
    parts.append(place(main_d, (W - main_w) / 2, y + main_cap))
    y += main_cap + 22
    parts.append(place(tag_d, (W - tag_w) / 2, y + tag_cap))
    y += tag_cap + 2
    (OUT / "lockup.svg").write_text(svg(W, y, "".join(parts), "Atelier Alla Mode — Couture for Antique Dolls"))

    # wordmark
    W2 = main_w + 120
    rw, cap = rule_with_word(T, "ATELIER", 17, 0.5, W2, 0)
    y = cap + 14
    body = rw + place(main_d, (W2 - main_w) / 2, y + main_cap)
    (OUT / "wordmark.svg").write_text(svg(W2, y + main_cap + 1, body, "Atelier Alla Mode"))

    # header lockup
    hs = 0.62
    parts = [f'<g transform="translate({(W2 - FIG_W * hs) / 2:.2f} 0) scale({hs})">{figure("header")}</g>']
    y = FIG_H * hs + 14
    rw, cap = rule_with_word(T, "ATELIER", 17, 0.5, W2, y)
    parts.append(rw)
    y += cap + 14
    parts.append(place(main_d, (W2 - main_w) / 2, y + main_cap))
    (OUT / "header.svg").write_text(svg(W2, y + main_cap + 1, "".join(parts), "Atelier Alla Mode"))

    # seal
    S, c = 240, 120
    ring = (f'<g fill="none" stroke="currentColor"><circle cx="{c}" cy="{c}" r="116" stroke-width="1.6"/>'
            f'<circle cx="{c}" cy="{c}" r="111.5" stroke-width=".6"/>'
            f'<circle cx="{c}" cy="{c}" r="78" stroke-width=".6"/></g>')
    top = arc_text(T, "ATELIER · ALLA MODE", 15.5, 0.22, c, c, 89, top=True)
    bot = arc_text(T, TAGLINE, 10.5, 0.2, c, c, 89 + 7.5, top=False)
    dots = (f'<path d="M{c - 92:.1f} {c}l2.6 -2.6 2.6 2.6 -2.6 2.6z M{c + 92:.1f} {c}l-2.6 -2.6 -2.6 2.6 2.6 2.6z" '
            f'fill="currentColor"/>')
    fs = 0.82
    fig = f'<g transform="translate({c - FIG_W * fs / 2:.2f} {c - FIG_H * fs / 2 + 2:.2f}) scale({fs})">{figure("seal")}</g>'
    (OUT / "seal.svg").write_text(svg(S, S, ring + top + bot + dots + fig, "Atelier Alla Mode seal"))

    # emblem alone
    (OUT / "emblem.svg").write_text(svg(FIG_W, FIG_H, figure("emblem"), "Atelier Alla Mode emblem"))

    # monogram + favicon
    a_d, a_w = T.layout("A", 50)
    m_d, m_w = T.layout("M", 50)
    mcap = T.cap(50)
    overlap = 7
    x0 = (100 - (a_w + m_w - overlap)) / 2
    base = 50 + mcap / 2
    mono = (f'<g fill="none" stroke="currentColor"><ellipse cx="50" cy="50" rx="44" ry="47" stroke-width="1.3"/>'
            f'<ellipse cx="50" cy="50" rx="40.5" ry="43.5" stroke-width=".55"/></g>'
            + place(a_d, x0, base) + place(m_d, x0 + a_w - overlap, base))
    (OUT / "monogram.svg").write_text(svg(100, 100, mono, "Atelier Alla Mode monogram"))
    fav = mono.replace('stroke="currentColor"', 'stroke="#f4f0e9"').replace('fill="currentColor"', 'fill="#f4f0e9"')
    (ROOT / "site" / "favicon.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="14" fill="#6b1f24"/>{fav}</svg>\n')
    print("logo set written with", font_key)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "fonts/ofl", sys.argv[2] if len(sys.argv) > 2 else DEFAULT_FONT)

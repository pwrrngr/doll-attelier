#!/usr/bin/env python3
"""Generate the Atelier Alla Mode logo set as outlined SVG (no font dependency).

    python3 tools/logo.py /path/to/google-fonts/ofl

Writes to site/assets/brand/:
  lockup.svg       emblem + ATELIER / ALLA MODE / COUTURE FOR ANTIQUE DOLLS (stacked, primary)
  wordmark.svg     ATELIER / ALLA MODE (header)
  emblem.svg       dress-form emblem alone
  monogram.svg     AM monogram in an oval (favicon, social, labels)
Colours use currentColor so the marks inherit ink or ivory.
"""
import sys
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "assets" / "brand"


def load(path, **axes):
    f = TTFont(path)
    if "fvar" in f:
        f = instantiateVariableFont(f, axes, inplace=False)
    return f


class Text:
    def __init__(self, font):
        self.font = font
        self.cmap = font.getBestCmap()
        self.gs = font.getGlyphSet()
        self.upm = font["head"].unitsPerEm
        self.hmtx = font["hmtx"]

    def layout(self, text, size, tracking=0.0):
        """Return (svg path d, width) for text at size, tracking in em."""
        scale = size / self.upm
        x = 0.0
        pen = SVGPathPen(self.gs)
        for i, ch in enumerate(text):
            g = self.cmap.get(ord(ch))
            if g is None:
                raise SystemExit(f"glyph missing for {ch!r}")
            adv = self.hmtx[g][0]
            if ch != " ":
                t = TransformPen(pen, (scale, 0, 0, -scale, x, 0))
                self.gs[g].draw(t)
            x += adv * scale
            if i < len(text) - 1:
                x += tracking * size
        return pen.getCommands(), x

    def cap_height(self, size):
        os2 = self.font["OS/2"]
        h = getattr(os2, "sCapHeight", 0) or self.upm * 0.7
        return h * size / self.upm


# ---------------------------------------------------------------- emblem ---
# An antique dress form on a turned stand, a needle and thread drawn through it.
# Drawn on a 120 x 150 grid.
EMBLEM = """
<g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
  <!-- cameo frame -->
  <ellipse cx="60" cy="75" rx="56" ry="72" stroke-width="1.1"/>
  <ellipse cx="60" cy="75" rx="52.6" ry="68.4" stroke-width=".45"/>
  <g transform="translate(12 14) scale(.8)">
  <!-- finial and neck cap -->
  <circle cx="60" cy="7" r="2.4" stroke-width="1.1"/>
  <path d="M60 9.4 V13" stroke-width="1.1"/>
  <path d="M51.5 13.2 H68.5 Q69.6 13.2 69.4 14.4 L68.6 17.4 H51.4 L50.6 14.4 Q50.4 13.2 51.5 13.2 Z" stroke-width="1.1"/>
  <!-- body -->
  <path d="M53 17.6 C53.4 21.5 52.6 24.6 49 27 C43 30.6 35.5 30.8 33.2 36.4
           C31.2 41.6 31.6 48.6 33.8 54.8 C35.8 60.4 40.4 64.8 41.2 72
           C41.8 78.6 37.2 86.8 35.6 94.6 C35 97.8 35.4 100.2 36.2 101.6" stroke-width="1.35"/>
  <path d="M67 17.6 C66.6 21.5 67.4 24.6 71 27 C77 30.6 84.5 30.8 86.8 36.4
           C88.8 41.6 88.4 48.6 86.2 54.8 C84.2 60.4 79.6 64.8 78.8 72
           C78.2 78.6 82.8 86.8 84.4 94.6 C85 97.8 84.6 100.2 83.8 101.6" stroke-width="1.35"/>
  <path d="M36.2 101.6 Q60 108.4 83.8 101.6" stroke-width="1.35"/>
  <!-- princess seams and waist tape -->
  <path d="M55.2 22 C51 36 47.6 50 50.8 70 C52.6 82 51 94 49.6 104.4" stroke-width=".7" stroke-dasharray="1.4 1.8" opacity=".8"/>
  <path d="M64.8 22 C69 36 72.4 50 69.2 70 C67.4 82 69 94 70.4 104.4" stroke-width=".7" stroke-dasharray="1.4 1.8" opacity=".8"/>
  <path d="M41.4 71.2 Q60 76.6 78.6 71.2" stroke-width=".8"/>
  <!-- turned stand -->
  <path d="M60 105.4 V113" stroke-width="1.35"/>
  <ellipse cx="60" cy="115.4" rx="3.4" ry="2.2" stroke-width="1.1"/>
  <path d="M60 117.6 V125.6" stroke-width="1.35"/>
  <path d="M56.6 125.8 Q60 123.4 63.4 125.8 Q60 128.4 56.6 125.8 Z" stroke-width="1"/>
  <path d="M60 127.2 V136" stroke-width="1.35"/>
  <path d="M60 136 Q51 138 43 144 M60 136 Q69 138 77 144 M60 136 V145" stroke-width="1.2"/>
  <!-- needle through the shoulder, thread falling in one line -->
  <path d="M97 21 L75 43" stroke-width="1.1"/>
  <ellipse cx="95.4" cy="22.6" rx="2.2" ry=".8" transform="rotate(-45 95.4 22.6)" stroke-width=".8"/>
  <path d="M94.5 23.6 C103 31 104.5 46 97 58 C90.5 68.4 94 82 100 92" stroke-width=".7"/>
  </g>
</g>
"""
EMBLEM_W, EMBLEM_H = 120, 150


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" '
            f'width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')


def main(ofl):
    ofl = Path(ofl)
    bodoni = Text(load(ofl / "bodonimoda" / "BodoniModa[opsz,wght].ttf", wght=470, opsz=28))
    bodoni_text = Text(load(ofl / "bodonimoda" / "BodoniModa[opsz,wght].ttf", wght=520, opsz=11))
    OUT.mkdir(parents=True, exist_ok=True)

    # Wordmark (header): ATELIER small above ALLA MODE
    main_d, main_w = bodoni.layout("ALLA MODE", 60, tracking=0.16)
    cap = bodoni.cap_height(60)
    sub_d, sub_w = bodoni_text.layout("ATELIER", 17, tracking=0.6)
    sub_cap = bodoni_text.cap_height(17)
    gap = 12
    W = max(main_w, sub_w)
    H = sub_cap + gap + cap
    body = (f'<g fill="currentColor">'
            f'<path transform="translate({(W - sub_w) / 2:.2f} {sub_cap:.2f})" d="{sub_d}"/>'
            f'<path transform="translate({(W - main_w) / 2:.2f} {H:.2f})" d="{main_d}"/>'
            f'</g>')
    (OUT / "wordmark.svg").write_text(svg(W, H + 1, body, "Atelier Alla Mode"))

    # Primary lockup: emblem, ATELIER, ALLA MODE, rule, tagline
    tag_d, tag_w = bodoni_text.layout("COUTURE FOR ANTIQUE DOLLS", 13, tracking=0.36)
    tag_cap = bodoni_text.cap_height(13)
    pad = 6
    W2 = max(main_w, tag_w) + pad * 2
    em_scale = 0.82
    em_w, em_h = EMBLEM_W * em_scale, EMBLEM_H * em_scale
    y = 0
    parts = [f'<g color="currentColor" transform="translate({(W2 - em_w) / 2:.2f} 0) scale({em_scale})">{EMBLEM}</g>']
    y += em_h + 30
    parts.append(f'<path fill="currentColor" transform="translate({(W2 - sub_w) / 2:.2f} {y + sub_cap:.2f})" d="{sub_d}"/>')
    y += sub_cap + gap
    parts.append(f'<path fill="currentColor" transform="translate({(W2 - main_w) / 2:.2f} {y + cap:.2f})" d="{main_d}"/>')
    y += cap + 24
    parts.append(f'<path d="M{W2 / 2 - 36:.1f} {y:.1f} H{W2 / 2 - 6:.1f} M{W2 / 2 + 6:.1f} {y:.1f} H{W2 / 2 + 36:.1f}" stroke="currentColor" stroke-width=".8"/>'
                 f'<path d="M{W2 / 2:.1f} {y - 2.6:.1f} l2.6 2.6 -2.6 2.6 -2.6 -2.6 z" fill="currentColor"/>')
    y += 22
    parts.append(f'<path fill="currentColor" transform="translate({(W2 - tag_w) / 2:.2f} {y + tag_cap:.2f})" d="{tag_d}"/>')
    y += tag_cap + 2
    (OUT / "lockup.svg").write_text(svg(W2, y, "".join(parts), "Atelier Alla Mode — Couture for Antique Dolls"))

    # Emblem alone
    (OUT / "emblem.svg").write_text(svg(EMBLEM_W, EMBLEM_H, EMBLEM, "Atelier Alla Mode emblem"))

    # Monogram: A M in a thin double oval
    a_d, a_w = bodoni.layout("A", 52, 0)
    m_d, m_w = bodoni.layout("M", 52, 0)
    mcap = bodoni.cap_height(52)
    S = 100
    overlap = 9
    total = a_w + m_w - overlap
    x0 = (S - total) / 2
    base = S / 2 + mcap / 2
    mono = (f'<g fill="none" stroke="currentColor"><ellipse cx="50" cy="50" rx="44" ry="47" stroke-width="1.2"/>'
            f'<ellipse cx="50" cy="50" rx="40.5" ry="43.5" stroke-width=".5"/></g>'
            f'<g fill="currentColor"><path transform="translate({x0:.2f} {base:.2f})" d="{a_d}"/>'
            f'<path transform="translate({x0 + a_w - overlap:.2f} {base:.2f})" d="{m_d}"/></g>')
    (OUT / "monogram.svg").write_text(svg(S, S, mono, "Atelier Alla Mode monogram"))

    # Favicon: monogram on oxblood
    fav = mono.replace('stroke="currentColor"', 'stroke="#f4f0e9"').replace('fill="currentColor"', 'fill="#f4f0e9"')
    (ROOT / "site" / "favicon.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="14" fill="#6b1f24"/>{fav}</svg>\n')
    print("wrote", ", ".join(p.name for p in OUT.glob("*.svg")), "+ favicon.svg")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "fonts/ofl")

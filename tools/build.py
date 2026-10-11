#!/usr/bin/env python3
"""Build the static site: src/ -> site/.

Usage:
    python3 tools/build.py            # build pages
    python3 tools/build.py --images   # also (re)make responsive JPGs from assets-src/

Edit CONFIG below for the maker's name, email and site URL. Pages live in
src/pages/*.html, each starting with a small header comment:

    <!--
    title: The Maker
    description: One sentence for search results.
    nav: maker            (home | maker | savoir-faire | portfolio | commissions)
    header: light         (light = white header over a dark hero image)
    -->

Image shortcode inside pages:  [[img name | alt text | sizes | eager]]
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "site"
IMG_OUT = OUT / "images"
IMG_SRC = ROOT / "assets-src"

CONFIG = {
    "SITE_NAME": "The Doll Atelier",
    "MAKER": "Alla",                  # <- her name, exactly as it should appear
    "EMAIL": "hello@thedollatelier.com",  # <- real enquiry address
    "SITE_URL": "https://pwrrngr.github.io/doll-attelier/",
}

WIDTHS = (800, 1600, 2400)

NAV = [
    ("home", "index.html", "Maison"),
    ("maker", "maker.html", "About"),
    ("savoir-faire", "savoir-faire.html", "Savoir-faire"),
    ("portfolio", "portfolio.html", "Portfolio"),
    ("commissions", "commissions.html", "Commissions"),
]


def make_images():
    from PIL import Image  # noqa: WPS433

    IMG_OUT.mkdir(parents=True, exist_ok=True)
    for src in sorted(IMG_SRC.glob("*.*")):
        if src.suffix.lower() not in (".png", ".jpg", ".jpeg"):
            continue
        im = Image.open(src).convert("RGB")
        for w in WIDTHS:
            if w > im.width * 1.05 and w != WIDTHS[0]:
                continue
            target = IMG_OUT / f"{src.stem}-{w}.jpg"
            h = round(im.height * min(w, im.width) / im.width)
            im.resize((min(w, im.width), h), Image.LANCZOS).save(
                target, "JPEG", quality=82, optimize=True, progressive=True)
        print("image", src.stem, im.size)


def image_variants(name):
    found = []
    for w in WIDTHS:
        p = IMG_OUT / f"{name}-{w}.jpg"
        if p.exists():
            found.append((w, p))
    if not found:
        raise SystemExit(f"Missing image variants for '{name}'. Run with --images.")
    return found


def img_tag(match):
    parts = [p.strip() for p in match.group(1).split("|")]
    name, alt = parts[0], parts[1] if len(parts) > 1 else ""
    sizes = parts[2] if len(parts) > 2 and parts[2] else "100vw"
    eager = len(parts) > 3 and parts[3] == "eager"
    variants = image_variants(name)
    from PIL import Image  # noqa: WPS433
    w0, p0 = variants[min(1, len(variants) - 1)]
    with Image.open(p0) as im:
        width, height = im.size
    srcset = ", ".join(f"images/{p.name} {Image.open(p).width}w" for _, p in variants)
    attrs = [
        f'src="images/{p0.name}"',
        f'srcset="{srcset}"',
        f'sizes="{sizes}"',
        f'width="{width}" height="{height}"',
        f'alt="{html.escape(alt, quote=True)}"',
        'decoding="async"',
        'fetchpriority="high"' if eager else 'loading="lazy"',
    ]
    return "<img " + " ".join(attrs) + ">"


def parse_page(text):
    m = re.match(r"\s*<!--(.*?)-->\s*", text, re.S)
    meta = {}
    if m:
        for line in m.group(1).strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text


def nav_links(active, cls=""):
    out = []
    for key, href, label in NAV:
        cur = ' aria-current="page"' if key == active else ""
        out.append(f'<a href="{href}"{cur}>{label}</a>')
    return out


def fill(template, values):
    for k, v in values.items():
        template = template.replace("{{" + k + "}}", v)
    return template


def build():
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    for page in sorted((SRC / "pages").glob("*.html")):
        meta, body = parse_page(page.read_text(encoding="utf-8"))
        active = meta.get("nav", "")
        links = nav_links(active)
        menu = "\n".join(f"<li>{a}</li>" for a in links)
        body = re.sub(r"\[\[img\s+(.*?)\]\]", img_tag, body, flags=re.S)
        title = meta.get("title", CONFIG["SITE_NAME"])
        full_title = CONFIG["SITE_NAME"] if page.stem == "index" and title == CONFIG["SITE_NAME"] else f"{title} — {CONFIG['SITE_NAME']}"
        values = dict(CONFIG)
        values.update({
            "TITLE": html.escape(full_title),
            "DESCRIPTION": html.escape(meta.get("description", "")),
            "OG_IMAGE": CONFIG["SITE_URL"] + "images/" + meta.get("og", "hands-lace") + "-1600.jpg",
            "CANONICAL": CONFIG["SITE_URL"] + ("" if page.stem == "index" else page.name),
            "HEADER_CLASS": "site-header is-light" if meta.get("header") == "light" else "site-header",
            "NAV_LEFT": "".join(links[1:3]),
            "NAV_RIGHT": "".join(links[3:5]),
            "MENU": menu,
            "BODY": body,
            "PAGE": page.stem,
        })
        html_out = fill(layout, values)
        html_out = fill(html_out, CONFIG)  # placeholders used inside page bodies
        (OUT / page.name).write_text(html_out, encoding="utf-8")
        print("page", page.name)


if __name__ == "__main__":
    if "--images" in sys.argv:
        make_images()
    build()

# The Doll Atelier

Website for Alla, a master dressmaker — born in Ukraine, forty years in European dress design and atelier work — who now makes couture garments for antique dolls, for collectors in Japan, England and Spain.

Live: https://pwrrngr.github.io/doll-attelier/

## Pages

| Page | File | Purpose |
|---|---|---|
| Maison (home) | `src/pages/index.html` | Hero, manifesto, selected works, heritage, savoir-faire, worldwide, commission CTA |
| About | `src/pages/maker.html` | Her story, 40 years, Ukrainian heritage, principles |
| Savoir-faire | `src/pages/savoir-faire.html` | Six stages of making, materials glossary, techniques |
| Portfolio | `src/pages/portfolio.html` | Each garment with era, materials, handwork; collections by country |
| Commissions | `src/pages/commissions.html` | How it works, enquiry form (opens a prepared email), FAQ |

## Editing

1. Edit text in `src/pages/*.html` (shared header/footer in `src/layout.html`).
2. Her name, the enquiry email and the site URL are set **once** in `CONFIG` at the top of `tools/build.py`.
3. Rebuild: `python3 tools/build.py` (add `--images` after adding or replacing photos in `assets-src/`; needs Pillow).
4. Commit `src/`, `site/` and `assets-src/`. Pushing to `main` publishes `site/` to GitHub Pages.

Preview locally: `cd site && python3 -m http.server 8000`.

### Images

Originals live in `assets-src/` (not published). The build makes 800/1600/2400px JPGs in `site/images/`. In pages, use `[[img name | alt text | sizes]]`.

- `pearl-parlour`, `blue-hour`, `oxblood`, `worktable` — from the first ChatGPT draft
- the rest — mood imagery generated with Artlist (atmosphere only, not presented as her finished work)

## Before launch — confirm with the client

- [x] Her name — Alla (`CONFIG["MAKER"]`)
- [ ] Real enquiry email (`CONFIG["EMAIL"]`)
- [ ] **Portfolio photos of her real garments.** The three portfolio images look AI-generated; replace them, and correct titles, eras and materials
- [ ] Her story copy on the About page — born in Ukraine, European dressmaking, running an atelier, moving to dolls
- [ ] The manifesto line signed with her name on the home page
- [ ] Principles: "one pair of hands / nothing outsourced", "documented as new work", garments that "come away cleanly"
- [ ] "A limited number of commissions each season"; FAQ answers on timelines and shipping
- [ ] Optional: Instagram link, real collector testimonials (only with permission, never invented)

## Design notes

Ivory, ink and oxblood; Cormorant Garamond (display), EB Garamond (text), Jost (labels), all with Cyrillic. Heritage is framed as European couture: French atelier terms mark sections (l’héritage, l’atelier, le métier, fait main), and a small red-and-black cross-stitch band runs through the site as a quiet folk-embroidery accent.

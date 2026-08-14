# Site: shaikidris.github.io

Static site for two public Collatz papers. No framework at runtime — plain
HTML, CSS, and vanilla JavaScript, served from
`https://shaikidris.github.io/`.

## What lives where

The **root** is the current flagship paper; the **earlier** paper keeps its
full page under `/cet/`.

```
index.html                  Polylogarithmic Descent (v3.2.0) — landing page
paper/collatz-first-passage.pdf   exact Zenodo v3.2.0 PDF
code/index.html             theorem -> Lean declaration map (11 public theorems)

cet/index.html              Quantitative Collatz Descent (v2.0.2) — landing page
cet/paper/index.html        full v2.0.2 manuscript rendered to HTML (generated)
cet/paper/collatz-endpoint-transport.pdf   exact Zenodo v2.0.2 PDF
cet/code/index.html         v2.0.2 theorem -> Lean map

assets/site.css             shared design system (light/dark aware)
assets/paper.css            paper-page-only layout (sticky TOC, reading measure)
assets/figures.js           figure engine plus browser-local study interactions
assets/figure-data.json     generated numeric data for the /cet/ figures
assets/mathjax/             vendored MathJax 3.2.2 bundle, WOFF fonts, licence
assets/og-card.png          social-preview image — currently CET-specific
assets/favicon.svg
scripts/                    generators; see below
robots.txt, sitemap.xml, .nojekyll
```

**Asset paths are root-absolute** (`/assets/...`), not relative, so pages can
move between directories without breaking. `assets/figures.js` fetches
`/assets/figure-data.json` for the same reason.

## The two records

| | Root (`/`) | Earlier (`/cet/`) |
|---|---|---|
| Article | [10.5281/zenodo.21931194](https://doi.org/10.5281/zenodo.21931194) v3.2.0 | [10.5281/zenodo.21851173](https://doi.org/10.5281/zenodo.21851173) v2.0.2 |
| Formalization | [10.5281/zenodo.21930432](https://doi.org/10.5281/zenodo.21930432) | [10.5281/zenodo.21797535](https://doi.org/10.5281/zenodo.21797535) |
| Source | [FirstPassageLinearTransport](https://github.com/shaikidris/FirstPassageLinearTransport) tag `lean-v3.2.0` | [CET](https://github.com/shaikidris/CET) tag `v2.0.1` |

The two papers are logically independent and use different proof
architectures. Neither page may borrow theorem statements, ranges, or
numbering from the other.

## Regenerating things

```sh
python3 scripts/make_figure_data.py   # iterates the real shortcut Collatz map;
                                       # writes assets/figure-data.json
python3 scripts/make_og_card.py       # rebuilds assets/og-card.png (needs Pillow)
python3 scripts/build_paper.py        # re-renders the CET manuscript page
```

`build_paper.py` reads
`~/research/collatz/CET-Sigma/rewrite/collatz_endpoint_transport_main.md` and
writes the CET manuscript page. **Its output path still points at the old
`paper/` location** — update it to `cet/paper/` before the next CET
regeneration.

Requires `pandoc` and Python 3 with Pillow.

### Known follow-ups

- `assets/og-card.png` still shows the CET card. The root page therefore omits
  `og:image` rather than advertising the wrong paper. Regenerate for v3.2.0 and
  add the `og:image` / `twitter:image` tags back to `index.html`.
- The root page is a landing page only. A rendered full-text HTML edition of
  the v3.2.0 manuscript (the `/cet/paper/` equivalent) is not built yet.

## Content boundary

Every page is synchronized to a **published** record — a Zenodo DOI and a
public tag. No unpublished or internal draft is a source for this site. See
`CONTENT-PROMPT.md` for the per-paper source of truth and the update gate.

## Preview locally

```sh
cd ~/research/collatz/site
python3 -m http.server 4823
# open http://localhost:4823/
```

## Deployment

The repo is `shaikidris/shaikidris.github.io` on the personal `shaikidris`
account (**not** `shaiki_Zeta` — see `~/research/collatz/AGENTS.md`), served by
GitHub Pages from `main` at the root folder. `.nojekyll` is present.

After a structural change like the `/cet/` relocation, resubmit
`https://shaikidris.github.io/sitemap.xml` in Google Search Console and Bing
Webmaster Tools. The `citation_*` tags and `ScholarlyArticle` JSON-LD on each
landing page are what Google Scholar needs to index them as citable documents;
re-crawling after a URL move can take several weeks.

**Do not push or deploy without separate explicit authorization.**

# Site: shaikidris.github.io

Static site for two public Collatz papers. No framework at runtime — plain
HTML, CSS, and vanilla JavaScript, served from
`https://shaikidris.github.io/`.

## What lives where

The **root** is the current flagship paper; the **earlier** paper keeps its
full page under `/cet/`.

```
index.html                  Polylogarithmic Descent (v3.2.3) — landing page
paper/collatz-first-passage.pdf   exact Zenodo v3.2.3 PDF
code/index.html             theorem -> Lean declaration map (11 public theorems)

cet/index.html              Quantitative Collatz Descent (v2.0.2) — landing page
cet/paper/index.html        full v2.0.2 manuscript rendered to HTML (generated)
cet/paper/collatz-endpoint-transport.pdf   exact Zenodo v2.0.2 PDF
cet/code/index.html         v2.0.2 theorem -> Lean map

assets/site.css             shared design system (light/dark aware)
assets/paper.css            paper-page-only layout (sticky TOC, reading measure)
assets/figures.js           figure engine plus browser-local study interactions
assets/figure-data.json     generated numeric data for the /cet/ figures
assets/figures-polylog.js   root-paper figures and browser-local interactions
assets/figure-data-polylog.json   generated data for root-paper figures
assets/collatz-primer-core.js     exact standard/shortcut orbit calculator
assets/mathjax/             vendored MathJax 3.2.2 bundle, WOFF fonts, licence
assets/og-card.png          1200x630 social-preview image for the root paper
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
| Article | [SSRN Paper 7290240](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7290240), DOI [10.2139/ssrn.7290240](https://doi.org/10.2139/ssrn.7290240); versioned archive [10.5281/zenodo.21984038](https://doi.org/10.5281/zenodo.21984038) v3.2.3 | [10.5281/zenodo.21851173](https://doi.org/10.5281/zenodo.21851173) v2.0.2 |
| Direct PDF | [Version 3.2.3](https://shaikidris.github.io/paper/collatz-first-passage.pdf) | [Version 2.0.2](https://shaikidris.github.io/cet/paper/collatz-endpoint-transport.pdf) |
| Formalization | [10.5281/zenodo.21930432](https://doi.org/10.5281/zenodo.21930432) | [10.5281/zenodo.21797535](https://doi.org/10.5281/zenodo.21797535) |
| Source | [FirstPassageLinearTransport](https://github.com/shaikidris/FirstPassageLinearTransport) tag `lean-v3.2.0` | [CET](https://github.com/shaikidris/CET) tag `v2.0.1` |

The two papers are logically independent and use different proof
architectures. Neither page may borrow theorem statements, ranges, or
numbering from the other.

## Regenerating things

```sh
python3 scripts/make_figure_data.py   # iterates the real shortcut Collatz map;
                                       # writes assets/figure-data.json
python3 scripts/make_figure_data_polylog.py  # root-paper figures and widgets
python3 scripts/make_og_card.py       # rebuilds assets/og-card.png (needs Pillow)
python3 scripts/build_paper.py        # re-renders the CET manuscript page
```

`build_paper.py` reads
`~/research/collatz/CET-Sigma/rewrite/collatz_endpoint_transport_main.md` and
writes the CET manuscript page at `cet/paper/index.html`.

Requires `pandoc` and Python 3 with Pillow.

The beginner orbit arithmetic has a dependency-free regression check:

```sh
node scripts/test_collatz_primer.js
```

### Known follow-up

The root page is a landing page only. A rendered full-text HTML edition of
the v3.2.3 manuscript (the `/cet/paper/` equivalent) is not built yet.

## Content boundary

Every page is synchronized to a **published** record — a Zenodo DOI and a
public tag. No unpublished or internal draft is a source for this site. See
`CONTENT-PROMPT.md` for the per-paper source of truth and the update gate.

The root-page beginner orbit primer is an exact browser-local computation,
not a theorem illustration generated from sampled data. It defaults to the
standard Collatz map and can switch explicitly to the shortcut map used in the
paper. It must retain finite step and display-size caps, and a capped run must
never be described as evidence for or against the pointwise conjecture.

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

GitHub Pages currently serves static assets with a ten-minute browser cache.
Whenever root-page CSS, JavaScript, or generated figure data changes, bump the
shared `?v=` revision on the corresponding URLs in `index.html` and the figure
data fetch in `assets/figures-polylog.js`. This prevents a newly deployed HTML
page from running against stale interaction code. Interactive controls should
also use `type="button"` rather than native form submission, so missing or stale
JavaScript cannot navigate the page.

### Analytics

All public HTML pages load GoatCounter with the site endpoint
`https://shaikidris.goatcounter.com/count`. The endpoint is a public site
identifier, not a credential. GoatCounter's default localhost filter prevents
local previews from being counted.

Important outbound links and interactive controls use
`data-goatcounter-click` event names. Event names describe only the action
(for example, `root-paper-pdf` or `cet-orbit-run`); never include form values,
starting integers, slider values, or other visitor-entered data. New public
HTML pages must include both the GoatCounter script in `<head>` and the short
privacy notice in the footer.

After a structural change like the `/cet/` relocation, resubmit
`https://shaikidris.github.io/sitemap.xml` in Google Search Console and Bing
Webmaster Tools. The `citation_*` tags and `ScholarlyArticle` JSON-LD on each
landing page are what Google Scholar needs to index them as citable documents;
re-crawling after a URL move can take several weeks.

**Do not push or deploy without separate explicit authorization.**

# Site: Quantitative Collatz Descent

Static site presenting public article version 2.0.2 (DOI
[10.5281/zenodo.21851173](https://doi.org/10.5281/zenodo.21851173)) as a
readable, SEO-indexable article, with a cross-reference to the public CET
v2.0.1 Lean artifact (software DOI
[10.5281/zenodo.21797535](https://doi.org/10.5281/zenodo.21797535)). No
framework is required at runtime: the output is plain HTML, CSS, and vanilla
JavaScript, designed for `https://shaikidris.github.io/`.

## Layout

```
index.html              theorem, fundamentals/literature, proof/parameter labs, 4 figures
paper/index.html        full manuscript rendered to HTML (generated, see below)
paper/collatz-endpoint-transport.pdf   exact public Zenodo v2.0.2 PDF
code/index.html         theorem -> Lean declaration cross-reference table
assets/site.css         shared design system (light/dark aware)
assets/paper.css        paper-page-only layout (sticky TOC, reading measure)
assets/figures.js       figure engine plus browser-local study interactions
assets/figure-data.json generated numeric data for all 4 figures (see below)
assets/mathjax/         vendored MathJax 3.2.2 bundle, WOFF fonts, and license
assets/og-card.png      generated social-preview image
assets/favicon.svg
scripts/                generators; see below
robots.txt, sitemap.xml, .nojekyll
```

## Regenerating things

No preset numerical evidence is hand-typed. Three scripts regenerate the
non-prose content:

```sh
python3 scripts/make_figure_data.py   # iterates the real shortcut Collatz map;
                                       # writes assets/figure-data.json
python3 scripts/make_og_card.py       # rebuilds assets/og-card.png from the
                                       # same data (needs Pillow)
python3 scripts/build_paper.py        # re-renders paper/index.html from the
                                       # canonical manuscript via pandoc
```

`build_paper.py` reads
`~/research/collatz/CET-Sigma/rewrite/collatz_endpoint_transport_main.md`,
the source corresponding to the streamlined public v2.0.2 article. The
bundled PDF must separately match the current file served by Zenodo record
`21851173`. Re-run the script after a public article update, then diff
`paper/index.html` and verify the Zenodo PDF checksum before publishing.

Requires `pandoc` (`brew install pandoc`) and Python 3 with Pillow
(`pip install pillow`) for the OG card.

The theorem lab reads the public endpoint and witness clock from the generated
JSON. Its scale calculator evaluates the displayed closed forms in the
browser. The custom-orbit control iterates the shortcut map locally for
integers up to 10^12; those user-selected runs are finite illustrations and
are never stored or treated as evidence for the density theorem.

## Content boundary

The landing-page prose, proof outline, theorem ranges, and formalization scope
are synchronized to the two public records above. `CONTENT-PROMPT.md` now
records that source boundary and the update gate. The numbered `CONTENT SLOT`
comments remain only as stable editorial anchors; they are no longer
placeholders.

Do not source this site from unpublished or internal Collatz drafts. In
particular, a stronger later theorem, different proof architecture, or
different theorem numbering must not be blended into this public article
page.

## Preview locally

```sh
cd ~/research/collatz/site
python3 -m http.server 4823
# open http://localhost:4823/
```

## Deploying to shaikidris.github.io

This directory is not yet a git repository or pushed anywhere. To go live:

1. Create the repo `shaikidris/shaikidris.github.io` on the personal
   `shaikidris` GitHub account (**not** `shaiki_Zeta` — see
   `~/research/collatz/AGENTS.md`). It must be public for Pages to serve it
   for free, and the repo name must match exactly for GitHub's user-site
   convention.
2. From this directory:
   ```sh
   git init
   git add .
   git commit -m "Initial site: paper, figures, Lean theorem map"
   git branch -M main
   git remote add origin https://github.com/shaikidris/shaikidris.github.io.git
   git push -u origin main
   ```
3. In the repo's Settings → Pages, set the source to the `main` branch, root
   folder. GitHub serves it at `https://shaikidris.github.io/` within a few
   minutes; `.nojekyll` is already present so nothing gets mangled by the
   default Jekyll pass.
4. After it's live, submit `https://shaikidris.github.io/sitemap.xml` in
   Google Search Console and Bing Webmaster Tools so the scholarly `<meta
   name="citation_*">` tags and `ScholarlyArticle` JSON-LD get crawled and
   indexed (Google Scholar in particular needs the `citation_*` tags to pick
   it up as a citable document, which can take some weeks).

None of this has been done yet — no repo was created and nothing was pushed.

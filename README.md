# Site: shaikidris.github.io

Research directory and graduate-level paper explainers, built as plain HTML,
CSS and browser-local JavaScript at <https://shaikidris.github.io/>.

## Current reading routes

| | Polylogarithmic descent | Collatz endpoint transport |
|---|---|---|
| Overview | `/polylog/` | `/cet/` |
| Primary paper record | [Hexagon 2610.00299v1](https://hexagonmath.org/2610.00299v1) | [SSRN 7341398](https://doi.org/10.2139/ssrn.7341398) |
| Pinned manuscript | [Zenodo v4.0.2](https://doi.org/10.5281/zenodo.23132901) | [Zenodo v2.2.0](https://doi.org/10.5281/zenodo.22544006) |
| Full HTML paper | `/polylog/paper/` | `/cet/paper/` |
| Current PDF | `/paper/collatz-first-passage.pdf` | `/cet/paper/collatz-endpoint-transport.pdf` |
| Lean declaration map | `/code/` | `/cet/code/` |
| Palomar record | [v4 · four declarations](https://palomar-registry.org/entry?id=PALOMAR-2026-08-26-000005&version=4) | [v3 · one operator declaration](https://palomar-registry.org/entry?id=PALOMAR-2026-08-27-000018&version=3) |
| Earlier interactive edition | `/archive/polylog-v3.2.4/` | `/archive/cet-v2.0.3/` |

Manuscript, repository-release, Hexagon and registry versions are independent.
The current PDFs are exact copies of the named Zenodo files. The full-text
pages render their published Markdown without revising the manuscript wording.
CET's published text predates its v3 registration; the overview and code map
link the registered record and state its selected operator scope.

## Sources and builds

`data/works.json` owns publication identifiers, version labels, PDF paths,
registered source pins and public-source checksums. `content/` contains the
graduate explanations and shared orbit primer. `data/papers/` contains only
the already-published Markdown downloaded from the recorded `source_url`.
For CET, `source_member` identifies the Markdown inside the public source ZIP.

`scripts/build_paper.py` generates both overviews, full-text editions and Lean
maps. It checks manuscript/PDF SHA-256 hashes, source titles and version
agreement before rendering. It reads no private manuscript checkout.

```sh
python3 scripts/build_paper.py         # requires Pandoc on PATH
python3 scripts/build_home.py          # homepage and sitemap
python3 scripts/build_paper.py --check
python3 scripts/build_sitemap.py --check
python3 -m unittest discover -s scripts -p test_seo.py -v
node scripts/test_collatz_primer.js
```

Use `--pandoc /path/to/pandoc` when Pandoc is installed outside PATH.
No Python package is required by the site generators.

Before updating a reading edition, download its published source and PDF,
verify the deposit checksums, update the records and local SHA-256 values,
and revise the explainer to match the actual theorem and selected declarations.
Run the builds in the order above. A version-label change alone is insufficient.

The historical interactive editions retain their own PDFs and Lean maps.
Their HTML has `noindex, follow` and separate canonical URLs; these editions
are excluded from the sitemap. The older figure generators and data files
remain for those archived pages. The current routes retain the exact standard
and shortcut orbit primer, whose finite computations are illustrative.

## Research directory

`scripts/build_home.py` generates `index.html` from `data/works.json` as
crawlable HTML. Each work may name a single `palomar` record or a list of
`palomar_entries`; declaration totals count registry listings, not unique
mathematical results. A DOI or a public URL can identify a preprint.

An optional `hexagon` record makes Hexagon the primary reading link while
keeping the independently versioned Zenodo archive. `primary` can explicitly
select another public record, as with CET's SSRN link. `source_url` pins the
registered Lean source rather than relying on a moving default branch.

```sh
python3 scripts/build_home.py --check  # read-only Zenodo/Palomar drift check
```

This check reports missing or changed publication and registry records; it
does not prove manuscript-to-formalization correspondence. Refresh the selected
declarations and inspect their exact registered source when updating claims.

`assets/site.css` supplies the shared design system. `assets/reading.css`
styles current reading pages; `assets/home.css` styles the research directory.
MathJax is vendored under `assets/mathjax/`. [SEO.md](SEO.md) documents the
sitemap, ownership verification and static-hosting limits.

## Content boundary

Every pushed page must be synchronized to a **published** record — a Zenodo DOI and a
public tag. No unpublished or internal draft is a source for this site. Use the published sources and update checks described above; `CONTENT-PROMPT.md` is the historical design brief for the archived interactive editions.

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

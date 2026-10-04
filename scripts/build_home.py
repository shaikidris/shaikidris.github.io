#!/usr/bin/env python3
"""Build the research hub at index.html from data/works.json.

    python3 scripts/build_home.py           # write index.html
    python3 scripts/build_home.py --check   # compare works.json with live Zenodo/Palomar

The page is static HTML: the research table is in the markup itself, so search
engines index it without running JavaScript. The only script on the page
filters rows by area and toggles the theme; without it, every row is shown.
"""

from __future__ import annotations

import html
import json
import sys
import urllib.parse
import subprocess
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DATA = SITE / "data" / "works.json"
OUT = SITE / "index.html"
BASE = "https://shaikidris.github.io/"
REV = "20261004-hub3"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def doi_url(doi: str) -> str:
    return "https://doi.org/" + doi


def palomar_url(p: dict) -> str:
    return f"https://palomar-registry.org/entry?id={p['id']}&version={p['version']}"


def repo_url(name: str, owner: str) -> str:
    return f"https://github.com/{owner}/{name}"


# --------------------------------------------------------------------------- rows

def row(w: dict, owner: str) -> str:
    pre = w.get("preprint")
    pal = w["palomar"]
    title = esc(w["title"])
    title_html = (f'<a href="{doi_url(pre["doi"])}" rel="noopener" '
                  f'data-goatcounter-click="hub-title-{w["id"]}">{title}</a>') if pre else title
    msc = "".join(f'<span class="chip">{esc(m)}</span>' for m in w.get("msc", []))

    if pre:
        extra = "".join(
            f' · <a href="{esc(a["url"])}" rel="noopener">{esc(a["label"])}</a>'
            for a in w.get("also", []))
        preprint = (f'<span class="ver">v{esc(pre["version"])}</span>'
                    f'<span class="date">{esc(pre["date"])}</span>'
                    f'<a class="doi" href="{doi_url(pre["doi"])}" rel="noopener" '
                    f'data-goatcounter-click="hub-doi-{w["id"]}">{esc(pre["doi"])}</a>'
                    f'<span class="sub">{esc(pre.get("platform", "Zenodo"))} · CC BY 4.0{extra}</span>')
    else:
        preprint = '<span class="none">Not yet released</span>'

    repos = " · ".join(f'<a href="{repo_url(r, owner)}" rel="noopener">{esc(r)}</a>'
                       for r in w.get("repos", []))
    sw = w.get("software")
    sw_html = (f'<span class="sub">Lean archive <a href="{doi_url(sw["doi"])}" rel="noopener">'
               f'{esc(sw["doi"].split("zenodo.")[-1])}</a></span>') if sw else ""
    decl = pal["declarations"]
    formal = (f'<a class="palomar" href="{palomar_url(pal)}" rel="noopener" '
              f'data-goatcounter-click="hub-palomar-{w["id"]}">'
              f'<span class="pid">{esc(pal["id"].replace("PALOMAR-", ""))}</span>'
              f'<span class="pv">v{pal["version"]}</span></a>'
              f'<span class="trust">{esc(pal["trust"])} trust · {decl} declaration{"s" if decl != 1 else ""}</span>'
              f'<span class="sub repos">{repos}</span>{sw_html}')

    ex = w.get("explainer")
    if ex:
        stale = pre and ex.get("covers") and ex["covers"] != pre["version"]
        note = (f'<span class="sub">written for v{esc(ex["covers"])}</span>' if stale else "")
        lean = (f'<a class="sub" href="{esc(w["lean_map"])}">Theorem → Lean map</a>'
                if w.get("lean_map") else "")
        explore = (f'<a class="btn btn-sm" href="{esc(ex["url"])}" '
                   f'data-goatcounter-click="hub-explainer-{w["id"]}">{esc(ex["label"])}</a>'
                   f'{note}{lean}')
    else:
        explore = '<span class="none">—</span>'

    return f"""
      <tr data-area="{esc(w['area'])}">
        <td data-label="Result" class="c-result">
          <span class="wtitle">{title_html}</span>
          <span class="summary">{esc(w['summary'])}</span>
          <span class="chips">{msc}</span>
        </td>
        <td data-label="Preprint" class="c-pre">{preprint}</td>
        <td data-label="Formal verification" class="c-formal">{formal}</td>
        <td data-label="Explore" class="c-explore">{explore}</td>
      </tr>"""


def table(d: dict) -> str:
    owner = d["author"]["github"]
    groups = []
    for a in d["areas"]:
        ws = [w for w in d["works"] if w["area"] == a["id"]]
        if not ws:
            continue
        body = "".join(row(w, owner) for w in ws)
        groups.append(f"""
    <tbody data-area="{esc(a['id'])}">
      <tr class="group"><th colspan="4" scope="rowgroup">
        <span class="gname">{esc(a['name'])}</span>
        <span class="gblurb">{esc(a['blurb'])}</span>
      </th></tr>{body}
    </tbody>""")
    return f"""
  <div class="worktable-wrap">
  <table class="worktable">
    <caption class="sr-only">Preprints, Lean formalizations, Palomar registry entries and explainers</caption>
    <thead><tr>
      <th scope="col">Result</th><th scope="col">Preprint</th>
      <th scope="col">Formal verification</th><th scope="col">Explore</th>
    </tr></thead>{''.join(groups)}
  </table>
  </div>"""


def explainer_cards(d: dict) -> str:
    cards = []
    for w in d["works"]:
        ex = w.get("explainer")
        if not ex:
            continue
        pre = w.get("preprint", {})
        cards.append(f"""
      <a class="tile excard" href="{esc(ex['url'])}" data-goatcounter-click="hub-card-{w['id']}">
        <span class="eyebrow-sm">{esc(next(a['name'] for a in d['areas'] if a['id'] == w['area']))}</span>
        <b>{esc(w['title'])}</b>
        <span>{esc(ex['features'][0].upper() + ex['features'][1:])}.</span>
        <span class="covers">Written for v{esc(ex['covers'])} · current record v{esc(pre.get('version', '—'))}</span>
      </a>""")
    return "".join(cards)


def jsonld(d: dict) -> str:
    a = d["author"]
    person = {"@type": "Person", "name": a["name"],
              "identifier": f"https://orcid.org/{a['orcid']}",
              "sameAs": [f"https://orcid.org/{a['orcid']}", f"https://github.com/{a['github']}"]}
    parts = []
    for i, w in enumerate(d["works"], 1):
        item = {"@type": "ScholarlyArticle", "name": w["title"], "abstract": w["summary"],
                "author": {"@type": "Person", "name": a["name"]}}
        if w.get("preprint"):
            p = w["preprint"]
            item.update({"identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": p["doi"]},
                         "url": doi_url(p["doi"]), "datePublished": p["date"], "version": p["version"],
                         "license": "https://creativecommons.org/licenses/by/4.0/"})
        else:
            item["url"] = palomar_url(w["palomar"])
        parts.append({"@type": "ListItem", "position": i, "item": item})
    doc = {"@context": "https://schema.org", "@type": "ProfilePage", "url": BASE,
           "name": f"{a['name']} — Mathematics research",
           "mainEntity": person,
           "hasPart": {"@type": "ItemList", "name": "Research preprints and formalizations",
                       "itemListElement": parts}}
    return json.dumps(doc, ensure_ascii=False, indent=1)


# --------------------------------------------------------------------------- page

def page(d: dict) -> str:
    a = d["author"]
    works = d["works"]
    n_pre = sum(1 for w in works if w.get("preprint"))
    n_pal = len(works)
    n_decl = sum(w["palomar"]["declarations"] for w in works)
    n_ex = sum(1 for w in works if w.get("explainer"))
    filters = "".join(
        f'<button type="button" class="chip-btn" data-filter="{esc(x["id"])}" aria-pressed="false">{esc(x["name"])}</button>'
        for x in d["areas"])
    desc = (f"{a['name']}: {n_pre} open preprints in quantitative number theory and graph theory — "
            f"Collatz dynamics in natural density, Gallai path decompositions, and arithmetic graph spectra — "
            f"with selected results formalized in Lean 4 and registered on Palomar.")
    orcid = f"https://orcid.org/{a['orcid']}"
    zenodo = ("https://zenodo.org/search?q=" +
              urllib.parse.quote(f'metadata.creators.person_or_org.identifiers.identifier:"{a["orcid"]}"'))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Generated by scripts/build_home.py from data/works.json. Edit those, not this file. -->
<title>{esc(a['name'])} — Mathematics research, preprints and Lean formalizations</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}">
<meta name="author" content="{esc(a['name'])}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">

<meta property="og:type" content="profile">
<meta property="og:site_name" content="{esc(a['name'])} — Mathematics">
<meta property="og:title" content="{esc(a['name'])} — Mathematics research">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{BASE}">
<meta property="og:image" content="{BASE}assets/og-home.png?v={REV}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(a['name'])} — Mathematics research">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{BASE}assets/og-home.png?v={REV}">

<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css?v={REV}">
<link rel="stylesheet" href="/assets/home.css?v={REV}">

<script type="application/ld+json">
{jsonld(d)}
</script>
<script>
  (function () {{
    try {{ var t = localStorage.getItem("theme");
      if (t) document.documentElement.setAttribute("data-theme", t); }} catch (e) {{}}
    document.documentElement.classList.add("js");
  }})();
</script>
<script data-goatcounter="https://shaikidris.goatcounter.com/count"
        async src="https://gc.zgo.at/count.js"></script>
</head>

<body class="hub">
<a class="skip" href="#main">Skip to content</a>

<header class="masthead">
  <div class="wrap">
    <a class="brand" href="/">{esc(a['name'])}</a>
    <nav>
      <a href="#research">Research</a>
      <a href="#explainers" class="opt">Explainers</a>
      <a href="#verification" class="opt">Verification</a>
      <a href="{orcid}" rel="noopener me" class="opt">ORCID</a>
      <button class="theme-toggle" id="theme-toggle" type="button" aria-label="Toggle colour theme" title="Toggle colour theme">◐</button>
    </nav>
  </div>
</header>

<main id="main">

<section class="hero hub-hero">
  <div class="wrap">
    <p class="eyebrow">Mathematics · Formal verification</p>
    <h1>{esc(a['name'])}</h1>
    <p class="tagline">
      {esc(a['affiliation'])} working in quantitative number theory and combinatorics.
      Progress on the <strong>Collatz conjecture</strong> and proved cases of
      <strong>Gallai’s path-decomposition conjecture</strong>, alongside arithmetic graph spectra.
      Full Lean&nbsp;4 formalization projects submitted to <strong>Palomar</strong>;
      each registered entry specifies the declarations it verifies.
    </p>
    <div class="actions">
      <a class="btn btn-primary" href="#research">Browse the research</a>
      <a class="btn" href="{orcid}" rel="noopener me">ORCID</a>
      <a class="btn" href="https://github.com/{esc(a['github'])}" rel="noopener me">GitHub</a>
      <a class="btn" href="{zenodo}" rel="noopener">All records on Zenodo</a>
    </div>
    <dl class="stats">
      <div><dt>Open preprints</dt><dd>{n_pre}</dd></div>
      <div><dt>Palomar entries</dt><dd>{n_pal}</dd></div>
      <div><dt>Registered declarations</dt><dd>{n_decl}</dd></div>
      <div><dt>Interactive explainers</dt><dd>{n_ex}</dd></div>
    </dl>
  </div>
</section>

<section id="research" class="research">
  <div class="wrap">
    <div class="sechead">
      <div>
        <h2>Research</h2>
        <p class="lede">Each row links the preprint of record, its Lean formalization and
        Palomar entry, and — where one exists — a graduate-level explainer.</p>
      </div>
      <div class="filters" role="group" aria-label="Filter by area">
        <button type="button" class="chip-btn" data-filter="all" aria-pressed="true">All</button>{filters}
      </div>
    </div>
    {table(d)}
    <p class="tablenote">Versions and dates are those of the latest public record. Titles link to the
    paper DOI; Zenodo records also list earlier versions. SSRN dates identify the public revision.</p>
  </div>
</section>

<section id="explainers">
  <div class="wrap">
    <h2>Graduate explainers</h2>
    <p class="lede">Long-form companion pages for first-year graduate students: the theorem in context,
    the proof architecture step by step, and figures computed from the actual map. They are optional
    reading — the preprint is always the reference.</p>
    <div class="grid excards">{explainer_cards(d)}
    </div>
  </div>
</section>

<section id="verification">
  <div class="wrap narrow">
    <h2>What the formal verification certifies</h2>
    <p>
      Each Palomar entry records a Lean&nbsp;4 project at one pinned GitHub commit, the selected
      declarations that were machine-checked against it, and an archival fork that preserves the source.
      A <em>high</em> trust level means the registry's checks passed for those declarations.
    </p>
    <p>
      This is <strong>mechanical verification and preservation, not peer review</strong>. It certifies the
      listed declarations — not every specialization, remark or literature comparison in the manuscript.
      Each manuscript is written to be checked independently of its formalization.
    </p>
    <div class="note caution">
      <p><strong>Scope.</strong> The Collatz results are almost-all statements in natural density, or
      positive-density statements; none proves the Collatz conjecture or excludes exceptional cycles or
      divergent orbits. The path-decomposition results settle specific cases; Gallai's conjecture in
      general remains open.</p>
    </div>
    <p><a href="https://palomar-registry.org/about" rel="noopener">About the Palomar registry →</a></p>
  </div>
</section>

</main>

<footer>
  <div class="wrap">
    <p style="margin:0">
      © 2026 {esc(a['name'])} · Preprints under
      <a href="https://creativecommons.org/licenses/by/4.0/" rel="license noopener">CC BY 4.0</a>;
      Lean code under the licence of each repository ·
      <a href="{orcid}" rel="noopener me">ORCID</a> ·
      <a href="https://github.com/{esc(a['github'])}" rel="noopener me">GitHub</a>
    </p>
    <p style="margin:.45rem 0 0;font-size:.85rem">
      Privacy-friendly, cookieless page and interaction counts are collected
      with <a href="https://www.goatcounter.com/help/privacy" rel="noopener">GoatCounter</a>;
      no form values are sent.
    </p>
  </div>
</footer>

<script>
  (function () {{
    var btn = document.getElementById("theme-toggle");
    btn && btn.addEventListener("click", function () {{
      var root = document.documentElement, cur = root.getAttribute("data-theme");
      if (!cur) cur = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
      var next = cur === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try {{ localStorage.setItem("theme", next); }} catch (e) {{}}
    }});
    var chips = [].slice.call(document.querySelectorAll(".chip-btn"));
    var groups = [].slice.call(document.querySelectorAll(".worktable tbody[data-area]"));
    function apply(f) {{
      chips.forEach(function (c) {{ c.setAttribute("aria-pressed", String(c.dataset.filter === f)); }});
      groups.forEach(function (g) {{ g.hidden = !(f === "all" || g.dataset.area === f); }});
    }}
    chips.forEach(function (c) {{ c.addEventListener("click", function () {{ apply(c.dataset.filter); }}); }});
  }})();
</script>
</body>
</html>
"""


# --------------------------------------------------------------------------- check

def get(url: str):
    # curl uses the system trust store; python.org builds of Python ship without
    # one until "Install Certificates.command" is run.
    out = subprocess.run(["curl", "-fsSL", "--max-time", "30",
                          "-A", "shaikidris-site-check", url],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def check(d: dict) -> int:
    drift = 0
    orcid = d["author"]["orcid"]
    known_pre = {w["preprint"]["concept"] for w in d["works"] if w.get("preprint", {}).get("concept")}
    known_pal = {w["palomar"]["id"] for w in d["works"]}

    for w in d["works"]:
        pre = w.get("preprint")
        if pre and pre["doi"].startswith("10.5281/zenodo."):
            rid = pre["doi"].split("zenodo.")[-1]
            latest = get(f"https://zenodo.org/api/records/{rid}/versions/latest")
            v = str(latest["metadata"].get("version", "")).lstrip("vV")
            if v != pre["version"]:
                drift += 1
                print(f"[preprint] {w['id']}: works.json v{pre['version']} -> Zenodo v{v} ({latest['doi']})")
            ex = w.get("explainer")
            if ex and ex.get("covers") != v:
                print(f"[explainer] {w['id']}: {ex['url']} written for v{ex['covers']}, latest v{v} (banner should say so)")
        pal = w["palomar"]
        rec = get(f"https://data.palomar-registry.org/versions/{pal['id']}.json")
        top = max((x["version"] for x in rec["entries"] if x.get("status") == "registered"), default=0)
        if top and top != pal["version"]:
            drift += 1
            print(f"[palomar] {w['id']}: works.json v{pal['version']} -> registry v{top}")

    q = urllib.parse.urlencode({"q": f'creators.orcid:"{orcid}"', "size": 25})
    for r in get(f"https://zenodo.org/api/records?{q}")["hits"]["hits"]:
        if r["metadata"]["resource_type"].get("type") == "publication" and r.get("conceptdoi") not in known_pre:
            drift += 1
            print(f"[new preprint] {r['metadata']['title']} ({r['doi']}) is not in works.json")
    q = urllib.parse.urlencode({"q": d["author"]["name"], "trust": "all"})
    for e in get(f"https://data.palomar-registry.org/api/v1/results?{q}")["entries"]:
        if e["id"] not in known_pal and any(a.get("name") == d["author"]["name"] for a in e.get("authors", [])):
            drift += 1
            print(f"[new palomar] {e['id']} v{e['version']}: {e['title']} is not in works.json")

    print("no drift" if not drift else f"{drift} item(s) differ from the live records")
    return 1 if drift else 0


def main() -> None:
    d = json.loads(DATA.read_text(encoding="utf-8"))
    if "--check" in sys.argv:
        sys.exit(check(d))
    OUT.write_text("\n".join(line.rstrip() for line in page(d).splitlines()) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes, {len(d['works'])} works)")


if __name__ == "__main__":
    main()

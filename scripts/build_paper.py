#!/usr/bin/env python3
"""Render the public Zenodo v2.0.2 article source to cet/paper/index.html.

Source of truth:
  ~/research/collatz/CET-Sigma/rewrite/collatz_endpoint_transport_main.md

The manuscript is never edited here. This script only converts it and wraps it
in the site chrome, so re-running it after a manuscript change is safe.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
SRC = Path.home() / "research/collatz/CET-Sigma/rewrite/collatz_endpoint_transport_main.md"
OUT = SITE / "cet" / "paper" / "index.html"

TITLE = ("Quantitative Collatz Descent to Stretched-Logarithmic Scale in "
         "Natural Density, with a Lean 4 Formalization")
DESC = ("Full text of the public Zenodo v2.0.2 article: for every fixed "
        "0 < delta < delta_0 = 0.251245530155874..., the shortcut Collatz "
        "orbit minimum satisfies T_min(n) <= exp((log n)^(1-delta)) on a set "
        "of natural density one, with an explicit exceptional count and a "
        "6.953 log n witness.")
CANON = "https://shaikidris.github.io/cet/paper/"
DOI = "10.5281/zenodo.21851173"


def pandoc(md: str) -> str:
    """Markdown -> HTML fragment, leaving TeX delimiters intact for MathJax."""
    proc = subprocess.run(
        ["pandoc", "--from", "markdown+tex_math_dollars+tex_math_single_backslash"
                            "+pipe_tables+fenced_divs+raw_html+header_attributes",
         "--to", "html5", "--mathjax", "--no-highlight", "--section-divs"],
        input=md, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        sys.exit(f"pandoc failed:\n{proc.stderr}")
    return proc.stdout


def build_toc(body: str) -> str:
    """Build a two-level table of contents from h2/h3 with ids."""
    items = re.findall(r'<h([23])[^>]*id="([^"]+)"[^>]*>(.*?)</h[23]>', body, re.S)
    if not items:
        return ""
    out = ['<nav class="toc" aria-label="Table of contents"><h5>Contents</h5><ul>']
    for level, hid, text in items:
        text = re.sub(r"<[^>]+>", "", text).strip()
        text = re.sub(r"\\\((.*?)\\\)", r"\1", text)
        if len(text) > 78:
            text = text[:75] + "…"
        cls = "lvl3" if level == "3" else "lvl2"
        out.append(f'<li class="{cls}"><a href="#{hid}">{html.escape(text)}</a></li>')
    out.append("</ul></nav>")
    return "".join(out)


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — full text</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">

<meta name="citation_title" content="{title}">
<meta name="citation_author" content="Shaik, Idris Ali">
<meta name="citation_author_orcid" content="https://orcid.org/0009-0009-9699-9712">
<meta name="citation_publication_date" content="2026/08/08">
<meta name="citation_doi" content="{doi}">
<meta name="citation_abstract_html_url" content="https://shaikidris.github.io/cet/">
<meta name="citation_fulltext_html_url" content="{canon}">
<meta name="citation_pdf_url" content="https://shaikidris.github.io/cet/paper/collatz-endpoint-transport.pdf">
<meta name="citation_language" content="en">
<meta name="citation_keywords" content="Collatz conjecture; almost all Collatz orbits; shortcut Collatz map; ordinary natural density; stretched-logarithmic descent; fixed-total Rényi estimate; endpoint transport; endpoint fibers; parity vectors; quantitative exceptional-set bounds; logarithmic witnessing clock; Lean 4 formalization; Mathlib">

<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="https://shaikidris.github.io/assets/og-card.png">
<meta name="twitter:card" content="summary_large_image">

<meta name="author" content="Idris Ali Shaik">
<meta name="robots" content="index, follow, max-snippet:-1">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/paper.css">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ScholarlyArticle",
  "headline": "{title}",
  "author": {{ "@type": "Person", "name": "Idris Ali Shaik",
               "identifier": "https://orcid.org/0009-0009-9699-9712" }},
  "datePublished": "2026-08-08",
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "identifier": {{ "@type": "PropertyValue", "propertyID": "DOI", "value": "{doi}" }},
  "url": "{canon}",
  "keywords": "Collatz conjecture, almost all Collatz orbits, shortcut Collatz map, ordinary natural density, stretched-logarithmic descent, fixed-total Rényi estimate, endpoint transport, endpoint fibers, parity vectors, quantitative exceptional-set bounds, logarithmic witnessing clock, Lean 4 formalization, Mathlib",
  "isPartOf": {{ "@type": "WebSite", "name": "Quantitative Collatz Descent",
                 "url": "https://shaikidris.github.io/cet/" }}
}}
</script>

<script>
  (function () {{ var t = localStorage.getItem("theme");
    if (t) document.documentElement.setAttribute("data-theme", t); }})();
</script>
<script>
window.MathJax = {{
  tex: {{ inlineMath: [["\\\\(", "\\\\)"]], displayMath: [["\\\\[", "\\\\]"]],
          processEscapes: true, tags: "none" }},
  options: {{ skipHtmlTags: ["script","noscript","style","textarea","pre","code"] }},
  chtml: {{ scale: 0.97 }}
}};
</script>
<script defer src="/assets/mathjax/tex-chtml.js"></script>
<script data-goatcounter="https://shaikidris.goatcounter.com/count"
        async src="https://gc.zgo.at/count.js"></script>
</head>
<body class="paperpage">
<a class="skip" href="#doc">Skip to the paper</a>

<header class="masthead">
  <div class="wrap">
    <a class="brand" href="/cet/">Quantitative Collatz Descent</a>
    <nav>
      <a href="/cet/">Overview</a>
      <a href="./" aria-current="page">Paper</a>
      <a href="/cet/code/">Lean code</a>
      <button class="theme-toggle" id="theme-toggle" aria-label="Toggle colour theme">◐</button>
    </nav>
  </div>
</header>

<div class="paperbar">
  <div class="wrap">
    <span>Preprint · v2.0.2 · CC BY 4.0</span>
    <a href="collatz-endpoint-transport.pdf" data-goatcounter-click="cet-paper-download-pdf">Download PDF</a>
    <a href="https://doi.org/{doi}" rel="noopener" data-goatcounter-click="cet-paper-preprint-doi">doi:{doi}</a>
  </div>
</div>

<div class="paperlayout wrap">
{toc}
  <article id="doc" class="doc">
    {body}
  </article>
</div>

<footer>
  <div class="wrap">
    <p style="margin:0">
      © 2026 Idris Ali Shaik · licensed
      <a href="https://creativecommons.org/licenses/by/4.0/" rel="license noopener">CC BY 4.0</a> ·
      <a href="/cet/">site overview</a> ·
      <a href="/cet/code/">theorem → Lean map</a>
      <br>An almost-all result in natural density; not a proof of the Collatz conjecture.
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
      localStorage.setItem("theme", next);
    }});
    // highlight the section currently in view
    var links = [].slice.call(document.querySelectorAll(".toc a"));
    var map = {{}};
    links.forEach(function (a) {{
      var el = document.getElementById(a.getAttribute("href").slice(1));
      if (el) map[a.getAttribute("href").slice(1)] = a;
    }});
    if ("IntersectionObserver" in window) {{
      var io = new IntersectionObserver(function (es) {{
        es.forEach(function (e) {{
          var a = map[e.target.id];
          if (a && e.isIntersecting) {{
            links.forEach(function (l) {{ l.classList.remove("active"); }});
            a.classList.add("active");
            a.scrollIntoView({{ block: "nearest" }});
          }}
        }});
      }}, {{ rootMargin: "0px 0px -80% 0px" }});
      Object.keys(map).forEach(function (id) {{
        var el = document.getElementById(id);
        if (el) io.observe(el);
      }});
    }}
  }})();
</script>
</body>
</html>
"""


def main() -> None:
    if not SRC.exists():
        sys.exit(f"manuscript not found: {SRC}")
    md = SRC.read_text()

    # Drop the H1 and the front-matter block; the site chrome supplies them.
    md = re.sub(r"\A#\s+.*?\n", "", md, count=1)

    body = pandoc(md)
    toc = build_toc(body)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(TEMPLATE.format(
        title=html.escape(TITLE), desc=html.escape(DESC),
        canon=CANON, doi=DOI, body=body, toc=toc))

    n_sections = len(re.findall(r"<h2", body))
    print(f"wrote {OUT}  ({OUT.stat().st_size:,} bytes, {n_sections} sections)")


if __name__ == "__main__":
    main()

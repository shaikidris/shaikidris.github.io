# Search indexing for the research site

The site publishes static HTML through GitHub Pages at
<https://shaikidris.github.io/>. `.nojekyll` disables Jekyll processing. Each
reading page is a real `index.html` file with its own canonical URL; research
table content is present without JavaScript.

## Generated metadata and sitemap

The homepage generator provides title, description, canonical, Open Graph,
social-image descriptions and ProfilePage JSON-LD. Its Person entity connects
the author's ORCID, GitHub and LinkedIn profiles, and paper authors reference
that identity. Article URLs and versions retain their independent publication
identities; the hub is not a journal-acceptance claim.

`python3 scripts/build_home.py` regenerates the homepage and sitemap together.
The sitemap generator reads canonical metadata from public index pages and
adds their same-origin citation PDFs. It fails if a canonical names the wrong
local page or a cited local PDF is missing. It excludes `noindex` pages and
deduplicates URLs. It omits modification dates rather than inferring them from
a rebuild or restored filesystem timestamp.

```sh
python3 -B scripts/build_home.py
python3 -B scripts/build_sitemap.py --check
python3 -B -m unittest discover -s scripts -p test_seo.py -v
```

`robots.txt` permits crawling and advertises
<https://shaikidris.github.io/sitemap.xml>. A sitemap aids discovery; it does
not guarantee indexing or rankings.

## Search Console ownership verification

1. Add the URL-prefix property `https://shaikidris.github.io/` in Google Search
   Console and choose HTML file verification.
2. Download the actual Google-issued HTML file. Place it unchanged at the
   publishing root, using the supplied filename and contents. Do not invent a
   token, replace another owner's token, or commit a sample verification file.
3. Commit and deploy that file, confirm its exact public URL returns it, and
   finish verification in Search Console. Keep the file after verification.
4. Submit `sitemap.xml` and use URL Inspection to inspect the homepage and the
   main reading pages.

The generators overwrite only their named outputs; root-level verification
files remain untouched. Jekyll plugins and `keep_files` are not involved in this
publishing setup. Account verification cannot be completed without the actual
file and the owner's Search Console access.

## URL changes and hosting

No SPA routing fallback is required. A JavaScript router in `404.html` would
not turn a server's 404 into a successful indexable page.

For a real future page move, retain an HTML page at the old location with a
canonical link, an immediate meta refresh and a visible destination link.
Google recognizes an immediate refresh as a permanent redirect signal; this
does not create an HTTP 301 response. Do not redirect the research homepage
to one paper, since the homepage has its own portfolio purpose.

A custom domain requires a separately chosen domain and verified DNS/Pages
settings. No `CNAME` or DNS changes are part of the default GitHub-hosted site.

References: [Google ownership verification](https://support.google.com/webmasters/answer/9008080),
[Google redirect handling](https://developers.google.com/search/docs/crawling-indexing/301-redirects),
[GitHub Pages build options](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll).

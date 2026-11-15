#!/usr/bin/env python3
"""Generate the static site's sitemap from canonical index pages and citation PDFs.

Run directly to rebuild, or pass --check to validate the committed sitemap.
No dependency on Jekyll, JavaScript rendering, file mtimes or network access.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

SITE = Path(__file__).resolve().parent.parent
BASE = 'https://shaikidris.github.io/'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'

class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.pdfs = []
        self.noindex = False

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == 'link' and 'canonical' in data.get('rel', '').lower().split():
            self.canonicals.append(data.get('href', ''))
        if tag == 'meta':
            name = data.get('name', '').lower()
            content = data.get('content', '')
            if name in ('robots', 'googlebot') and 'noindex' in content.lower():
                self.noindex = True
            if name == 'citation_pdf_url':
                self.pdfs.append(content)

def local_file(site: Path, base: str, url: str) -> Path:
    parsed, origin = urlsplit(url), urlsplit(base)
    if (parsed.scheme, parsed.netloc) != (origin.scheme, origin.netloc) or parsed.query or parsed.fragment:
        raise ValueError('Sitemap URL must be canonical and same-origin: ' + url)
    path = (site / unquote(parsed.path).lstrip('/')).resolve()
    if not path.is_relative_to(site.resolve()):
        raise ValueError('URL escapes publishing directory: ' + url)
    if parsed.path.endswith('/'):
        path /= 'index.html'
    if not path.is_file():
        raise ValueError('Missing public file: ' + url)
    return path

def render(site: Path = SITE, base: str = BASE) -> str:
    urls = set()
    for page in sorted(site.rglob('index.html')):
        parts = page.relative_to(site).parts
        if any(p.startswith('.') or p in ('assets', 'scripts', 'node_modules', 'vendor') for p in parts):
            continue
        meta = Metadata()
        meta.feed(page.read_text(encoding='utf-8'))
        if meta.noindex:
            continue
        if len(meta.canonicals) != 1:
            raise ValueError(f'{page}: expected exactly one canonical URL')
        canonical = meta.canonicals[0]
        if local_file(site, base, canonical) != page.resolve():
            raise ValueError(f'{page}: canonical URL names another local page')
        urls.add(canonical)
        for pdf in meta.pdfs:
            if urlsplit(pdf).netloc == urlsplit(base).netloc:
                local_file(site, base, pdf)
                urls.add(pdf)
    if base not in urls:
        raise ValueError('The canonical homepage is missing')
    ET.register_namespace('', NS)
    tree = ET.Element('{' + NS + '}urlset')
    for url in sorted(urls):
        node = ET.SubElement(tree, '{' + NS + '}url')
        ET.SubElement(node, '{' + NS + '}loc').text = url
    ET.indent(tree, space='  ')
    # Omit lastmod rather than asserting a page changed whenever a build runs.
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(tree, encoding='unicode') + '\n'

def write_sitemap(site: Path = SITE, base: str = BASE):
    text = render(site, base)
    (site / 'sitemap.xml').write_text(text, encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    text = render()
    if args.check:
        if (SITE / 'sitemap.xml').read_text(encoding='utf-8') != text:
            parser.exit(1, 'sitemap.xml is stale; run python3 scripts/build_sitemap.py\n')
        print('Sitemap matches canonical pages and local citation PDFs.')
    else:
        write_sitemap()
        print('Regenerated sitemap.xml.')

if __name__ == '__main__':
    main()

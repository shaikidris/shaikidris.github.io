"""Static SEO regression checks; no network, publication or account actions."""
import json
from pathlib import Path
import tempfile
import unittest

from build_home import DATA, jsonld
from build_sitemap import BASE, SITE, render

class SEOTests(unittest.TestCase):
    def test_author_profiles_and_article_identity(self):
        doc = json.loads(jsonld(json.loads(DATA.read_text())))
        author = doc['mainEntity']
        self.assertEqual(author['url'], BASE)
        self.assertIn('https://www.linkedin.com/in/shaikidris/', author['sameAs'])
        for entry in doc['hasPart']['itemListElement']:
            item = entry['item']
            self.assertEqual(item['author']['@id'], author['@id'])
            self.assertNotIn(item['url'], item.get('sameAs', []))

    def test_committed_sitemap_matches_public_pages(self):
        self.assertEqual((SITE / 'sitemap.xml').read_text(), render())

    def test_generator_rejects_missing_pdf_and_keeps_verification_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / 'index.html'
            page.write_text(f'<link rel="canonical" href="{BASE}"><meta name="citation_pdf_url" content="{BASE}paper.pdf">')
            verification = root / 'google-fixture.html'
            verification.write_text('fixture token; not a real verification credential')
            with self.assertRaisesRegex(ValueError, 'Missing public file'):
                render(root)
            (root / 'paper.pdf').touch()
            sitemap = render(root)
            self.assertIn(BASE + 'paper.pdf', sitemap)
            self.assertNotIn('google-fixture', sitemap)
            self.assertEqual(verification.read_text(), 'fixture token; not a real verification credential')

    def test_noindex_pages_are_not_listed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'index.html').write_text(f'<link rel="canonical" href="{BASE}">')
            (root / 'hidden').mkdir()
            (root / 'hidden/index.html').write_text('<meta name="robots" content="noindex, follow">')
            self.assertNotIn('/hidden/', render(root))

if __name__ == '__main__':
    unittest.main()

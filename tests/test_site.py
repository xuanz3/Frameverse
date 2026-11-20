"""Static checks requiring only the Python standard library (runs in GitHub Actions)."""
import re
import unittest
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote

ROOT=Path(__file__).resolve().parents[1]

class SiteLinksParser(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.titles=[];self.images=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('a','link','script','img'):
            field='href' if tag in ('a','link') else 'src'
            if a.get(field):self.links.append(a[field])
        if tag=='img':self.images.append(a)
        if a.get('id'):self.ids.append(a['id'])

class SiteQualityTests(unittest.TestCase):
    def test_all_local_links_exist(self):
        for doc in ROOT.glob('*.html'):
            with self.subTest(page=doc.name):
                parser=SiteLinksParser();parser.feed(doc.read_text(encoding='utf-8'))
                for target in parser.links:
                    parsed=urlparse(target)
                    if parsed.scheme or parsed.netloc or target.startswith(('#','mailto:','tel:')):continue
                    path=unquote(parsed.path)
                    if path.startswith('/'): resolved=ROOT/path.lstrip('/')
                    else:resolved=doc.parent/path
                    self.assertTrue(resolved.exists(),f'{doc.name} -> missing {target}')
                self.assertEqual(len(parser.ids),len(set(parser.ids)),f'Duplicate IDs: {doc.name}')
                for image in parser.images:
                    self.assertTrue(image.get('alt') is not None,f'Missing alt in {doc.name}')
    def test_page_semantics(self):
        for doc in ROOT.glob('*.html'):
            html=doc.read_text(encoding='utf-8')
            with self.subTest(page=doc.name):
                self.assertIn('<main id="main">',html)
                self.assertIn('<nav class="nav-desktop"',html)
                self.assertIn('name="description"',html)
                self.assertIn('href="privacy.html"',html)
                self.assertIn('<h1',html)
    def test_content_size(self):
        self.assertGreaterEqual(len(list(ROOT.glob('figure-*.html'))),8)
        self.assertGreaterEqual(len(list(ROOT.glob('article-*.html'))),6)
        self.assertGreaterEqual(len(list(ROOT.glob('*.html'))),20)
    def test_no_fake_store_claims(self):
        for name in ('collections.html','figure-nocturne.html','figure-sentinel.html'):
            s=(ROOT/name).read_text()
            self.assertIn('not for sale',s.lower())
    def test_search_index(self):
        import json
        data=json.loads((ROOT/'assets/search-index.json').read_text())
        self.assertGreaterEqual(len(data),18)
        self.assertTrue(all((ROOT/x['href']).exists() for x in data if not x.get('external')))
if __name__=='__main__':unittest.main()

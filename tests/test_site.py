"""FRAMEVERSE V2: dependency-free static site checks for GitHub Actions."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import json,re,unittest
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/archive.json').read_text(encoding='utf-8'))

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.images=[];self.ids=[];self.headings=[];self.buttons=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('a','link','script','img'):
            value=a.get('href' if tag in ('a','link') else 'src')
            if value:self.links.append(value)
        if tag=='img':self.images.append(a)
        if tag=='button':self.buttons.append(a)
        if tag=='h1':self.headings.append(tag)
        if 'id' in a:self.ids.append(a['id'])

class SiteQuality(unittest.TestCase):
    def test_all_pages_have_semantic_nav_and_h1(self):
        for doc in ROOT.glob('*.html'):
            with self.subTest(doc=doc.name):
                text=doc.read_text(encoding='utf-8')
                parser=SiteParser();parser.feed(text)
                self.assertEqual(len(parser.ids),len(set(parser.ids)),f'Duplicate IDs: {doc.name}')
                self.assertEqual(len(parser.headings),1,f'Expected one h1 in {doc.name}')
                self.assertIn('<main id="main">',text)
                self.assertIn('<nav class="desktop-nav"',text)
                self.assertIn('name="description"',text)
                self.assertIn('Zenless Zone Zero',text)
                self.assertIn('Not affiliated with HoYoverse',text)
                self.assertTrue(all('alt' in img for img in parser.images))
                self.assertTrue(all('type' in b for b in parser.buttons),f'button lacking explicit type: {doc.name}')
    def test_markup_balanced_for_structural_tags(self):
        # Structural HTML balance catches browser auto-repair that can silently break CSS grids.
        tags = ('div','section','main','header','footer','nav','a','button','h1','h2','h3','em','i','strong','p')
        for doc in ROOT.glob('*.html'):
            raw = doc.read_text(encoding='utf-8')
            for tag in tags:
                opens=len(re.findall(fr'<{tag}(?=[\s>])',raw))
                closes=len(re.findall(fr'</{tag}>',raw))
                with self.subTest(page=doc.name,tag=tag):
                    self.assertEqual(opens,closes,f'Unbalanced <{tag}> in {doc.name}')
    def test_no_broken_local_links(self):
        for doc in ROOT.glob('*.html'):
            parser=SiteParser();parser.feed(doc.read_text(encoding='utf-8'))
            for target in parser.links:
                parsed=urlparse(target)
                if parsed.scheme or parsed.netloc or target.startswith(('#','mailto:','tel:')):continue
                path=unquote(parsed.path)
                resolved=ROOT/path.lstrip('/') if path.startswith('/') else doc.parent/path
                with self.subTest(page=doc.name,target=target):self.assertTrue(resolved.exists())
    def test_images_and_data_exist(self):
        for category,items in DATA.items():
            for item in items:
                self.assertTrue((ROOT/item['image']).is_file(),f'{category}: {item["image"]}')
        self.assertGreaterEqual(len(list((ROOT/'media').glob('*.webp'))),90)
    def test_site_has_curated_coverage(self):
        expected={'wallpapers':6,'cg':9,'scenes':24,'bangboo':22,'agents':12,'ui':26}
        self.assertEqual({k:len(v) for k,v in DATA.items()},expected)
        for route in ['index.html','agents.html','scenes.html','bangboo.html','cg.html','ui.html','wallpapers.html','journal.html','about.html']:
            self.assertTrue((ROOT/route).is_file())
        self.assertEqual(len(list(ROOT.glob('agent-agent-*.html'))),12)
        self.assertEqual(len(list(ROOT.glob('*.html'))),21)
    def test_search_index_integrity(self):
        idx=json.loads((ROOT/'data/search.json').read_text(encoding='utf-8'))
        self.assertGreaterEqual(len(idx),95)
        for item in idx:
            self.assertTrue((ROOT/item['url']).is_file(),f"Missing search target: {item['url']}")
            self.assertTrue((ROOT/item['image']).is_file())
    def test_no_legacy_shop_or_event_claims(self):
        for doc in ROOT.glob('*.html'):
            body=doc.read_text(encoding='utf-8').lower()
            self.assertNotIn('not for sale',body)
            self.assertNotIn('add to cart',body)
            self.assertNotIn('oz comic-con melbourne',body)
        self.assertFalse((ROOT/'collections.html').exists())
        self.assertFalse((ROOT/'events.html').exists())
    def test_accessible_controls(self):
        script=(ROOT/'assets/site.js').read_text(encoding='utf-8')
        for term in ['data-lightbox','Escape','aria-hidden','aria-pressed','search.json','prefers-reduced-motion']:
            self.assertIn(term,script)
        css=(ROOT/'assets/site.css').read_text(encoding='utf-8')
        self.assertIn('@media(prefers-reduced-motion:reduce)',css)
if __name__=='__main__':unittest.main()

from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import unittest,re
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.h1=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  for key in ('href','src'):
   if key in a:self.links.append(a[key])
class SiteChecks(unittest.TestCase):
 def test_pages_are_reachable(self):
  for page in ['about','services','individual','marathons','menu','consultation','analyses','reviews','nutrition','diary','articles','food','faq','contacts','events','club','retreats','documents','checkout']:
   self.assertTrue((ROOT/f'{page}.html').exists(),page)
 def test_links_and_images_resolve(self):
  for path in ROOT.glob('*.html'):
   p=Links();p.feed(path.read_text());self.assertEqual(p.h1,1,path.name)
   self.assertEqual(len(p.ids),len(set(p.ids)),path.name)
   for link in p.links:
    u=urlparse(link)
    if u.scheme or link.startswith('//'):continue
    target=ROOT/unquote(u.path) if u.path else path
    self.assertTrue(target.exists(),f'{path.name}: {link}')
    if u.fragment and target.suffix=='.html':
     t=Links();t.feed(target.read_text());self.assertIn(u.fragment,t.ids,f'{path.name}: {link}')
 def test_real_review_assets_exist(self):
  self.assertGreaterEqual(len(list((ROOT/'assets/reviews-redacted').glob('*.webp'))),11)
 def test_shared_navigation_and_clear_hero(self):
  buttons=[]
  for page in ROOT.glob('*.html'):
   html=page.read_text()
   buttons.append(re.search(r'<button class="menu-toggle".*?</button>',html).group())
   self.assertEqual(html.count('id="mobile-menu"'),1,page.name)
   self.assertIn('ui.js?v=20261111-palace1',html,page.name)
   self.assertIn('luxury.css?v=20261111-palace1',html,page.name)
  self.assertEqual(len(set(buttons)),1)
  self.assertNotIn('home-fashion',(ROOT/'index.html').read_text())
  self.assertIn('fashion-sprite wine',(ROOT/'about.html').read_text())
 def test_published_review_sources_are_redacted(self):
  html=(ROOT/'reviews.html').read_text()
  self.assertNotIn('assets/reviews/',html)
  self.assertEqual(html.count('data-review='),11)
 def test_salon_and_footer(self):
  html=(ROOT/'reviews.html').read_text()
  self.assertEqual(html.count('class="salon-frame '),11)
  self.assertIn('class="salon-host"',html)
  self.assertIn('aria-label="Закрыть отзыв"',html)
  for page in ROOT.glob('*.html'):
   self.assertNotIn('Постановочные fashion-образы',page.read_text())
 def test_review_images_fully_decode(self):
  from PIL import Image
  for path in (ROOT/'assets/reviews-redacted').glob('*.webp'):
   with Image.open(path) as image:
    image.load()
    self.assertGreater(image.height,500,path.name)
 def test_payment_never_collects_in_browser(self):
  if not (ROOT/'commerce.js').exists():self.fail('checkout not implemented')
  js=(ROOT/'commerce.js').read_text();self.assertNotIn('localStorage',js);self.assertNotIn('cardNumber',js)
if __name__=='__main__':unittest.main()

from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import unittest,re,json
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
  self.assertGreaterEqual(len(list((ROOT/'assets/reviews-redacted').glob('*.webp'))),35)
 def test_shared_navigation_and_clear_hero(self):
  buttons=[]
  for page in ROOT.glob('*.html'):
   html=page.read_text()
   buttons.append(re.search(r'<button class="menu-toggle".*?</button>',html).group())
   self.assertEqual(html.count('id="mobile-menu"'),1,page.name)
   self.assertIn('ui.js?v=20261111-menu1',html,page.name)
   self.assertIn('luxury.css?v=20261111-menu1',html,page.name)
  self.assertEqual(len(set(buttons)),1)
  self.assertNotIn('home-fashion',(ROOT/'index.html').read_text())
  self.assertIn('fashion-sprite wine',(ROOT/'about.html').read_text())
 def test_published_review_sources_are_redacted(self):
  html=(ROOT/'reviews.html').read_text()
  self.assertNotIn('assets/reviews/',html)
  self.assertEqual(html.count('data-review='),35)
 def test_salon_and_footer(self):
  html=(ROOT/'reviews.html').read_text()
  self.assertEqual(html.count('class="salon-frame '),35)
  self.assertIn('class="salon-host"',html)
  self.assertIn('aria-label="Закрыть отзыв"',html)
  for page in ROOT.glob('*.html'):
   self.assertNotIn('Постановочные fashion-образы',page.read_text())
 def test_review_images_fully_decode(self):
  from PIL import Image
  for path in (ROOT/'assets/reviews-redacted').glob('*.webp'):
   with Image.open(path) as image:
    image.load()
    self.assertGreater(min(image.width,image.height),100,path.name)
 def test_review_catalog_covers_all_sources(self):
  catalog=json.loads((ROOT/'review-catalog.json').read_text())
  items=catalog['items']
  self.assertEqual(len(items),35)
  self.assertEqual(len({item['image'] for item in items}),35)
  self.assertEqual(len({item['source'] for item in items}),33)
  self.assertEqual(catalog['source_file_count']-len(catalog['duplicate_files']),33)
  for item in items:self.assertTrue((ROOT/'assets/reviews-redacted'/('review-'+item['image'])).exists())
 def test_fireplace_has_transparent_surroundings_and_opening(self):
  from PIL import Image
  with Image.open(ROOT/'assets/palace-fireplace-cutout.webp') as image:
   self.assertEqual(image.mode,'RGBA')
   alpha=image.getchannel('A');w,h=image.size
   for point in [(0,0),(w-1,0),(0,h-1),(w-1,h-1),(w//2,h//2)]:self.assertEqual(alpha.getpixel(point),0)
   self.assertGreater(alpha.getpixel((w//2,h//5)),240)
 def test_payment_never_collects_in_browser(self):
  if not (ROOT/'commerce.js').exists():self.fail('checkout not implemented')
  js=(ROOT/'commerce.js').read_text();self.assertNotIn('localStorage',js);self.assertNotIn('cardNumber',js)
if __name__=='__main__':unittest.main()

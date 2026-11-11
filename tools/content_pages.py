"""Local editorial content. Source catalog is separate from the shared shell."""
from html import escape as e
import json,re

def add_content(ROOT,PAGES,add,section):
 recipes=json.loads((ROOT/'recipes.json').read_text())
 tiles=[]
 for x in recipes:
  slug='recipe-'+x['slug'];image=f'<img class="recipe-photo" src="{x["image"]}" alt="{e(x["title"])}" width="960" height="960" loading="lazy">'
  tiles.append(f'<a class="recipe-card" href="{slug}.html">{image}<div><span class="eyebrow">{x["minutes"]} МИН · {x["servings"]} ПОРЦИИ</span><h3>{x["title"]}</h3><p>{x["description"]}</p><span class="text-link">Готовим вместе →</span></div></a>')
  body=f'<article class="recipe-article"><a class="text-link" href="food.html">← Все рецепты</a><div class="recipe-heading"><div><span class="eyebrow">НА КУХНЕ ХИЩНИЦЫ</span><h1>{x["title"]}</h1><p>{x["description"]}</p><p class="recipe-meta">{x["minutes"]} минут · {x["servings"]} порции</p></div>{image}</div><div class="recipe-method"><section><h2>Что понадобится</h2><ul>'+''.join('<li>'+e(i)+'</li>' for i in x['ingredients'])+'</ul></section><section><h2>Как приготовить</h2><ol>'+''.join('<li>'+e(i)+'</li>' for i in x['steps'])+f'</ol><p class="recipe-tip">{x["tip"]}</p></section></div><p class="recipe-source">Редакционная адаптация на русском по мотивам рецепта <a href="{e(x["source"],quote=True)}">{e(x["source_name"])}</a>. Количество ингредиентов и способ подачи адаптированы. Фотоиллюстрация создана специально для этого рецепта.</p></article>'
  add(slug,x['title'],x['description'],body)
 add('food','Что мы едим','25 рецептов: мясо, рыба, яйца и сыр. Ингредиенты и пошаговое приготовление.',section('Мясо. Огонь.<br><em>И удовольствие.</em>','<p class="food-intro">Двадцать пять идей для домашней кухни: от рибая до нежного паштета. Русские адаптации рецептов американских и европейских авторов. Выбирайте блюдо и открывайте пошаговый рецепт.</p><div class="recipe-grid">'+''.join(tiles)+'</div>','НА КУХНЕ ХИЩНИЦЫ'))
 posts_path=ROOT/'max-posts.json'
 if not posts_path.exists():return
 posts=json.loads(posts_path.read_text())
 categories={'diary':[],'articles':[],'events':[],'individual':[],'food':[]}
 for x in reversed(posts):
  if not x.get('text') and not x.get('media'):continue
  category=x['category'];slug='journal-'+x['id'];media=''
  for m in x.get('media',[]):
   if m['type']=='video':
    media+=f'<figure class="journal-video {"circle-video" if x.get("circle") else ""}"><video controls playsinline preload="none" poster="{m.get("poster","")}" src="{m["src"]}" aria-label="{e(x["title"],quote=True)}"></video><figcaption><time datetime="{x["date"]}">{x["date_label"]}</time></figcaption></figure>'
   else:media+=f'<img class="journal-photo" src="{m["src"]}" alt="{e(x["title"],quote=True)}" loading="lazy">'
  paras=''.join('<p>'+e(p).replace('\n','<br>')+'</p>' for p in x['text'].split('\n\n') if p.strip())
  extra_links=''.join(f'<a class="text-link" href="{e(a["href"],quote=True)}">{e(a["text"])}</a>' for a in x.get('links',[]))
  body=f'<article class="journal-article"><a class="text-link" href="{category}.html">← К разделу</a><span class="eyebrow">АЛЁНА · ЛИЧНЫЙ ДНЕВНИК</span><h1>{e(x["title"])}</h1><time class="date-badge" datetime="{x["date"]}">{x["date_label"]} · {x["time"]}</time><div class="journal-media">{media}</div><div class="journal-prose">{paras}{extra_links}</div></article>'
  add(slug,x['title'],x['text'][:150] or x['title'],body)
  cover=next((m for m in x.get('media',[]) if m['type']=='image'),None)
  pic=f'<img src="{cover["src"]}" alt="" loading="lazy">' if cover else ''
  if x.get('circle') and media:tile=f'<article class="journal-card journal-circle-card">{media}<a href="{slug}.html"><h3>{e(x["title"])}</h3></a></article>'
  else:tile=f'<a class="journal-card" href="{slug}.html">{pic}<div><time datetime="{x["date"]}">{x["date_label"]}</time><h3>{e(x["title"])}</h3><p>{e(x["text"][:150])}</p><span class="text-link">Читать →</span></div></a>'
  categories[category].append(tile)
 for category,tiles in categories.items():
  if not tiles:continue
  block=section('Свежие <em>записи.</em>','<div class="journal-grid">'+''.join(tiles)+'</div>','ИЗ ЖИЗНИ ХИЩНИЦЫ')
  if category in ['diary','articles']:
   title='Личный дневник' if category=='diary' else 'Статьи и заметки';intro='Моменты, разговоры и короткие видео из моей жизни.' if category=='diary' else 'Мои мысли о еде, привычках и повседневной жизни.'
   add(category,title,intro,section(title,f'<p>{intro}</p>')+block)
  else:
   title,desc,body,theme=PAGES[category];PAGES[category]=(title,desc,body+block,theme)

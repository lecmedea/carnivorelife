"""Build the static multi-page site from one catalog and shared page shell."""
from pathlib import Path
from html import escape as e
import json,re
ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/'site-config.json').read_text())
MAX=CONFIG['max_url'];BASE=CONFIG['base_url']
PAGES={}
NAV=[('about','Обо мне'),('services','Услуги'),('reviews','Отзывы'),('events','Афиша'),('club','Клуб'),('retreats','Ретриты')]

def icon(name):
 return f'<svg class="icon" aria-hidden="true" focusable="false"><use href="icons.svg#{name}"></use></svg>'
def link(href,label,cls='text-link'):
 return f'<a class="{cls}" href="{e(href,quote=True)}">{label} {icon("arrow")}</a>'
def sprite(variant='wine',cls=''):
 return f'<div class="fashion-sprite {variant} {cls}" role="img" aria-label="Постановочный образ Алёны в вечернем платье с чёрной пантерой"></div>'
def hero(kicker,title,text,variant='wine'):
 return f'<section class="editorial-hero"><div class="editorial-copy"><div class="eyebrow">{kicker}</div><h1>{title}</h1><p class="hero-description">{text}</p>{link(MAX,"Написать Алёне в MAX","button primary")}</div><div class="fashion-stage">{sprite(variant)}<span class="stage-caption">ДНЕВНИК ХИЩНИЦЫ · ХАРАКТЕР И ВКУС</span></div></section>'
def section(title,body,kicker=''):
 return f'<section class="content-section"><div class="eyebrow">{kicker}</div><h2>{title}</h2>{body}</section>'
def note(text):return f'<p class="editorial-note">{text}</p>'
def cta(title='Давайте знакомиться',text='Расскажите о своём запросе. Вместе выберем следующий шаг.'):
 return f'<section class="page-cta"><div><span class="eyebrow">НА СВОЕЙ СТОРОНЕ</span><h2>{title}</h2><p>{text}</p></div>{link(MAX,"Написать в MAX","button primary")}</section>'
def cards(items):
 return '<div class="editorial-grid">'+''.join(f'<article class="editorial-card">{icon("calendar" if h=="marathons.html" else "diamond" if h in ["club.html","retreats.html"] else "spark")}<span class="eyebrow">{k}</span><h3>{t}</h3><p>{b}</p>{link(h,l)}</article>' for k,t,b,h,l in items)+'</div>'
def service_card(s,i):
 price=s.get('price_range') or ('Стоимость — '+str(s['price'])+' ₽' if s['price'] else 'Условия — лично')
 return f'<article class="editorial-card service-tile"><span class="eyebrow">0{i} / {s["eyebrow"]}</span><h3>{s["title"]}</h3><p>{s["intro"]}</p><span class="price">{price}</span>{link(s["id"]+".html","Подробнее")}</article>'
def header(current=''):
 links=''.join(f'<a href="{p}.html"'+(' aria-current="page"' if p==current else '')+f'>{t}</a>' for p,t in NAV)
 extra_links=''.join(f'<a href="{slug}.html">{label}</a>' for slug,label in [('nutrition','О питании'),('food','Что мы едим'),('diary','Дневник'),('articles','Статьи'),('faq','Вопросы'),('questionnaires','Анкеты'),('documents','Документы'),('contacts','Контакты')])
 return f'<a class="skip" href="#main">Перейти к содержанию</a><header class="site-header"><a class="brand" href="index.html" aria-label="Дневник Хищницы — на главную"><img src="logo.svg" alt="" width="38" height="44"><span>Дневник<br><b>Хищницы</b></span></a><nav aria-label="Основная навигация">{links}</nav><a class="nav-cta" href="{MAX}">Написать в MAX {icon("arrow")}</a><button class="menu-toggle" aria-label="Открыть меню" aria-expanded="false" aria-controls="mobile-menu">Меню {icon("menu")}</button></header><nav id="mobile-menu" class="mobile-menu" aria-label="Мобильное меню" hidden>{links}{extra_links}</nav>'
def footer():
 extra=[('about','Обо мне'),('services','Услуги'),('reviews','Отзывы'),('events','Афиша'),('club','Клуб'),('retreats','Ретриты'),('nutrition','О питании'),('food','Что мы едим'),('diary','Дневник'),('articles','Статьи'),('faq','Вопросы'),('contacts','Контакты'),('documents','Документы')]
 socials=[('max',MAX,'MAX'),('telegram','https://t.me/mycarnivorelife','Telegram'),('vk','https://vk.ru/carnivorelife','ВКонтакте'),('dzen','https://dzen.ru/carnivorelife','Дзен')]
 return '<footer class="site-footer"><a class="brand" href="index.html"><img src="logo.svg" width="42" height="42" alt="След львиной лапы"><span>Дневник<br><b>Хищницы</b></span></a><div class="socials">'+''.join(f'<a href="{url}" aria-label="{label}">{icon(symbol)}<span>{label}</span></a>' for symbol,url,label in socials)+'</div><div class="footer-nav">'+''.join(f'<a href="{p}.html">{t}</a>' for p,t in extra)+'</div><p>Health-коучинг и личный опыт. Не медицинская помощь. Результаты индивидуальны.<br>© 2026 Дневник Хищницы</p><button class="effects" aria-pressed="true">Сочный кровавый режим: вкл.</button></footer>'

def head(slug,title,description):
 return f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#faf9f6"><title>{e(title)} — Дневник Хищницы</title><meta name="description" content="{e(description,quote=True)}"><link rel="canonical" href="{BASE}{slug}.html"><meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(description,quote=True)}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}{slug}.html"><meta property="og:image" content="{BASE}assets/alena-atlas.webp"><link rel="icon" href="logo.svg"><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="luxury.css"><script src="ui.js" defer></script><script src="app.js" defer></script></head>'
def add(slug,title,desc,body,theme='light'):
 PAGES[slug]=(title,desc,body,theme)
REVIEW_QUOTES=json.loads((ROOT/'review-quotes.json').read_text())
REVIEW_IMAGES=['06-gallery.webp','07-gallery.webp','10-gallery.webp','11-gallery.webp','16-gallery.webp','17-gallery.webp','18-gallery.webp']
EXTRA_REVIEWS=['19-gallery.webp','20-gallery.webp','21-gallery.webp','22-gallery.webp']
def review_card(n,i=0):
 return f'<figure class="salon-frame frame-{i+1} finish-{i%4}"><a href="assets/reviews-redacted/review-{n}" data-review="{n}" aria-label="Увеличить отзыв {i+1}"><span class="frame-mat"><img src="assets/reviews-redacted/review-{n}" alt="Скриншот отзыва {i+1}, личные данные скрыты" loading="eager" decoding="async"></span><span class="frame-zoom">{icon("arrow")}<span>Читать отзыв {i+1}</span></span></a></figure>'
def reviews_markup():
 return '<section class="salon-section palace-room" aria-label="Картинная галерея отзывов"><div class="salon-stage"><div class="pendant pendant-1"><span class="lamp-beam" aria-hidden="true"></span><button class="lamp-button" type="button" aria-label="Покачать светильник 1"><img src="assets/palace-lantern.webp" alt="" width="724" height="2172"><span class="lamp-flame" aria-hidden="true"></span></button></div><div class="pendant pendant-2"><span class="lamp-beam" aria-hidden="true"></span><button class="lamp-button" type="button" aria-label="Покачать светильник 2"><img src="assets/palace-lantern.webp" alt="" width="724" height="2172"><span class="lamp-flame" aria-hidden="true"></span></button></div><div class="salon-wall">'+''.join(review_card(n,i) for i,n in enumerate(REVIEW_IMAGES))+'</div><div class="salon-host" aria-hidden="true">'+sprite('navy')+'</div><span class="salon-signature">Галерея тёплых слов</span><div class="room-light" aria-hidden="true"></div></div><div class="salon-continuation" aria-label="Продолжение галереи">'+''.join(review_card(n,i+len(REVIEW_IMAGES)) for i,n in enumerate(EXTRA_REVIEWS))+'</div></section><dialog id="review-dialog" class="review-dialog" aria-label="Просмотр отзыва"><div class="review-toolbar"><span id="review-counter" aria-live="polite"></span><button type="button" class="review-close" aria-label="Закрыть отзыв">'+icon('close')+'</button></div><div class="review-scroll"><img id="review-full" alt="Увеличенный скриншот отзыва" decoding="sync"><p id="review-status" role="status"></p></div><div class="review-controls"><button type="button" data-review-step="-1" aria-label="Предыдущий отзыв">'+icon('back')+'<span>Предыдущий</span></button><button type="button" data-review-step="1" aria-label="Следующий отзыв"><span>Следующий</span>'+icon('next')+'</button></div></dialog>'

services=CONFIG['services']
add('services','Услуги Алёны','Индивидуальное сопровождение, марафоны, меню и образовательные консультации с Алёной.',hero('ЛИЧНО И В КРУГУ СВОИХ','Ваш путь.<br><em>Моя поддержка.</em>','Выберите формат, в котором вам будет комфортно. Начать можно с простого разговора.','emerald')+section('Внимание <em>к вам.</em>','<div class="editorial-grid">'+''.join(service_card(s,i) for i,s in enumerate(services,1))+'</div>')+note('Я не врач. Не ставлю диагнозы, не назначаю лечение и не отменяю назначения. Изменения питания при заболеваниях обсуждайте с лечащим врачом.')+cta())
for s in services:
 body=hero(s['eyebrow'],s['title'],s['intro'],'navy' if s['id']=='analyses' else 'emerald')
 body+=section('Как это <em>устроено.</em>','<ol class="steps">'+''.join(f'<li><span>0{i}</span><p>{text}</p></li>' for i,text in enumerate(s['items'],1))+'</ol>')
 if s['id']=='analyses':body+=section('Вопросы, с которыми<br>можно <em>пойти к врачу.</em>','<p>В прошедших марафонах я бесплатно помогала участникам разобраться в обозначениях показателей и подготовить вопросы специалисту. Это мой рассказ о работе в группе, а не отзыв клиента и не медицинское заключение.</p><p>Образовательная консультация — 500–2 500 ₽. Итоговая стоимость зависит от согласованного объёма.</p>')
 body+=section('Следующий шаг',f'<p>Уточним запрос, длительность, объём и стоимость до начала работы.</p>{link("checkout.html?service="+s["id"],"Выбрать услугу","button primary")} '+link(MAX,'Задать вопрос'))
 body+=note('Сопровождение и образовательные консультации не заменяют медицинскую помощь. При противопоказаниях формат может не подойти; порядок отказа и возврата определяется условиями услуги.')
 add(s['id'],s['title'],s['intro'],body)
add('reviews','Отзывы и результаты','Галерея скриншотов отзывов участников марафонов и сопровождения Алёны.','<section class="salon-intro"><div class="eyebrow">ГАЛЕРЕЯ ЖИВЫХ ИСТОРИЙ</div><h1>Слова, которые<br><em>остаются.</em></h1><p>За каждой рамой — настоящее сообщение. Откройте картину, чтобы прочитать его крупно.</p></section>'+reviews_markup()+note('Имена, аватары и отдельные личные сведения в скриншотах закрыты. Несколько скриншотов могут быть фрагментами одного сообщения. Опыт каждого человека индивидуален.')+cta('Пора написать<br><em>свою историю.</em>')+'<section class="palace-hearth" aria-label="Венецианский камин"><img src="assets/palace-fireplace.webp" alt="Резной мраморный камин со львом, позолотой и тлеющими поленьями" width="1536" height="1024" loading="lazy"><canvas class="hearth-fire" aria-hidden="true"></canvas><span class="hearth-glow" aria-hidden="true"></span></section><script src="salon.js?v=20261111-palace1" defer></script>', 'gallery')
add('about','Об Алёне','Алёна — автор Дневника Хищницы, предприниматель и health-коуч.',hero('Я НАСТОЯЩАЯ','В своей жизни —<br><em>главная.</em>','Я Алёна. Предприниматель, мама и автор «Дневника Хищницы». Люблю жизнь с характером: настоящую еду, красивые вещи и людей, с которыми можно быть собой.','wine')+section('Не только <em>про еду.</em>','<div class="prose-columns"><p>Мой путь к своему питанию был длинным: попытки, вопросы и поиск того, что подходит лично мне. Кето и карнивор стали частью моей повседневной жизни.</p><p>Теперь я делюсь опытом и поддерживаю людей в работе с привычками. Мне важно, чтобы за любым рационом оставался человек — с его ритмом, вкусами и жизнью.</p></div>')+section('Свобода быть <em>собой.</em>',cards([('ХАРАКТЕР','Красота — тоже часть жизни','Мех, блеск бриллиантов и большие планы. Мне нравится выбирать то, что радует.','diary.html','Мой дневник'),('ВНИМАНИЕ','Работа с человеком','Помогаю разбираться с повседневным питанием и не оставаться один на один с вопросами.','individual.html','О сопровождении')]))+cta())
add('nutrition','О кето и карниворе','Знакомство с подходом Алёны к питанию и границами health-коучинга.',hero('МОЙ ПОДХОД','Настоящая еда.<br><em>Осознанный выбор.</em>','Здесь — мой опыт и основные ориентиры для знакомства с питанием. Универсального рациона для всех не существует.','emerald')+section('С чего <em>начать.</em>',cards([('01','Понять свой запрос','Подумайте, что именно вы хотите изменить в повседневных привычках и какой поддержки вам не хватает.','consultation.html','Обсудить запрос'),('02','Увидеть простую еду','В моём карниворе — простые животные продукты и понятные способы приготовления.','food.html','Что мы едим'),('03','Учесть здоровье','При заболеваниях и приёме лекарств изменения питания сначала обсуждают с лечащим врачом.','faq.html','Частые вопросы')]))+cta())
add('food','Что мы едим','Фотоиллюстрации простой еды в карниворе: мясо, яйца и приготовление на огне.',hero('ПРОСТО И СО ВКУСОМ','Еда без<br><em>лишнего шума.</em>','Мясо на огне. Яйца. Понятные продукты. Эта галерея — про вкус и простоту, а не сложные рецепты.','wine')+section('Ничего <em>лишнего.</em>','<div class="food-grid">'+''.join(f'<figure><div class="food-sprite food-{i}" role="img" aria-label="{title}"></div><figcaption>{title}</figcaption></figure>' for i,title in enumerate(['Стейк в керамической тарелке','Яйца и мясо','Рёбра на огне']))+'</div>')+note('Фотоиллюстрации созданы с помощью ИИ. Это примеры подачи, а не фотографии рационов клиентов или индивидуальная рекомендация.')+cta())
event_items=[('ГРУППОВАЯ ПОДДЕРЖКА','Марафоны','Ближайший набор, программа и условия — у Алёны. Дата следующей группы будет опубликована после подтверждения.','marathons.html','Узнать о группе'),('ВСТРЕЧИ','Клуб Хищниц','Первые встречи планируются в Москве. Город и место каждой встречи появятся в анонсе.','club.html','О клубе'),('ПУТЕШЕСТВИЯ','Ретриты с Хищницей','Лес, озёра, огонь и мясо. Будущие поездки в тёплый сезон, в Московскую и соседние области.','retreats.html','О поездках')]
add('events','Афиша','Предстоящие марафоны, встречи, эфиры и поездки Дневника Хищницы.',hero('ЖИЗНЬ ПРОДОЛЖАЕТСЯ','Есть повод<br><em>встретиться.</em>','Марафоны, живые встречи и будущие путешествия. Здесь появятся подтверждённые даты, программы эфиров и лекций.','wine')+section('Ближайшее и <em>будущее.</em>',cards(event_items))+cta('Узнать <em>первой.</em>','Напишите, какое событие вам интересно. Алёна расскажет о ближайших планах.'))
add('club','Клуб Хищниц','Будущие реальные встречи с Алёной и сообществом Дневника Хищницы.',hero('СВОИ УЗНАЮТ СВОИХ','Клуб<br><em>Хищниц.</em>','Из переписки — в настоящую жизнь. Круг женщин, которым хочется общения, красивых встреч и поводов выбираться из повседневности.','emerald')+section('Увидимся <em>вживую.</em>','<div class="prose-columns"><p>Первые встречи планируются в Москве. Сам клуб не привязан к одному городу: географию будем расширять вместе с сообществом.</p><p>Дата, место, программа и стоимость будут указаны в анонсе каждой встречи. Сейчас можно сообщить Алёне о своём интересе.</p></div>')+cta('Хочу <em>в свой круг.</em>','Напишите Алёне, из какого вы города и какой формат встреч вам интересен.'),'club-theme')
add('retreats','Ретриты с Хищницей','Будущие групповые поездки с Алёной: природа, костры и общение.',hero('ПЛАНЫ НА ТЁПЛЫЙ СЕЗОН','Подальше<br><em>от суеты.</em>','Дремучий лес, озеро, огонь и мясо на углях. Несколько дней с людьми, которым хорошо вместе.','navy')+section('Ретриты <em>с Хищницей.</em>','<div class="prose-columns"><p>Планируем групповые поездки в Московскую и соседние области: природа, уютный отель и время для себя.</p><p>Направления и программы готовятся. Точные даты, состав поездки и стоимость появятся после подтверждения. Сейчас можно оставить интерес, без оплаты места.</p></div>')+cta('Я бы <em>поехала.</em>','Расскажите Алёне, какие направления и продолжительность поездки вам интересны.'),'retreat-theme')
add('diary','Личный дневник','Заметки Алёны о жизни, питании, привычках и маленьких радостях.',hero('НЕ ТОЛЬКО ПРО ЕДУ','Поводы<br><em>расцветать.</em>','Дом, близкие, красивые вещи и настоящая еда. Моя жизнь шире любой системы питания.','wine')+section('Продолжение — <em>в дневнике.</em>',cards([('MAX','Мой каждый день','Живые заметки, короткие видео и разговоры с сообществом.',MAX,'Открыть дневник'),('ВКОНТАКТЕ','Оставаться на связи','Новости и публикации на удобной вам площадке.','https://vk.ru/carnivorelife','Открыть ВКонтакте')]))+cta())
add('articles','Статьи и полезные материалы','Полные публикации Алёны в Дзене и материалы Дневника Хищницы.',hero('ЕСТЬ ЧТО ПОЧИТАТЬ','Мысли<br><em>со вкусом.</em>','Полные статьи собираю в Дзене. Здесь — путь к публикациям, которые можно спокойно прочитать и сохранить.','navy')+section('Длинные тексты —<br><em>в своём ритме.</em>',f'<p>Личный опыт, питание и повседневные привычки. Откройте канал, чтобы выбрать материал по интересующей теме.</p>{link("https://dzen.ru/carnivorelife","Читать в Дзене","button primary")}')+cta())
questions=[('С чего начать?','Напишите Алёне в MAX, расскажите о своём запросе. Можно выбрать личную консультацию или обсудить сопровождение.'),('Алёна врач?','Нет. Алёна работает как health-коуч, делится опытом и помогает с привычками. Диагностика и лечение относятся к компетенции врача.'),('Подходит ли карнивор всем?','Нет. При заболеваниях, беременности, приёме лекарств и других обстоятельствах изменения питания необходимо обсудить с лечащим врачом.'),('Есть ли гарантированный результат?','Нет. Истории участников отражают личный опыт. Реакция на питание и результаты индивидуальны.'),('Как узнать стоимость?','Условия каждой услуги уточняются до покупки. Для образовательной консультации по анализам заявлен диапазон 500–2 500 ₽.'),('Как попасть на встречу или ретрит?','Пока собираем интерес. Напишите Алёне; даты, программа и условия участия будут опубликованы в афише после подтверждения.')]
add('faq','Частые вопросы','Ответы о сопровождении, питании и будущих встречах с Алёной.',section('Можно <em>спросить?</em>','<div class="faq-list">'+''.join(f'<details><summary>{q}<span>+</span></summary><p>{a}</p></details>' for q,a in questions)+'</div>','БЕЗ НЕДОСКАЗАННОСТИ')+cta())
phone=link('tel:'+re.sub(r'[^+\d]','',CONFIG['phone']),'Позвонить','button') if CONFIG['phone'] else '<p>Для личного разговора напишите Алёне в MAX и договоритесь о звонке.</p>'
form=link(CONFIG['request_form_url'],'Оставить заявку','button primary') if CONFIG['request_form_url'] else link(MAX,'Оставить заявку в MAX','button primary')
add('contacts','Контакты и запись','Связаться с Алёной в MAX, записаться на консультацию или уточнить условия сопровождения.',hero('Я НА СВЯЗИ','Начнём<br><em>с разговора.</em>','Пара слов о вас и вашем запросе. Алёна ответит лично и поможет выбрать формат.','emerald')+section('Как вам <em>удобнее.</em>',f'<div class="contact-options">{link(MAX,"Написать в MAX","button primary")}{phone}{link("https://vk.ru/carnivorelife","Написать ВКонтакте","button")}</div>')+section('Заявка на услугу',f'<p>Укажите в сообщении интересующий формат и удобное время для связи. Анализы и сведения о здоровье в общей заявке присылать не нужно.</p>{form}')+note('Анкеты перед оказанием услуги передаются отдельно с соответствующими документами и согласиями.'))
docs=CONFIG['documents']
docsbody='<ul class="document-list">'+''.join(f'<li>{link(x["url"],e(x["title"]))}</li>' for x in docs)+'</ul>' if docs else '<p>Документы по выбранной услуге можно запросить у Алёны до оплаты: оферту, политику обработки персональных данных, необходимые согласия и условия возврата.</p>'+link(MAX,'Получить документы','button primary')
add('documents','Документы и условия','Оферты, согласия и условия оказания услуг Дневника Хищницы.',section('Документы<br>и <em>условия.</em>',docsbody,'ДО ПРИНЯТИЯ РЕШЕНИЯ')+section('Анкеты перед началом работы','<p>Для разных услуг предусмотрены разные анкеты. Способ заполнения и перечень сведений сообщаются после выбора формата. Данные о здоровье не направляются через обычную форму заявки.</p>')+cta())
add('checkout','Выбрать услугу','Уточнить условия, стоимость и порядок оформления услуги Алёны.',section('Ваш <em>следующий шаг.</em>','<div id="checkout-panel"><p>Выберите услугу, чтобы увидеть условия.</p><label for="service-choice">Формат работы</label><select id="service-choice">'+''.join(f'<option value="{s["id"]}">{s["title"]}</option>' for s in services)+'</select><h2 id="checkout-title"></h2><p id="checkout-description"></p><p id="checkout-price" class="price"></p><div id="checkout-documents"></div><a id="checkout-action" class="button primary" href="'+MAX+'">Уточнить условия в MAX ↗</a><p id="checkout-status" role="status"></p></div>','ЛИЧНО С АЛЁНОЙ')+'<script src="commerce.js" defer></script>')

for slug,(title,desc,body,theme) in PAGES.items():
 body=body.replace('<h2>', '<h1>',1).replace('</h2>', '</h1>',1) if '<h1>' not in body else body
 html=head(slug,title,desc).replace('</head>', '<link rel="stylesheet" href="salon.css?v=20261111-palace1"></head>' if slug=='reviews' else '</head>')+f'<body class="inner-page {theme}">'+header(slug)+f'<main id="main">{body}</main>'+footer()+'<canvas id="liquid" aria-hidden="true"></canvas></body></html>'
 (ROOT/f'{slug}.html').write_text(html)

# Preserve the existing home composition while adding real page navigation.
if (ROOT/'tools/home-original.html').exists():
 home=(ROOT/'tools/home-original.html').read_text()
 home=home.replace('<link rel="stylesheet" href="style.css">','<link rel="canonical" href="'+BASE+'"><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="luxury.css"><script src="ui.js" defer></script>')
 home=re.sub(r'<a class="skip"[^>]*>.*?</a>', '', home)
 home=re.sub(r'<header>.*?</header>',header(),home,flags=re.S)
 home=home.replace('https://t.me/alenaladushki',MAX).replace('напишите мне в Telegram','напишите мне в MAX')
 home=home.replace('<b>42</b><span>посаженных дерева</span>','<b>Лично</b><span>внимание к вашему запросу</span>')
 home=home.replace('<a class="button primary" href="'+MAX+'" target="_blank" rel="noopener">Открыть дневник <span>↗</span></a>','<a class="button primary" href="individual.html">Личное сопровождение <span>↗</span></a>')
 home=home.replace('href="#story">Давайте знакомиться','href="about.html">Давайте знакомиться')
 # Replace the selfie paper hero with an integrated fashion sprite.
 home=re.sub(r'<figure class="photo hero-photo collision">.*?</figure>','',home,count=1,flags=re.S)
 home=home.replace('Стоимость и условия обсуждаем лично до начала работы.','Выберите формат и уточните условия до начала работы.')
 home=home.replace('Обсудить сопровождение <span>↗</span>','Подробнее о сопровождении <span>↗</span>',1)
 home=home.replace(f'<a href="{MAX}" target="_blank" rel="noopener" class="text-link">Подробнее о сопровождении', '<a href="individual.html" class="text-link">Подробнее о сопровождении',1)
 home=home.replace(f'<a href="{MAX}" target="_blank" rel="noopener" class="text-link">Узнать о ближайшей группе','<a href="marathons.html" class="text-link">Узнать о ближайшей группе',1)
 new=section('Встречи, которые<br><em>хочется ждать.</em>',cards(event_items),'АФИША · КЛУБ · РЕТРИТЫ')
 new+=section('Слова, которые <em>остаются.</em>','<div class="home-review-preview">'+''.join(f'<a class="review-frame" href="reviews.html"><img src="assets/reviews-redacted/review-{n}" alt="Скриншот отзыва с закрытыми личными данными" loading="lazy"></a>' for n in REVIEW_IMAGES[:3])+'</div>'+link('reviews.html','Войти в галерею отзывов','button primary'))
 home=home.replace('<section class="faq section">',new+'<section class="faq section">')
 home=re.sub(r'<footer>.*?</footer>',footer(),home,flags=re.S)
 # Keep the personal easter egg safely isolated from page functionality.
 home=home.replace('<button id="secret"','<button id="secret"')
 # Remove redundant channel CTAs, retain service navigation and the social footer.
 home=re.sub(r'<a[^>]*>Давайте знакомиться.*?</a>', '', home)
 home=re.sub(r'<a[^>]*>В дневник Хищницы.*?</a>', '', home)
 home=home.replace('<span class="small-star">✳</span>',icon('spark'))
 home=home.replace('<i>✳</i>',icon('spark'))
 (ROOT/'index.html').write_text(home)
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+p+'</loc></url>' for p in ['']+[f'{s}.html' for s in PAGES if s!='checkout'])+'</urlset>')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /checkout.html\nDisallow: /tools/\nDisallow: /tests/\nSitemap: '+BASE+'sitemap.xml\n')
try:
 from privacy_pages import build_privacy_pages
except ModuleNotFoundError:
 privacy_slugs=[p.stem for p in ROOT.glob('*.html') if p.stem not in PAGES and p.stem!='index']
else:
 privacy_slugs=build_privacy_pages()
for path in ROOT.glob('*.html'):
 text=path.read_text()
 # Strip old cache keys before checking the shared asset tags.
 text=re.sub(r'((?:src|href)="(?:style|luxury|icons|privacy)\.(?:css|js)|src="(?:ui|app|liquid-physics|intake|commerce)\.js)\?v=[^"]*',r'\1',text)
 if 'src="privacy.js"' not in text:
  text=text.replace('</head>','<link rel="stylesheet" href="privacy.css"><script src="privacy.js" defer></script></head>')
 if path.stem in privacy_slugs:
  text=text.replace('</head>','<link rel="stylesheet" href="luxury.css"></head>') if 'href="luxury.css"' not in text else text
  text=text.replace('<body>', '<body>'+header()) if 'class="site-header"' not in text else text
  text=re.sub(r'<footer.*?</footer>',footer(),text,flags=re.S)
  if 'src="ui.js"' not in text:text=text.replace('</head>','<script src="ui.js" defer></script></head>')
 text=text.replace('href="logo.svg"><link rel="stylesheet"','href="favicon.svg?v=lion-2"><link rel="stylesheet"')
 text=text.replace('https://m.dzen.ru/carnivorelife','https://dzen.ru/carnivorelife')
 if 'href="icons.css"' not in text:text=text.replace('</head>','<link rel="stylesheet" href="icons.css"></head>')
 if 'src="app.js"' in text and 'src="liquid-physics.js"' not in text:text=text.replace('<script src="app.js"','<script src="liquid-physics.js" defer></script><script src="app.js"')
 text=text.replace('<span>↗</span>',icon('arrow'))
 text=text.replace('href="logo.svg"','href="favicon.svg?v=lion-2"') if '<link rel="icon" href="logo.svg"' in text else text
 for asset in ['style.css','luxury.css','icons.css','privacy.css','ui.js','app.js','liquid-physics.js','privacy.js','intake.js','commerce.js']:
  text=text.replace('="'+asset+'"','="'+asset+'?v=20261111-palace1"')
 text=text.replace('src="logo.svg"','src="logo.svg?v=lion-2"')
 # Keep repeated builds idempotent, including preserved legacy pages.
 seen_assets=set()
 def unique_asset(match):
  tag=match.group(0)
  if tag in seen_assets:return ''
  seen_assets.add(tag)
  return tag
 text=re.sub(r'<link[^>]*href="[^"]+\.css(?:\?[^"]*)?"[^>]*>|<script[^>]*src="[^"]+"[^>]*></script>',unique_asset,text)
 path.write_text(text)
# Append privacy routes to the sitemap without duplication.
sitemap=(ROOT/'sitemap.xml').read_text()
sitemap=sitemap.replace('</urlset>',''.join('<url><loc>'+BASE+slug+'.html</loc></url>' for slug in privacy_slugs)+'</urlset>')
(ROOT/'sitemap.xml').write_text(sitemap)
print(f'Built home + {len(PAGES)} editorial pages + {len(privacy_slugs)} privacy/intake pages')

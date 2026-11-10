'use strict';
(() => {
 const VERSION='2026-11-10.1',KEY='khishnitsa-privacy-choice';
 let banner,opener;
 function read(){try{const r=JSON.parse(localStorage.getItem(KEY));return r?.version===VERSION?r:null}catch{return null}}
 function choose(value){try{localStorage.setItem(KEY,JSON.stringify({version:VERSION,value,at:new Date().toISOString()}))}catch{}banner.hidden=true;opener?.focus()}
 function show(){banner.hidden=false;banner.querySelector('button').focus()}
 function setup(){
  banner=document.createElement('section');banner.className='privacy-banner';banner.setAttribute('aria-label','Ваши персональные данные');
  banner.innerHTML='<div><span class="privacy-kicker">ВАША ПРИВАТНОСТЬ</span><h2>Сначала — ваше согласие.</h2><p>Для заявки и сопровождения Алёна использует только необходимые данные. Условия можно прочитать полностью. Просматривать сайт можно без согласия; сведения о здоровье требуют отдельного оформления.</p><a href="consent.html">Прочитать полные условия ↗</a></div><div class="privacy-actions"><button type="button" data-choice="agree">Согласен(на)</button><button type="button" data-choice="decline">Продолжить без согласия</button></div>';
  banner.querySelectorAll('[data-choice]').forEach(b=>b.addEventListener('click',()=>choose(b.dataset.choice)));
  document.body.append(banner);banner.hidden=!!read();
  const footer=document.querySelector('footer')||document.body;
  const settings=document.createElement('button');settings.className='privacy-settings';settings.type='button';settings.textContent='Настройки приватности';settings.addEventListener('click',()=>{opener=settings;show()});footer.append(settings);
  const nav=document.createElement('div');nav.className='privacy-links';
  [['privacy.html','Политика обработки данных'],['consent.html','Согласие'],['questionnaires.html','Анкеты']].forEach(([href,label])=>{const a=document.createElement('a');a.href=href;a.textContent=label;nav.append(a)});footer.append(nav);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',setup);else setup();
})();

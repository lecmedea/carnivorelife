'use strict';
(() => {
 const menu=document.querySelector('#mobile-menu');
 const toggle=document.querySelector('.menu-toggle');
 function setMenu(open){if(!menu||!toggle)return;menu.hidden=!open;if(!open)menu.querySelectorAll('details[open]').forEach(section=>section.open=false);toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Закрыть меню':'Открыть меню');toggle.querySelector('use')?.setAttribute('href','icons.svg?v=20261111-palace2#'+(open?'close':'menu'))}
 function closeMenu(){setMenu(false)}
 toggle?.addEventListener('click',()=>setMenu(toggle.getAttribute('aria-expanded')!=='true'));
 document.addEventListener('click',e=>{if(menu&&!menu.hidden&&!menu.contains(e.target)&&!toggle?.contains(e.target))closeMenu()});
 menu?.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu()});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu&&!menu.hidden){closeMenu();toggle.focus()}});
 const portraits=[...document.querySelectorAll('.fashion-sprite')];
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 let scheduled=false;
 addEventListener('scroll',()=>{if(scheduled||reduced.matches)return;scheduled=true;requestAnimationFrame(()=>{for(const portrait of portraits){const y=portrait.parentElement.getBoundingClientRect().top;portrait.style.transform=`translateY(${Math.max(-14,Math.min(14,-y*.025))}px)`}scheduled=false})},{passive:true});
 const links=[...document.querySelectorAll('[data-review]')];
 const dialog=document.querySelector('#review-dialog');
 if(!dialog)return;
 let selected=0,lastTrigger=null;
 const full=document.querySelector('#review-full'),status=document.querySelector('#review-status');
 const scroller=dialog.querySelector('.review-scroll');
 const zoom=dialog.querySelector('.review-size');
 function setOriginal(original){scroller.classList.toggle('actual-size',original);zoom?.setAttribute('aria-pressed',String(original));if(zoom){zoom.textContent=original?'Вписать в окно':'Масштаб 100%';zoom.setAttribute('aria-label',original?'Вписать отзыв в окно':'Показать отзыв в исходном масштабе')}scroller.scrollTop=0;scroller.scrollLeft=0}
 zoom?.addEventListener('click',()=>setOriginal(!scroller.classList.contains('actual-size')));
 full.addEventListener('load',()=>{status.textContent=''});
 full.addEventListener('error',()=>{status.textContent='Не удалось загрузить изображение. Попробуйте открыть другой отзыв и вернуться.'});
 function show(index){setOriginal(false);selected=(index+links.length)%links.length;status.textContent='Загружается отзыв…';full.src=links[selected].getAttribute('href');full.alt=links[selected].querySelector('img').alt;scroller.scrollTop=0;document.querySelector('#review-counter').textContent=`${selected+1} / ${links.length}`;if(full.complete&&full.naturalWidth)status.textContent=''}
 links.forEach((a,i)=>a.addEventListener('click',e=>{e.preventDefault();lastTrigger=a;show(i);dialog.showModal()}));
 dialog.querySelector('.review-close').addEventListener('click',()=>dialog.close());
 dialog.addEventListener('close',()=>lastTrigger?.focus({preventScroll:true}));
 dialog.querySelectorAll('[data-review-step]').forEach(b=>b.addEventListener('click',()=>show(selected+Number(b.dataset.reviewStep))));
 dialog.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();show(selected+1)}if(e.key==='ArrowLeft'){e.preventDefault();show(selected-1)}});
 dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close()}});
})();
;document.querySelectorAll('.nav-expand').forEach(button=>{button.addEventListener('click',()=>{const group=button.closest('.nav-group');const open=!group.classList.contains('is-open');document.querySelectorAll('.nav-group.is-open').forEach(g=>{g.classList.remove('is-open');g.querySelector('.nav-expand').setAttribute('aria-expanded','false')});group.classList.toggle('is-open',open);button.setAttribute('aria-expanded',String(open))})});document.addEventListener('keydown',event=>{if(event.key==='Escape')document.querySelectorAll('.nav-group.is-open').forEach(g=>{g.classList.remove('is-open');g.querySelector('.nav-expand').setAttribute('aria-expanded','false')})});

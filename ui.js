'use strict';
(() => {
 const menu=document.querySelector('#mobile-menu');
 const toggle=document.querySelector('.menu-toggle');
 function setMenu(open){if(!menu||!toggle)return;menu.hidden=!open;toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Закрыть меню':'Открыть меню');toggle.querySelector('use')?.setAttribute('href','icons.svg#'+(open?'close':'menu'))}
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
 let selected=0;
 const full=document.querySelector('#review-full'),quote=document.querySelector('#review-quote');
 function show(index){selected=(index+links.length)%links.length;const text=links[selected].dataset.reviewText;full.hidden=!!text;if(quote){quote.hidden=!text;quote.textContent=text?'«'+text+'»':''}if(!text)full.src=links[selected].getAttribute('href');document.querySelector('#review-counter').textContent=`${selected+1} / ${links.length}`}
 links.forEach((a,i)=>a.addEventListener('click',e=>{e.preventDefault();show(i);dialog.showModal()}));
 dialog.querySelector('.review-close').addEventListener('click',()=>dialog.close());
 dialog.querySelectorAll('[data-review-step]').forEach(b=>b.addEventListener('click',()=>show(selected+Number(b.dataset.reviewStep))));
 dialog.addEventListener('keydown',e=>{if(e.key==='ArrowRight')show(selected+1);if(e.key==='ArrowLeft')show(selected-1)});
 dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close()}});
})();

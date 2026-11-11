'use strict';
(() => {
 const room=document.querySelector('.palace-room');
 if(!room)return;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const stage=room.querySelector('.salon-stage');
 const lamps=[...room.querySelectorAll('.pendant')].map(el=>({el,start:0,amplitude:0,angle:0}));
 let raf=0;
 function animate(t){
  raf=0;let moving=false;
  for(const lamp of lamps){
   const elapsed=(t-lamp.start)/1000;
   lamp.angle=reduced.matches?0:lamp.amplitude*Math.exp(-elapsed*.24)*Math.cos(elapsed*2.65);
   if(Math.abs(lamp.amplitude*Math.exp(-elapsed*.24))>.04)moving=true;else lamp.angle=0;
   lamp.el.style.transform=`rotate(${lamp.angle.toFixed(3)}deg)`;
  }
  const angle=lamps.reduce((sum,l)=>sum+l.angle,0);
  stage.style.setProperty('--shadow-x',`${(-angle*1.9).toFixed(2)}px`);
  stage.style.setProperty('--lamp-x',`${50+angle*2.5}%`);
  if(moving&&!document.hidden)raf=requestAnimationFrame(animate);
 }
 lamps.forEach(lamp=>lamp.el.querySelector('button').addEventListener('click',()=>{
  lamp.start=performance.now();lamp.amplitude=reduced.matches?0:Math.min(14,Math.abs(lamp.angle)+10);
  if(!raf)raf=requestAnimationFrame(animate);
 }));
 const fire=document.querySelector('.hearth-fire');
 const toggle=document.querySelector('.fire-toggle');
 if(!fire||!toggle)return;
 let inView=false,userEnabled=false;
 function loadFire(){if(!fire.getAttribute('src')){fire.src=fire.dataset.src;fire.load()}}
 function playFire(){
  if(document.hidden||!inView||(reduced.matches&&!userEnabled)){fire.pause();return}
  loadFire();fire.muted=true;
  fire.play().then(()=>{toggle.hidden=true}).catch(()=>{toggle.textContent='Включить огонь';toggle.hidden=false});
 }
 toggle.hidden=!reduced.matches;
 toggle.addEventListener('click',()=>{userEnabled=true;playFire()});
 new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;if(inView)playFire();else fire.pause()},{rootMargin:'100px'}).observe(fire);
 document.addEventListener('visibilitychange',()=>{if(document.hidden){fire.pause();cancelAnimationFrame(raf);raf=0}else{playFire();if(lamps.some(l=>l.amplitude))raf=requestAnimationFrame(animate)}});
 reduced.addEventListener('change',()=>{userEnabled=false;toggle.hidden=!reduced.matches;playFire();if(!raf)raf=requestAnimationFrame(animate)});
})();

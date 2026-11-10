'use strict';
// Original lightweight art-directed liquid: spring surface + ballistic droplets + DOM collisions.
(() => {
const canvas=document.querySelector('#liquid');
if(!canvas)return;
const ctx=canvas.getContext('2d');
const toggles=[...document.querySelectorAll('.effects')],reduce=matchMedia('(prefers-reduced-motion: reduce)');
let enabled=!reduce.matches;
try{enabled=enabled&&localStorage.getItem('carnivore-liquid')!=='off'}catch{}
let w=0,h=0,dpr=1,lastY=scrollY,lastScroll=performance.now(),energy=0,raf=0,lastTime=0,acc=0;
let surface=[],drops=[],stains=[],obstacles=[],lastSpawn=0,pointer=.66;
const nodes=85,STEP=1/60;
function resize(){const bounds=canvas.getBoundingClientRect(),oldW=w,oldH=h;w=bounds.width;h=bounds.height;dpr=Math.min(devicePixelRatio||1,1.5);canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);if(!surface.length)surface=Array.from({length:nodes},()=>({y:0,v:0}));if(oldW&&oldH)for(const p of drops){p.x*=w/oldW;p.y+=h-oldH}measure();wake()}
function measure(){obstacles=[...document.querySelectorAll('.collision')].map(el=>({el,r:el.getBoundingClientRect()})).filter(o=>o.r.bottom>0&&o.r.top<h)}
function state(){for(const toggle of toggles){toggle.setAttribute('aria-pressed',String(enabled));toggle.textContent=enabled?'◉ Живая жидкость: вкл.':'○ Живая жидкость: выкл.'}canvas.style.display=enabled?'block':'none'}
function wake(){if(enabled&&!document.hidden&&!raf){lastTime=performance.now();raf=requestAnimationFrame(frame)}}
function splash(force){const now=performance.now();if(now-lastSpawn<48)return;lastSpawn=now;const count=Math.min(w<700?26:40,Math.floor(force*2.8+8));for(let i=0;i<count;i++){const side=Math.random()<.5;const x=side?w*(.02+Math.random()*.25):w*(.75+Math.random()*.23);const launch=Math.min(h*.94,120+force*34);drops.push({x,y:h-9,vx:(side?1:-1)*(35+Math.random()*215)+(Math.random()-.5)*240,vy:-Math.sqrt(2*920*launch)*(.50+Math.random()*.65),r:1.2+Math.random()*4.4,life:3.4,bounces:0});}if(drops.length>200)drops.splice(0,drops.length-200)}
function inject(force){LiquidMotion.impulse(surface,pointer,force);splash(force)}
function step(){const target=5+energy*1.7;LiquidMotion.step(surface,STEP);energy*=.976;
for(let i=drops.length-1;i>=0;i--){const p=drops[i],ox=p.x,oy=p.y;p.vy+=920*STEP;p.vx*=.996;p.x+=p.vx*STEP;p.y+=p.vy*STEP;p.life-=STEP;
if(p.x<p.r||p.x>w-p.r){p.x=Math.max(p.r,Math.min(w-p.r,p.x));p.vx*=-.62}
if(p.bounces<2)for(const o of obstacles){const r=o.r;if(p.x>r.left&&p.x<r.right&&p.y>r.top-p.r&&p.y<r.bottom+p.r){if(oy<r.top&&p.vy>0){p.y=r.top-p.r;p.vy*=-.43;p.vx+=(Math.random()-.5)*140;p.bounces++;stains.push({el:o.el,x:(p.x-r.left)/r.width,y:0,r:p.r*1.5,age:0});break}else if(oy>r.bottom&&p.vy<0){p.y=r.bottom+p.r;p.vy*=-.38;p.bounces++;break}else if(ox<r.left||ox>r.right){p.vx*=-.58;p.x=ox;p.bounces++;break}}}
if(p.y>h-target){const k=Math.max(0,Math.min(nodes-1,Math.round(p.x/w*(nodes-1))));surface[k].v-=p.r*11;drops.splice(i,1)}else if(p.life<=0||p.x<-30||p.x>w+30)drops.splice(i,1)}
for(let i=stains.length-1;i>=0;i--){stains[i].age+=STEP;if(stains[i].age>2.8)stains.splice(i,1)}if(stains.length>35)stains.splice(0,stains.length-35)}
function draw(){ctx.clearRect(0,0,w,h);const base=h-(5+energy*1.7);const grad=ctx.createLinearGradient(0,base-65,0,h);grad.addColorStop(0,'#dc3044');grad.addColorStop(.35,'#ae1329');grad.addColorStop(1,'#670315');ctx.fillStyle=grad;ctx.beginPath();ctx.moveTo(0,h);ctx.lineTo(0,base+surface[0].y);for(let i=1;i<nodes;i++){const x=i*w/(nodes-1),px=(i-1)*w/(nodes-1);ctx.quadraticCurveTo(px,base+surface[i-1].y,(px+x)/2,base+(surface[i-1].y+surface[i].y)/2)}ctx.lineTo(w,base+surface[nodes-1].y);ctx.lineTo(w,h);ctx.closePath();ctx.fill();ctx.strokeStyle='#f9858470';ctx.lineWidth=1;ctx.stroke();
for(const p of drops){const stretch=Math.min(2.5,1+Math.abs(p.vy)/600);ctx.save();ctx.translate(p.x,p.y);ctx.rotate(-Math.atan2(p.vx,p.vy));const g=ctx.createRadialGradient(-p.r*.3,-p.r*.4,.1,0,0,p.r*1.4);g.addColorStop(0,'#ec6670');g.addColorStop(.28,'#bc233a');g.addColorStop(1,'#750519');ctx.fillStyle=g;ctx.beginPath();ctx.ellipse(0,0,p.r/Math.sqrt(stretch),p.r*stretch,0,0,Math.PI*2);ctx.fill();ctx.restore()}
for(const s of stains){const o=obstacles.find(o=>o.el===s.el);if(!o)continue;ctx.globalAlpha=Math.max(0,1-s.age/2.8)*.58;ctx.fillStyle='#a70e25';ctx.beginPath();ctx.ellipse(o.r.left+o.r.width*s.x,o.r.top+Math.min(s.age*8,20),s.r*(1+s.age*.15),s.r+s.age*3,0,0,Math.PI*2);ctx.fill()}ctx.globalAlpha=1}
function frame(t){raf=0;if(!enabled||document.hidden)return;acc+=Math.min((t-lastTime)/1000,.05);lastTime=t;while(acc>=STEP){step();acc-=STEP}draw();const moving=energy>.025||drops.length||stains.length||surface.some(s=>Math.abs(s.v)>.08||Math.abs(s.y)>.08);if(moving)raf=requestAnimationFrame(frame)}
addEventListener('scroll',()=>{const now=performance.now(),dy=scrollY-lastY,dt=Math.max(16,now-lastScroll),speed=Math.min(17,Math.abs(dy)/dt*3);lastY=scrollY;lastScroll=now;if(!enabled)return;energy=Math.min(14,energy+speed*.25);measure();if(speed>.3)inject(speed);wake()},{passive:true});
addEventListener('pointermove',e=>{pointer=Math.max(.02,Math.min(.98,e.clientX/w))},{passive:true});
addEventListener('resize',resize,{passive:true});window.visualViewport?.addEventListener('resize',resize,{passive:true});document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(raf);raf=0}else wake()});
toggles.forEach(toggle=>toggle.addEventListener('click',()=>{enabled=!enabled&&!reduce.matches;try{localStorage.setItem('carnivore-liquid',enabled?'on':'off')}catch{}state();if(enabled){energy=2;inject(3);wake()}else{cancelAnimationFrame(raf);raf=0;ctx.clearRect(0,0,w,h)}}));
reduce.addEventListener('change',()=>{enabled=!reduce.matches;state();wake()});state();resize();
const dialog=document.querySelector('#letter'),secret=document.querySelector('#secret');if(!dialog||!secret)return;secret.addEventListener('click',()=>dialog.showModal());dialog.querySelector('.close').addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close()}});
})();

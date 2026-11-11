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
 const canvas=document.querySelector('.hearth-fire'),ctx=canvas?.getContext('2d');
 if(!ctx)return;
 // A heat field rises through neighbouring cells; its palette gives fire soft, irregular edges.
 const w=180,h=120;canvas.width=w;canvas.height=h;
 let heat=new Float32Array(w*h),next=new Float32Array(w*h),fireRaf=0,visible=false,last=0;
 const pixels=ctx.createImageData(w,h);let sparks=[];
 function drawFire(t=0){
  fireRaf=0;if(document.hidden||!visible)return;
  if(t-last<40&&!reduced.matches){fireRaf=requestAnimationFrame(drawFire);return}last=t;
  for(let x=0;x<w;x++){
   const envelope=Math.pow(Math.sin(Math.PI*x/(w-1)),.7);
   const log=(Math.sin(x*.22+t*.0015)+Math.sin(x*.073-t*.002))*19;
   heat[(h-1)*w+x]=envelope*(145+Math.random()*110+log);
  }
  for(let y=0;y<h-1;y++)for(let x=1;x<w-1;x++){
   const drift=Math.round(Math.sin(y*.07+t*.001)*1.2),sx=Math.max(1,Math.min(w-2,x+drift));
   const below=Math.min(h-1,y+2);
   next[y*w+x]=Math.max(0,(heat[(y+1)*w+sx-1]+heat[(y+1)*w+sx]+heat[(y+1)*w+sx+1]+heat[below*w+sx])*.25-1.3-Math.random()*2.1);
  }
  next.set(heat.subarray((h-1)*w), (h-1)*w);[heat,next]=[next,heat];
  for(let i=0;i<heat.length;i++){
   const v=heat[i],k=i*4;
   pixels.data[k]=Math.min(255,v*3.5);pixels.data[k+1]=Math.max(0,Math.min(255,(v-75)*2.1));pixels.data[k+2]=Math.max(0,Math.min(245,(v-170)*2.7));pixels.data[k+3]=Math.max(0,Math.min(255,(v-24)*2.9));
  }
  ctx.putImageData(pixels,0,0);
  if(Math.random()>.45)sparks.push({x:w*(.2+Math.random()*.6),y:h*.86,vx:(Math.random()-.5)*.9,vy:1+Math.random()*1.1,life:45+Math.random()*30});
  ctx.fillStyle='#ffd58a';sparks=sparks.filter(p=>p.life-->0&&p.y>2);
  for(const p of sparks){p.x+=p.vx;p.y-=p.vy;ctx.globalAlpha=Math.min(1,p.life/30);ctx.fillRect(p.x,p.y,.6,1.2)}ctx.globalAlpha=1;
  if(!reduced.matches)fireRaf=requestAnimationFrame(drawFire);
 }
 function start(){if(visible&&!document.hidden&&!fireRaf){if(reduced.matches){for(let i=0;i<100;i++){last=0;drawFire(i*50)}}else fireRaf=requestAnimationFrame(drawFire)}}
 new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible)start();else{cancelAnimationFrame(fireRaf);fireRaf=0}},{rootMargin:'100px'}).observe(canvas);
 document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(fireRaf);cancelAnimationFrame(raf);fireRaf=raf=0}else{start();if(lamps.some(l=>l.amplitude))raf=requestAnimationFrame(animate)}});
 reduced.addEventListener('change',()=>{cancelAnimationFrame(fireRaf);fireRaf=0;start();if(!raf)raf=requestAnimationFrame(animate)});
})();

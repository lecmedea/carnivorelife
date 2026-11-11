'use strict';
(() => {
 const button=document.querySelector('.back-to-top');
 if(!button)return;
 const mobile=matchMedia('(max-width: 1100px)');
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 function update(){
  const distance=document.documentElement.scrollHeight-innerHeight;
  button.hidden=!mobile.matches||distance<=0||scrollY/distance<.7;
 }
 button.addEventListener('click',()=>scrollTo({top:0,behavior:reduced.matches?'instant':'smooth'}));
 addEventListener('scroll',update,{passive:true});
 addEventListener('resize',update,{passive:true});
 addEventListener('load',update);
 mobile.addEventListener('change',update);
 update();
})();

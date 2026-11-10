/* Bounded impulses, unconstrained spring positions: no flat wave ceiling. */
(function(root){
 'use strict';
 const motion={
  impulse(surface,pointer,force){
   const center=Math.floor(pointer*(surface.length-1));
   for(let i=0;i<surface.length;i++){
    const distance=i-center;
    const kick=Math.exp(-distance*distance/90)*Math.min(force*75,650)*Math.exp(-Math.max(0,-surface[i].y)/60);
    surface[i].v=900*Math.tanh((surface[i].v-kick)/900);
   }
  },
  step(surface,dt){
   const acceleration=surface.map((s,i)=>-42*s.y+130*(surface[Math.max(0,i-1)].y+surface[Math.min(surface.length-1,i+1)].y-2*s.y)-9*s.v);
   surface.forEach((s,i)=>{s.v+=acceleration[i]*dt;s.y+=s.v*dt});
  }
 };
 if(typeof module!=='undefined'&&module.exports)module.exports=motion;
 else root.LiquidMotion=motion;
})(typeof window==='undefined'?{}:window);

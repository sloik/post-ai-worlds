const phases = [
  ['RESEARCHERS / OBSERVERS', 'Understand<br>the world.', 'Ask better questions. Connect what we know. Turn experience into a clearer picture of what matters and what could come next.', 'KNOWLEDGE WORTH ACTING ON'],
  ['DESIGNERS / BUILDERS', 'Make something<br>useful.', 'Turn understanding into working software, tools and experiments. Different specialists bring their strengths to a concrete problem.', 'IDEAS THAT MEET REALITY'],
  ['CRITICS / EVALUATORS', 'Let reality<br>answer back.', 'Compare the outcome with the intention. Find failures, challenge assumptions and decide what is worth keeping.', 'EVIDENCE BEFORE CONFIDENCE'],
  ['CURATORS / INTEGRATORS', 'Carry the<br>learning forward.', 'Keep useful knowledge and accepted improvements. Preserve continuity so the next cycle starts with more than the last.', 'EXPERIENCE BECOMES CAPABILITY']
];
const tabs = [...document.querySelectorAll('[data-phase]')];
function selectPhase(index, focus = false) {
  tabs.forEach((tab, i) => { tab.setAttribute('aria-selected', String(i === index)); tab.tabIndex = i === index ? 0 : -1; });
  document.querySelector('#phase-role').textContent = phases[index][0];
  document.querySelector('#phase-title').innerHTML = phases[index][1];
  document.querySelector('#phase-description').textContent = phases[index][2];
  document.querySelector('#phase-output').textContent = 'OUTPUT → ' + phases[index][3];
  document.querySelector('#phase-content').setAttribute('aria-labelledby', 'phase-' + index);
  if (focus) tabs[index].focus();
}
tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectPhase(index));
  tab.addEventListener('keydown', event => {
    let next = index;
    if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
    else if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = tabs.length - 1;
    else return;
    event.preventDefault(); selectPhase(next, true);
  });
});
const canvas = document.querySelector('#neural');
const ctx = canvas.getContext('2d');
const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
let size = 660, angle = 0, frame;
const points = Array.from({length: 390}, (_, i) => {
  const y = 1 - (i / 389) * 2;
  const radius = Math.sqrt(1 - y * y);
  const phi = i * Math.PI * (3 - Math.sqrt(5));
  return {x:Math.cos(phi)*radius,y,z:Math.sin(phi)*radius};
});
function resize() { size = canvas.clientWidth; const dpr = Math.min(window.devicePixelRatio || 1,2); canvas.width = size*dpr; canvas.height = size*dpr; ctx.setTransform(dpr,0,0,dpr,0,0); }
function draw() {
  ctx.clearRect(0,0,size,size);
  const radius = size*.33;
  const projected = points.map(p => {
    const x=p.x*Math.cos(angle)-p.z*Math.sin(angle), z=p.x*Math.sin(angle)+p.z*Math.cos(angle);
    const scale=1+z*.15;
    return {x:size/2+x*radius*scale,y:size/2+p.y*radius*scale,z};
  });
  for(let i=0;i<projected.length;i++) {
    const a=projected[i];
    for(let j=i+1;j<projected.length;j++) {
      const b=projected[j], dx=a.x-b.x,dy=a.y-b.y,d=dx*dx+dy*dy;
      if(d<size*size*.0023 && Math.abs(a.z-b.z)<.25) { ctx.strokeStyle=`rgba(169,219,78,${(1-d/(size*size*.0023))*(.06+(a.z+1)*.1)})`;ctx.lineWidth=.6;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke(); }
    }
    ctx.fillStyle=a.z>.4?'rgba(213,255,103,.9)':'rgba(90,162,110,.45)';ctx.beginPath();ctx.arc(a.x,a.y,a.z>.5?1.7:1,0,Math.PI*2);ctx.fill();
  }
  if(!motion.matches && !document.hidden) { angle+=.0016; frame=requestAnimationFrame(draw); }
}
function restart(){cancelAnimationFrame(frame);draw();}
resize(); draw();
window.addEventListener('resize',()=>{resize();restart();});
document.addEventListener('visibilitychange',restart);
motion.addEventListener('change',restart);

// The curve is an editorial illustration, never a capability forecast.
const eras = [
 {t:0,tag:'THE FOUNDATION / 1947',title:'A small switch. An enormous beginning.',copy:'The transistor emerged at Bell Labs in 1947. A new way to control electrical signals became a foundation for modern computing.'},
 {t:.36,tag:'THE CONNECTED WORLD',title:'More connections. More possibility.',copy:'Computing and networks changed how knowledge travels and how people build together. Each layer made new kinds of work possible.'},
 {t:.66,tag:'THE PRESENT / 2026',title:'We are inside the story.',copy:'AI is becoming part of how we research, design and build. Omnicorp is our way of preparing to participate in what comes next.'},
 {t:1,tag:'A HYPOTHETICAL HORIZON / NO DATE',title:'When the curve becomes a question.',copy:'The singularity imagines technological change accelerating beyond our ability to predict it. It is a possibility to think about, not an established destination or a scheduled event.'}
];
const eraButtons = [...document.querySelectorAll('[data-era]')];
eraButtons.forEach((button,index)=>button.addEventListener('click',()=>{
 const era=eras[index];
 eraButtons.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));
 document.querySelector('#era-tag').textContent=era.tag;
 document.querySelector('#era-title').textContent=era.title;
 document.querySelector('#era-copy').textContent=era.copy;
 const marker=document.querySelector('#explore-point');
 marker.setAttribute('cx',60+880*era.t);
 marker.setAttribute('cy',390-330*(Math.exp(4*era.t)-1)/(Math.exp(4)-1));
 if(!motion.matches) document.querySelector('.era-story').animate([{opacity:.35,transform:'translateY(7px)'},{opacity:1,transform:'translateY(0)'}],{duration:450,easing:'ease-out'});
}));
const mapNodes=[...document.querySelectorAll('.loop-map .node')];
mapNodes[0].classList.add('active');
tabs.forEach((tab,index)=>tab.addEventListener('click',()=>highlightNode(index)));
document.querySelector('.phase-tabs').addEventListener('keydown',()=>{
 const selected=tabs.findIndex(tab=>tab.getAttribute('aria-selected')==='true');highlightNode(selected);
});
function highlightNode(index){
 mapNodes.forEach((node,i)=>node.classList.toggle('active',i===index));
 if(!motion.matches) document.querySelector('#phase-content').animate([{opacity:.4,transform:'translateY(6px)'},{opacity:1,transform:'translateY(0)'}],{duration:400,easing:'ease-out'});
}
if('IntersectionObserver' in window){
 const revealObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{
  if(entry.isIntersecting){entry.target.classList.add('is-visible');if(entry.target.classList.contains('growth-console')) entry.target.classList.add('curve-enter');revealObserver.unobserve(entry.target);}
 }),{threshold:.08});
 document.querySelectorAll('.section-heading,.vision-layout,.statement,.system-title,.loop-map,.phase-panel,.frontier-card,.manifesto-heading,.principles article,.contact h2,.growth-console,.trajectory-heading').forEach((element,index)=>{
  if(!motion.matches){element.classList.add('reveal-pending');element.style.setProperty('--reveal-delay',`${index%3*70}ms`);}
  revealObserver.observe(element);
 });
}
if(window.matchMedia('(hover:hover) and (pointer:fine)').matches){
 document.querySelectorAll('.frontier-card').forEach(card=>{
  card.addEventListener('pointermove',event=>{if(motion.matches)return;const rect=card.getBoundingClientRect();card.style.setProperty('--tilt-x',`${((event.clientX-rect.left)/rect.width-.5)*5}deg`);card.style.setProperty('--tilt-y',`${-((event.clientY-rect.top)/rect.height-.5)*5}deg`);});
  card.addEventListener('pointerleave',()=>{card.style.setProperty('--tilt-x','0deg');card.style.setProperty('--tilt-y','0deg');});
 });
}

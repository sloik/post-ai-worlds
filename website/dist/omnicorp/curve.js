(()=>{
 const data=document.querySelector('#curve-data');if(!data)return;
 const records=JSON.parse(data.textContent),controls=[...document.querySelectorAll('[data-curve-event]')];
 const reduced=()=>matchMedia('(prefers-reduced-motion:reduce)').matches;
 const story=document.querySelector('.curve-event-story');
 function select(id,animate=true){const event=records.find(x=>x.id===id);if(!event)return false;
 controls.forEach(c=>c.setAttribute('aria-pressed',String(c.dataset.curveEvent===id)));
 document.querySelector('#curve-event-date').textContent=event.date;
 for(const [target,field] of [['title','title'],['claim','claim'],['reading','interpretation'],['limit','limit']])document.querySelector('#curve-event-'+target).textContent=event[field];
 document.querySelector('#curve-event-source').href=event.source;
 document.querySelector('#curve-event-source').textContent=event.source_label||'Read the primary source ↗';
 const permalink=story.querySelector('.curve-permalink');if(permalink)permalink.href='#curve-'+id;
 if(animate&&!reduced())story.animate([{opacity:.4,transform:'translateY(5px)'},{opacity:1,transform:'translateY(0)'}],{duration:350,easing:'ease-out'});
 return true;
 }
 // Deep links: #curve-<id> selects a dated milestone or a conditional accelerator (future-<question>).
 function fromHash(){
  const hash=decodeURIComponent(location.hash.slice(1));
  if(!hash.startsWith('curve-')||!controls.some(c=>c.dataset.curveEvent===hash.slice(6)))return false;
  select(hash.slice(6));
  story.scrollIntoView({block:'center',behavior:reduced()?'auto':'smooth'});
  return true;
 }
 const choose=id=>{select(id);history.replaceState(null,'','#curve-'+id);};
 controls.forEach(c=>{c.addEventListener('click',()=>choose(c.dataset.curveEvent));if(c.tagName.toLowerCase()==='g')c.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();choose(c.dataset.curveEvent);}});});
 addEventListener('hashchange',fromHash);
 if(!fromHash())select('opus-45',false);
})();

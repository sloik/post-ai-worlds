(()=>{
 const data=document.querySelector('#curve-data');if(!data)return;
 const records=JSON.parse(data.textContent),controls=[...document.querySelectorAll('[data-curve-event]')];
 function select(id,animate=true){const event=records.find(x=>x.id===id);if(!event)return;
 controls.forEach(c=>c.setAttribute('aria-pressed',String(c.dataset.curveEvent===id)));
 document.querySelector('#curve-event-date').textContent=event.date;
 for(const [target,field] of [['title','title'],['claim','claim'],['reading','interpretation'],['limit','limit']])document.querySelector('#curve-event-'+target).textContent=event[field];
 document.querySelector('#curve-event-source').href=event.source;
 document.querySelector('#curve-event-source').textContent=event.source_label||'Read the primary source ↗';
 if(animate&&!matchMedia('(prefers-reduced-motion:reduce)').matches)document.querySelector('.curve-event-story').animate([{opacity:.4,transform:'translateY(5px)'},{opacity:1,transform:'translateY(0)'}],{duration:350,easing:'ease-out'});
 }
 controls.forEach(c=>{c.addEventListener('click',()=>select(c.dataset.curveEvent));if(c.tagName.toLowerCase()==='g')c.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();select(c.dataset.curveEvent);}});});
 select('opus-45',false);
})();

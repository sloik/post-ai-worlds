const snapshot=JSON.parse(document.querySelector('#observatory-data').textContent);
const buttons=[...document.querySelectorAll('[data-event]')];
const reduced=matchMedia('(prefers-reduced-motion:reduce)');
const detail=document.querySelector('.evidence-detail');
function showEvent(index,animate=false){
 const event=snapshot.events[index];
 buttons.forEach(button=>button.setAttribute('aria-pressed',String(Number(button.dataset.event)===index)));
 for(const field of ['title','evidence','claim','interpretation','limit','comparison','direction'])document.querySelector('#event-'+field).textContent=event[field];
 document.querySelector('#event-date').textContent='EVENT / '+event.date;
 document.querySelector('#event-reviewed').textContent='REVIEW / '+event.assessed_on;
 const source=document.querySelector('#event-source');source.href=event.source;source.textContent=event.source_title+' ↗';
 detail.querySelector('.event-permalink').href='#event-'+event.id;
 const related=document.querySelector('#event-questions');related.replaceChildren();
 event.affects.forEach(id=>{const q=snapshot.questions.find(q=>q.id===id),a=document.createElement('a');a.href='#'+id;a.textContent='Related question: '+q.title+' ↗';related.append(a);});
 if(animate&&!reduced.matches)detail.animate([{opacity:.4,transform:'translateY(7px)'},{opacity:1,transform:'translateY(0)'}],{duration:400,easing:'ease-out'});
}
// Deep links: #event-<id> selects a reviewed event by its stable id, not its list position.
function eventFromHash(){
 const hash=decodeURIComponent(location.hash.slice(1));
 if(!hash.startsWith('event-'))return false;
 const index=snapshot.events.findIndex(event=>event.id===hash.slice(6));
 if(index<0)return false;
 showEvent(index,true);
 detail.scrollIntoView({block:'start',behavior:reduced.matches?'auto':'smooth'});
 return true;
}
buttons.forEach(button=>button.addEventListener('click',()=>{
 const index=Number(button.dataset.event);
 showEvent(index,true);
 history.replaceState(null,'','#event-'+snapshot.events[index].id);
}));
addEventListener('hashchange',eventFromHash);
if(!eventFromHash())showEvent(snapshot.events.length-1);

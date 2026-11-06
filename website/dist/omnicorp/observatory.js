const snapshot=JSON.parse(document.querySelector('#observatory-data').textContent);
const buttons=[...document.querySelectorAll('[data-event]')];
const reduced=matchMedia('(prefers-reduced-motion:reduce)');
function showEvent(index,animate=false){
 const event=snapshot.events[index];
 buttons.forEach(button=>button.setAttribute('aria-pressed',String(Number(button.dataset.event)===index)));
 for(const field of ['title','evidence','claim','interpretation','limit','comparison','direction'])document.querySelector('#event-'+field).textContent=event[field];
 document.querySelector('#event-date').textContent='EVENT / '+event.date;
 document.querySelector('#event-reviewed').textContent='REVIEW / '+event.assessed_on;
 const source=document.querySelector('#event-source');source.href=event.source;source.textContent=event.source_title+' ↗';
 const related=document.querySelector('#event-questions');related.replaceChildren();
 event.affects.forEach(id=>{const q=snapshot.questions.find(q=>q.id===id),a=document.createElement('a');a.href='#'+id;a.textContent='Related question: '+q.title+' ↗';related.append(a);});
 if(animate&&!reduced.matches)document.querySelector('.evidence-detail').animate([{opacity:.4,transform:'translateY(7px)'},{opacity:1,transform:'translateY(0)'}],{duration:400,easing:'ease-out'});
}
buttons.forEach(button=>button.addEventListener('click',()=>showEvent(Number(button.dataset.event),true)));
showEvent(snapshot.events.length-1);

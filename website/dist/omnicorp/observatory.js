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

function initEventTooltips() {
    const tooltip = document.createElement('div');
    tooltip.className = 'evidence-tooltip';
    // The same title is already the button's accessible name.
    tooltip.setAttribute('aria-hidden', 'true');
    document.body.append(tooltip);

    let hoveredDot = null;
    let focusedDot = null;

    function positionTooltip() {
        const dot = hoveredDot || focusedDot;
        if (!dot) {
            tooltip.hidden = true;
            return;
        }

        const viewport = document.documentElement;
        const anchor = dot.getBoundingClientRect();
        if (anchor.bottom <= 0 || anchor.top >= viewport.clientHeight) {
            tooltip.hidden = true;
            return;
        }

        const inset = 12;
        const gap = 8;
        const center = anchor.left + anchor.width / 2;
        tooltip.textContent = snapshot.events[Number(dot.dataset.event)].title;
        tooltip.hidden = false;
        const {width, height} = tooltip.getBoundingClientRect();
        const left = Math.max(inset, Math.min(center - width / 2, viewport.clientWidth - width - inset));
        const above = anchor.top - height - gap;
        const below = anchor.bottom + gap;
        const placeBelow = above < inset && below + height <= viewport.clientHeight - inset;
        const top = Math.max(inset, Math.min(placeBelow ? below : above, viewport.clientHeight - height - inset));
        tooltip.style.left = `${left}px`;
        tooltip.style.top = `${top}px`;
        tooltip.style.setProperty('--tip-arrow', `${Math.max(12, Math.min(center - left, width - 12))}px`);
        tooltip.dataset.side = placeBelow ? 'below' : 'above';
    }

    function dismissTooltip() {
        hoveredDot = null;
        focusedDot = null;
        positionTooltip();
    }

    for (const dot of document.querySelectorAll('.evidence-dot')) {
        dot.addEventListener('pointerenter', event => {
            if (event.pointerType === 'touch') return;
            hoveredDot = dot;
            positionTooltip();
        });
        dot.addEventListener('pointerleave', event => {
            if (hoveredDot !== dot || event.relatedTarget === tooltip) return;
            hoveredDot = null;
            positionTooltip();
        });
        dot.addEventListener('focus', () => {
            if (!dot.matches(':focus-visible')) return;
            focusedDot = dot;
            positionTooltip();
        });
        dot.addEventListener('blur', () => {
            if (focusedDot !== dot) return;
            focusedDot = null;
            positionTooltip();
        });
        dot.addEventListener('click', dismissTooltip);
    }

    tooltip.addEventListener('pointerleave', event => {
        if (event.relatedTarget === hoveredDot) return;
        hoveredDot = null;
        positionTooltip();
    });
    document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && !tooltip.hidden) dismissTooltip();
    });
    window.addEventListener('scroll', positionTooltip, {capture: true, passive: true});
    window.addEventListener('resize', positionTooltip);
}

initEventTooltips();

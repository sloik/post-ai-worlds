const filterButtons=[...document.querySelectorAll('[data-filter]')];
const search=document.querySelector('#paper-search');
const papers=[...document.querySelectorAll('.paper-grid .paper-card')];
let activeGroup='all';
function filterPapers(){
 const query=(search?.value||'').trim().toLocaleLowerCase();let count=0;
 papers.forEach(paper=>{const visible=(activeGroup==='all'||paper.dataset.group===activeGroup)&&(paper.dataset.search||paper.textContent).toLocaleLowerCase().includes(query);paper.hidden=!visible;if(visible)count++;});
 const status=document.querySelector('.result-count');if(status)status.textContent=`${count} ${count===1?'paper':'papers'}`;
 const empty=document.querySelector('.empty-results');if(empty)empty.hidden=count>0;
}
filterButtons.forEach(button=>button.addEventListener('click',()=>{activeGroup=button.dataset.filter;filterButtons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));filterPapers();}));
search?.addEventListener('input',filterPapers);
document.querySelector('.print-paper')?.addEventListener('click',()=>window.print());
const progress=document.querySelector('.reading-progress');
let pending=false;
function updateProgress(){const total=document.documentElement.scrollHeight-innerHeight;progress.style.transform=`scaleX(${total>0?scrollY/total:0})`;pending=false;}
addEventListener('scroll',()=>{if(!pending){requestAnimationFrame(updateProgress);pending=true;}},{passive:true});
addEventListener('resize',updateProgress);updateProgress();
if('IntersectionObserver' in window){
 const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting){document.querySelectorAll('.article-toc nav a').forEach(a=>a.classList.toggle('current',a.hash==='#'+entry.target.id));}});},{rootMargin:'-15% 0px -60% 0px'});
 document.querySelectorAll('.paper-body>section[id]').forEach(section=>observer.observe(section));
}

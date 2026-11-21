(()=>{
 // Copy-link controls: put the fragment in the address bar without jumping, then copy the full URL.
 document.addEventListener('click',ev=>{
  const a=ev.target.closest('a[data-permalink]');if(!a)return;
  ev.preventDefault();
  history.replaceState(null,'',a.getAttribute('href'));
  const url=location.href,text=a.textContent,label=a.getAttribute('aria-label');
  const show=message=>{a.textContent=message;if(label)a.setAttribute('aria-label',message);clearTimeout(a._permalinkTimer);a._permalinkTimer=setTimeout(()=>{a.textContent=text;if(label)a.setAttribute('aria-label',label);},1800);};
  if(navigator.clipboard&&window.isSecureContext)navigator.clipboard.writeText(url).then(()=>show('Link copied ✓'),()=>show('Link is in the address bar'));
  else show('Link is in the address bar');
 });
})();

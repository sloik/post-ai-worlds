"""Attach reviewed, selectable milestones to the conceptual growth curve."""
import html,json,math,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'dist/omnicorp';e=html.escape
d=json.loads((ROOT/'content/observatory.json').read_text());events={x['id']:x for x in d['events']}
p=OUT/'index.html';home=p.read_text();start=home.index('<div class="growth-plot">');end=home.index('<div class="growth-controls"',start)
plot=home[start:end]
# Remove a prior generated selection panel and pins before regenerating.
if '<!-- curve-controls -->' in plot:plot=plot.split('<!-- curve-controls -->')[0]
plot=re.sub(r'<g id="curve-milestone-pins">.*?</g><!-- end-curve-pins -->','',plot,flags=re.S)
plot=re.sub(r'<p class="curve-accuracy-note">.*?</p>','',plot,flags=re.S)
plot=plot.replace('<div class="growth-plot">','<div class="growth-plot"><p class="curve-accuracy-note"><strong>How accurate is this position?</strong> The date is factual; the height is schematic. No positional confidence percentage has been estimated. Use the dated milestone forecasts below for probabilities we can actually resolve.</p>')
pins='<g id="curve-milestone-pins">'
for m in d['curve_milestones']:
 t=m['position'];x=60+880*t;y=390-330*(math.exp(4*t)-1)/(math.exp(4)-1)
 color='#5cddd2' if m['event_id']=='opus-45' else '#d9ff43'
 pins+=f'<g class="curve-event-pin" data-curve-event="{m["event_id"]}" tabindex="0" role="button" aria-label="{e(m["label"]+": "+events[m["event_id"]]["date"],quote=True)}" aria-pressed="false"><circle cx="{x:.2f}" cy="{y:.2f}" r="17" fill="transparent"/><circle class="milestone-dot" cx="{x:.2f}" cy="{y:.2f}" r="5" fill="{color}" stroke="#09110b" stroke-width="1"/>'
 if m['event_id'] in ['chatgpt','opus-45']:
  pins+=f'<path d="M{x:.2f},{y-8:.2f}v-65" stroke="{color}" fill="none" opacity=".6"/><text class="curve-pin-label" x="{x:.2f}" y="{y-83:.2f}" text-anchor="middle" fill="{color}">{e(m["label"])}</text>'
 pins+='</g>'
for n,a in enumerate(d['curve_accelerators'],1):
 t=a['position'];x=60+880*t;y=390-330*(math.exp(4*t)-1)/(math.exp(4)-1)
 pins+=f'<g class="curve-event-pin future-pin" data-curve-event="future-{a["question_id"]}" tabindex="0" role="button" aria-label="Conditional accelerator {n}: {e(a["label"][5:],quote=True)}" aria-pressed="false"><circle cx="{x:.2f}" cy="{y:.2f}" r="20" fill="transparent"/><circle class="milestone-dot" cx="{x:.2f}" cy="{y:.2f}" r="13" fill="#0b2524" stroke="#5cddd2" stroke-width="1.5" stroke-dasharray="3 3"/><text x="{x:.2f}" y="{y+5:.2f}" text-anchor="middle" fill="#8bf1e6" style="font:14px monospace">{n}</text></g>'
pins+='</g><!-- end-curve-pins -->' 
plot=plot.replace('</svg>',pins+'</svg>')
if 'Four numbered future pins' not in plot:plot=plot.replace('Positions and slope are conceptual, not measured data or a forecast.','Positions and slope are conceptual, not measured data or a forecast. Four numbered future pins represent conditional acceleration mechanisms, not observed events.')
initial=events['opus-45']
controls='<!-- curve-controls --><div class="curve-selectors" role="group" aria-label="Explore dated milestones">'
for m in d['curve_milestones']:
 controls+=f'<button type="button" data-curve-event="{m["event_id"]}" aria-pressed="{str(m["event_id"]==initial["id"]).lower()}"><strong>{e(m["label"])}</strong><span>{e(m["subtitle"])}</span></button>'
controls+='</div><div class="curve-future-heading"><p class="eyebrow">WHAT COULD MAKE THE NEXT CYCLE FASTER?</p><p>Conditional accelerators / not observed events. Numbers link the future pins to the cards; they do not specify timing, sequence or measured impact.</p></div><div class="curve-selectors curve-future-selectors" role="group" aria-label="Explore potential accelerators">'
future_records=[]
questions={q['id']:q for q in d['questions']}
for a in d['curve_accelerators']:
 q=questions[a['question_id']];ident='future-'+a['question_id']
 controls+=f'<button type="button" data-curve-event="{ident}" aria-pressed="false"><strong>{e(a["label"])}</strong><span>Conditional · {round(q["prob"]*100)}% milestone forecast by {q["deadline"]}</span></button>'
 future_records.append(dict(id=ident,date='CONDITIONAL ACCELERATOR / NOT YET OBSERVED',title=a['label'][5:],claim=a['mechanism'],interpretation='What would count: '+q['criteria'],limit=a['brake']+' The milestone probability is not a probability that this mechanism accelerates the curve.',source='/omnicorp/observatory/#'+q['id'],source_label='Read the milestone forecast & opposing cases ↗'))
controls+=f'''</div><article class="curve-event-story" aria-live="polite" aria-atomic="true"><div><span id="curve-event-date" class="eyebrow">{initial['date']}</span><h3 id="curve-event-title">{e(initial['title'])}</h3></div><div><p id="curve-event-claim">{e(initial['claim'])}</p><p id="curve-event-reading">{e(initial['interpretation'])}</p><p class="curve-event-limit" id="curve-event-limit">{e(initial['limit'])}</p><a id="curve-event-source" class="text-link" href="{e(initial['source'],quote=True)}">Read the primary source ↗</a></div></article><p class="chart-note">Conceptual illustration. Milestone dates are factual anchors; their horizontal spacing and height are editorial, not a calendar or capability scale. The singularity is hypothetical and undated. <a href="https://www.nokia.com/bell-labs/about/history/">Transistor origin: Bell Labs, 1947 ↗</a></p><script id="curve-data" type="application/json">{json.dumps(d['events']+future_records,ensure_ascii=False).replace('<',chr(92)+'u003c')}</script>'''
fragment=plot+controls
(ROOT/'content/curve-fragment.html').write_text(fragment)
# Preserve the original outer console and section closing tags.
last=home.index('\n</div></section>',end)
home=home[:start]+fragment+'<div class="growth-controls" hidden></div>'+home[last:]
if 'src="curve.js"' not in home:home=home.replace('</head>','<script defer src="curve.js"></script></head>')
p.write_text(home)
print('Built five dated milestones and four conditional accelerators.')

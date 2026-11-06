"""Build a public, reviewed evidence snapshot; no automatic forecasting."""
import html,json,re
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'dist'/'omnicorp';e=html.escape
d=json.loads((ROOT/'content/observatory.json').read_text())
library=(OUT/'field-notes/index.html').read_text();home=(OUT/'index.html').read_text()
header=re.search(r'<header>.*?</header>',library,re.S).group().replace('aria-current="page"','aria-current="false"').replace('href="/omnicorp/observatory/"','href="/omnicorp/observatory/" aria-current="page"');footer=re.search(r'<footer>.*?</footer>',library,re.S).group()
plot=(ROOT/'content/curve-fragment.html').read_text()
p=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Observatory — Omnicorp</title><meta name="description" content="A growth horizon, reviewed events and testable forecast questions."><link rel="stylesheet" href="/omnicorp/style.css"><link rel="stylesheet" href="/omnicorp/publications.css"><link rel="stylesheet" href="/omnicorp/observatory.css"><script defer src="/omnicorp/observatory.js"></script><script defer src="/omnicorp/curve.js"></script></head><body class="publication-page observatory-page"><a class="skip" href="#main">Skip to content</a>{header}<main id="main"><section class="section observatory-hero"><div class="section-heading"><p class="eyebrow">THE OMNICORP OBSERVATORY</p><span class="mono dim">REVIEWED / {date.fromisoformat(d["reviewed_on"]).strftime("%d %b %Y").upper()}</span></div><h1>The world moves.<br><span>We update.</span></h1><p class="observatory-deck">From the transistor moment to an open horizon.<br>Track the evidence. Challenge the expectations.</p><div class="observatory-console"><div class="console-top mono"><span><i class="signal"></i> TODAY / SCHEMATIC POSITION</span><span>SINGULARITY: AN OPEN QUESTION</span></div>{plot}<div class="horizon-reading"><h2>Today is dated.<br><span>The height is schematic.</span></h2><p>{e(d['summary'])} The dot’s height was chosen for the illustration, not estimated from data. Its accuracy has no defined probability. The curves are scenarios, not confidence bands. The percentages below refer only to specific dated forecasts.</p></div></div><div class="observatory-links"><a href="#evidence">Explore the events ↓</a><a href="#questions">Forecast questions ↓</a><a href="#revisions">What changed ↓</a></div></section><section class="section" id="evidence"><div class="section-heading"><p class="eyebrow">01 / WHAT CHANGED?</p><span class="mono dim">EVENT ≠ ASSESSMENT ≠ FORECAST</span></div><h2>Read the signals.<br><span>Keep the counterevidence.</span></h2><p class="observatory-deck">A selected evidence timeline from public access to mathematical discovery. Dates and our assessments are distinct. Related reports retain their source lineage: a sequel is not another independent discovery. Public proof corrections stay visible alongside advances.</p><div class="evidence-workspace"><div><div class="evidence-rail mono"><span>2022</span><span>NOV 2026 / REVIEW SNAPSHOT</span></div>'''
for lane in ['Public access','Scientific work','Autonomous work','Real-world usefulness','Cumulative improvement','Physical work']:
 p+=f'<div class="evidence-lane {"scientific" if lane=="Scientific work" else ""}"><span>{e(lane)}</span><div class="lane-track">'
 events=[(i,x) for i,x in enumerate(d['events']) if x['lane']==lane]
 if not events:p+='<small>NO SELECTED OBSERVATION</small>'
 # Greedy row packing: events never share a row closer than 11% of the track (dot plus side label).
 rows_end=[];placed=[]
 for i,x in events:
  pos=8+(date.fromisoformat(x['date'])-date(2022,1,1)).days/(date(2026,11,5)-date(2022,1,1)).days*84
  row=next((r for r,end in enumerate(rows_end) if pos-end>=11),None)
  if row is None: rows_end.append(pos); row=len(rows_end)-1
  else: rows_end[row]=pos
  placed.append((i,x,pos,row))
 track_open=p.rindex('<div class="lane-track">')
 need=(6 if lane=='Scientific work' else 14)+len(rows_end)*30+4
 base=160 if lane=='Scientific work' else 78
 if need>base: p=p[:track_open]+f'<div class="lane-track" style="height:{need}px">'+p[track_open+len('<div class="lane-track">'):]
 for i,x,pos,row in placed:
  top=6+row*30 if lane=='Scientific work' else (29 if len(rows_end)==1 else 14+row*30)
  p+=f'<button data-event="{i}" class="evidence-dot {x["motion"]}" style="left:{pos:.2f}%;top:{top}px" aria-pressed="false" aria-label="{e(x["title"],quote=True)}"><span>{x["date"][5:]}</span></button>'
 p+='</div></div>'
p+='<p class="evidence-key mono">ACID / CAPABILITY SIGNAL · AMBER / LIMIT · CYAN / MIXED</p><div class="event-list" role="group" aria-label="Select a reviewed event">'
for i,x in enumerate(d['events']):p+=f'<button data-event="{i}" aria-pressed="false"><time>{x["date"]}</time><span>{e(x["title"])}</span><b>↗</b></button>'
p+='</div></div><article class="evidence-detail" aria-live="polite" aria-atomic="true"><p class="eyebrow" id="event-evidence"></p><h3 id="event-title"></h3><p class="event-meta mono"><span id="event-date"></span><br><span id="event-reviewed"></span></p><span id="event-direction" class="direction-label"></span><dl>'
for field,label in [('claim','What the source reports'),('interpretation','Our reading'),('limit','What it does not establish'),('comparison','Compared with expectations')]:p+=f'<dt>{label}</dt><dd id="event-{field}"></dd>'
p+='</dl><a id="event-source" class="text-link" href="#">Primary source ↗</a><div id="event-questions"></div></article></div></section><section class="section forecast-section" id="questions"><div class="section-heading"><p class="eyebrow">02 / MAKE EXPECTATIONS TESTABLE</p><span class="mono dim">SUPERFORECASTING / QUESTION DESIGN</span></div><h2>Smaller questions.<br><span>Sharper updates.</span></h2><p class="observatory-deck">How far to singularity has no agreed measuring stick. These registered milestone forecasts make parts of the ambition resolvable. Each percentage is our subjective chance of a qualifying new public record by its deadline—not confidence that the curve position is accurate.</p><div class="forecast-grid">'
for i,q in enumerate(d['questions']):
 percent=round(q['prob']*100)
 views=' / '.join(str(round(x*100))+'%' for x in q['views'])
 p+=f'<article class="forecast-card" id="{q["id"]}"><div class="forecast-card-top mono"><span>Q{i+1:02} / {e(q["lane"])}</span><span>BY {q["deadline"]}</span></div><h3>{e(q["title"])}</h3><div class="forecast-number"><strong>{percent}<span>%</span></strong><div>CHANCE OF YES<small>New public record by {q["deadline"]}<br>Issued 5 November 2026 · open forecast</small></div></div><p class="forecast-precision">Subjective estimate, not an empirical base rate or a singularity probability.</p><div class="forecast-cases"><div><h4>Why we think this may happen</h4><ul>'+''.join('<li>'+e(x)+'</li>' for x in q['why_right'])+'</ul></div><div><h4>Why we might be wrong</h4><ul>'+''.join('<li>'+e(x)+'</li>' for x in q['why_wrong'])+'</ul></div></div><details><summary>Exact outcome, timeframe & update signals +</summary><dl>'
 for field,label in [('criteria','What counts as YES'),('resolver','Resolution source & edge cases')]:p+=f'<dt>{label}</dt><dd>{e(q[field])}</dd>'
 p+=f'<dt>Observation window</dt><dd>6 November 2026 through {q["deadline"]} at 23:59 UTC. Criteria version 1.0. Previously published cases do not count as new outcomes.</dd>'
 for field,label in [('up_trigger','Evidence that would raise the probability'),('down_trigger','Evidence that would lower it')]:
  trigger=q[field];p+=f'<dt>{label}</dt><dd>{e(trigger["description"])} Proposed likelihood-ratio multiplier: {trigger["lr"]}. This is an update rule for review, not an automatic score.</dd>'
 p+='</dl></details><details><summary>How we estimated this +</summary><dl>'
 for field,label in [('prior_basis','One contributing analyst’s starting point'),('reference_class','Reference-class limitations'),('method','Combining perspectives'),('confidence_note','Limits of confidence')]:p+=f'<dt>{label}</dt><dd>{e(q[field])}</dd>'
 p+=f'<dt>Separately elicited views</dt><dd>{views}. The spread reflects analyst disagreement, not a confidence interval. Shared model-family and source dependencies limit the ensemble.</dd><dt>Current record</dt><dd>Forecast #{q["forecast_id"]} · initial estimate {percent}% · not yet resolved or scored.</dd></dl><p class="eyebrow">PRIMARY EVIDENCE</p><ul class="forecast-sources">'
 for source in q['sources']:p+=f'<li><a href="{e(source["url"],quote=True)}">{e(source["title"])} ↗</a></li>'
 p+='</ul></details></article>'
p+='</div><div class="calibration-note"><span class="mono">FORECASTING, NOT DECORATION</span><p>Before publishing a number: define the reference class, weigh evidence for and against, compare separately elicited assessments, record the probability and name its update triggers. At resolution: score it and retain the lesson. A Brier score measures accuracy on those questions; it does not validate a singularity-distance scale.</p><p>Four forecasts were registered on 5 November 2026 with fixed prospective criteria, probabilities and opposing cases. No resolved outcomes are available for this series, so calibration is not yet measured. Earlier internal forecasts remain separate. This is a reviewed snapshot, not automatic monitoring.</p><a class="text-link" href="https://github.com/sloik/superforecasting">The superforecasting playbook ↗</a><br><a class="text-link" href="/omnicorp/observatory/forecast-records.json">Download the dated forecast records ↗</a></div></section><section class="section" id="revisions"><div class="section-heading"><p class="eyebrow">03 / KEEP THE RECEIPTS</p><span class="mono dim">WHAT CHANGED / AND WHY</span></div><h2>Revision is<br><span>part of the work.</span></h2>'
for r in d['reviews']:p+=f'<article class="revision-entry"><time class="mono">{r["date"]}</time><div><h3>{e(r["title"])}</h3><p>{e(r["reason"])}</p><span class="mono">INITIAL FORECASTS ISSUED: {r.get("initial_forecasts",0)} · PROBABILITY REVISIONS: {r["forecast_changes"]}</span></div></article>'
p+='''<div class="review-method"><p class="eyebrow">HOW THE POSITION CHANGES</p><ol><li><strong>Record the event.</strong> Retain its date, source and research lineage.</li><li><strong>Test the criterion.</strong> Distinguish a new capability from another announcement of the same result.</li><li><strong>Revise a registered forecast.</strong> Explain the evidence, retain the prior and consider both directions. No change is a valid conclusion.</li><li><strong>Show the revision.</strong> Keep the registered initial probability and every subsequent revision visible. Failed expectations and retractions can move the outlook back; calendar time never moves backward.</li></ol><p>Demonstrated milestones change our picture of the future. They are not a percentage of the journey to singularity.</p></div><a class="button" href="/omnicorp/field-notes/">Read the thinking behind it <span>↗</span></a></section></main>'''
p+=footer.replace('</body></html>','')+'<script id="observatory-data" type="application/json">'+json.dumps(d,ensure_ascii=False).replace('<','\\u003c')+'</script></body></html>'
# Default evidence remains readable if JavaScript is unavailable.
initial=d['events'][-1]
for field in ['title','evidence','claim','interpretation','limit','comparison','direction']:
 p=re.sub(r'(<[^>]+id="event-'+field+r'"[^>]*>).*?(</[^>]+>)',lambda m:m[1]+e(initial[field])+m[2],p)
p=p.replace('<span id="event-date"></span>','<span id="event-date">EVENT / '+initial['date']+'</span>').replace('<span id="event-reviewed"></span>','<span id="event-reviewed">REVIEW / '+initial['assessed_on']+'</span>')
p=p.replace('<a id="event-source" class="text-link" href="#">Primary source ↗</a>','<a id="event-source" class="text-link" href="'+e(initial['source'],quote=True)+'">'+e(initial['source_title'])+' ↗</a>')
fallback='<noscript><section class="section"><h2>All reviewed events</h2>'
for event in d['events']:
 fallback+='<details><summary>'+e(event['date']+' / '+event['title'])+'</summary>'
 for field in ['claim','interpretation','limit','comparison']:fallback+='<p>'+e(event[field])+'</p>'
 fallback+='<a href="'+e(event['source'],quote=True)+'">'+e(event['source_title'])+' ↗</a></details>'
fallback+='</section></noscript>'
p=p.replace('</main>',fallback+'</main>')

(OUT/'observatory').mkdir(exist_ok=True);(OUT/'observatory/index.html').write_text(p)
print('Built Observatory.')

public_records=[{k:q[k] for k in ["id","title","criteria_version","criteria","window_start","deadline","issued_on","prob","status","forecast_id","forecaster","prior","prior_basis","prior_role","method","views","why_right","why_wrong","up_trigger","down_trigger","resolver","sources","probability_history"]} for q in d["questions"]]
(OUT/"observatory/forecast-records.json").write_text(json.dumps(public_records,ensure_ascii=False,indent=2)+"\n")

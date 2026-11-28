"""Build a public, reviewed evidence snapshot; no automatic forecasting."""
import html,json,re
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'dist'/'omnicorp';e=html.escape


def forecast_date(value):
    parsed = date.fromisoformat(value)
    return f'{parsed.day} {parsed:%B %Y}'


d=json.loads((ROOT/'content/observatory.json').read_text())
SLUG=re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')
for kind,items in (('event',d['events']),('question',d['questions'])):
    ids=[x['id'] for x in items]
    assert all(SLUG.fullmatch(x) for x in ids), f'{kind} ids must be lowercase slugs: {ids}'
    assert len(ids)==len(set(ids)), f'duplicate {kind} ids'
def review_anchors(reviews):
    seen={};out=[]
    for r in reviews:
        n=seen[r['date']]=seen.get(r['date'],0)+1
        out.append('review-'+r['date']+('' if n==1 else f'-{n}'))
    return out
library=(OUT/'field-notes/index.html').read_text();home=(OUT/'index.html').read_text()
header=re.search(r'<header>.*?</header>',library,re.S).group().replace('aria-current="page"','aria-current="false"').replace('href="/omnicorp/observatory/"','href="/omnicorp/observatory/" aria-current="page"');footer=re.search(r'<footer>.*?</footer>',library,re.S).group()
plot=(ROOT/'content/curve-fragment.html').read_text()
# Piecewise time scale anchored on the review date: recent evidence is dense, so the
# last 60 days take the right half of the track and earlier years are compressed.
REVIEW=date.fromisoformat(d['reviewed_on']);START=date(2022,1,1)
from datetime import timedelta
SEGMENTS=[(START,REVIEW-timedelta(days=365),3.0,25.0),(REVIEW-timedelta(days=365),REVIEW-timedelta(days=60),25.0,50.0),(REVIEW-timedelta(days=60),REVIEW,50.0,97.0)]
def track_position(day):
    for a,b,x0,x1 in SEGMENTS:
        if day<=b: return x0+max(0,(day-a).days)/max(1,(b-a).days)*(x1-x0)
    return SEGMENTS[-1][3]
def rail_ticks():
    ticks=[(track_position(date(y,1,1)),str(y)) for y in range(START.year,REVIEW.year+1) if date(y,1,1)<SEGMENTS[0][1]]
    ticks+=[(25.0,SEGMENTS[1][0].strftime('%b %Y').upper()),(50.0,SEGMENTS[2][0].strftime('%-d %b').upper())]
    m=date(SEGMENTS[2][0].year,SEGMENTS[2][0].month,1)
    while True:
        m=date(m.year+(m.month==12),m.month%12+1,1)
        if m>=REVIEW-timedelta(days=8): break
        ticks.append((track_position(m),m.strftime('%-d %b').upper()))
    ticks.append((97.0,REVIEW.strftime('%-d %b %Y').upper()))
    fixed=ticks[-1:]+[t for t in ticks if t[0] in (25.0,50.0)]
    kept=list(fixed)
    for t in ticks:
        if t not in kept and all(abs(t[0]-k[0])>=13 for k in kept): kept.append(t)
    ticks=sorted(kept)
    return ''.join(f'<span class="rail-tick{" rail-end" if x==97.0 else ""}" style="left:{x:.2f}%">{e(t)}</span>' for x,t in ticks)
RAIL=rail_ticks()
p=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Observatory — Omnicorp</title><meta name="description" content="A growth horizon, reviewed events and testable forecast questions."><link rel="stylesheet" href="/omnicorp/style.css"><link rel="stylesheet" href="/omnicorp/publications.css"><link rel="stylesheet" href="/omnicorp/observatory.css"><script defer src="/omnicorp/observatory.js"></script><script defer src="/omnicorp/curve.js"></script><script defer src="/omnicorp/permalink.js"></script></head><body class="publication-page observatory-page"><a class="skip" href="#main">Skip to content</a>{header}<main id="main"><section class="section observatory-hero"><div class="section-heading"><p class="eyebrow">THE OMNICORP OBSERVATORY</p><span class="mono dim">REVIEWED / {date.fromisoformat(d["reviewed_on"]).strftime("%d %b %Y").upper()}</span></div><h1>The world moves.<br><span>We update.</span></h1><p class="observatory-deck">From the transistor moment to an open horizon.<br>Track the evidence. Challenge the expectations.</p><div class="observatory-console"><div class="console-top mono"><span><i class="signal"></i> TODAY / SCHEMATIC POSITION</span><span>SINGULARITY: AN OPEN QUESTION</span></div>{plot}<div class="horizon-reading"><h2>Today is dated.<br><span>The height is schematic.</span></h2><p>{e(d['summary'])} The dot’s height was chosen for the illustration, not estimated from data. Its accuracy has no defined probability. The curves are scenarios, not confidence bands. The percentages below refer only to specific dated forecasts.</p></div></div><div class="observatory-links"><a href="#evidence">Explore the events ↓</a><a href="#questions">Forecast questions ↓</a><a href="#revisions">What changed ↓</a></div></section><section class="section" id="evidence"><div class="section-heading"><p class="eyebrow">01 / WHAT CHANGED?</p><span class="mono dim">EVENT ≠ ASSESSMENT ≠ FORECAST</span></div><h2>Read the signals.<br><span>Keep the counterevidence.</span></h2><p class="observatory-deck">A selected evidence timeline from public access to mathematical discovery. Dates and our assessments are distinct. Related reports retain their source lineage: a sequel is not another independent discovery. Public proof corrections stay visible alongside advances.</p><div class="evidence-workspace"><div><div class="evidence-rail mono">'''+RAIL+'</div>'
for lane in ['Public access','Scientific work','Autonomous work','Real-world usefulness','Cumulative improvement','Physical work']:
 p+=f'<div class="evidence-lane {"scientific" if lane=="Scientific work" else ""}"><span>{e(lane)}</span><div class="lane-track">'
 events=[(i,x) for i,x in enumerate(d['events']) if x['lane']==lane]
 if not events:p+='<small>NO SELECTED OBSERVATION</small>'
 # Greedy row packing: events never share a row closer than 11% of the track (dot plus side label).
 rows_end=[];placed=[]
 for i,x in events:
  pos=track_position(date.fromisoformat(x['date']))
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
  p+=f'<button data-event="{i}" class="evidence-dot {x["motion"]}" style="left:{pos:.2f}%;top:{top}px" aria-pressed="false" aria-label="{e(x["title"],quote=True)}"><span>{x["date"][5:] if date.fromisoformat(x["date"])>=SEGMENTS[2][0] else x["date"][:7]}</span></button>'
 p+='</div></div>'
p+='<p class="evidence-key mono">ACID / CAPABILITY SIGNAL · AMBER / LIMIT · CYAN / MIXED<br>SCALE WIDENS TOWARD THE REVIEW DATE: THE LAST 60 DAYS FILL THE RIGHT HALF, ENDING AT THE REVIEW</p>'
p+='</div><article class="evidence-detail" aria-live="polite" aria-atomic="true"><p class="eyebrow" id="event-evidence"></p><h3 id="event-title"></h3><p class="event-meta mono"><span id="event-date"></span><br><span id="event-reviewed"></span></p><span id="event-direction" class="direction-label"></span><dl>'
for field,label in [('claim','What the source reports'),('interpretation','Our reading'),('limit','What it does not establish'),('comparison','Compared with expectations')]:p+=f'<dt>{label}</dt><dd id="event-{field}"></dd>'
p+='</dl><a id="event-source" class="text-link" href="#">Primary source ↗</a><p class="permalink-row"><a class="permalink event-permalink" href="#event-__initial__" data-permalink aria-label="Copy link to this event">Copy link to this event</a></p><div id="event-questions"></div></article></div></section><section class="section forecast-section" id="questions"><div class="section-heading"><p class="eyebrow">02 / MAKE EXPECTATIONS TESTABLE</p><span class="mono dim">SUPERFORECASTING / QUESTION DESIGN</span></div><h2>Smaller questions.<br><span>Sharper updates.</span></h2><p class="observatory-deck">How far to singularity has no agreed measuring stick. These registered milestone forecasts make parts of the ambition resolvable. Each percentage is our subjective chance of a qualifying new public record by its deadline—not confidence that the curve position is accurate.</p><div class="forecast-grid">'
FROZEN_RECORDS="https://github.com/sloik/post-ai-worlds/blob/main/evidence/forecasts/2026-11-05-records.json"
for i,q in enumerate(d['questions']):
 percent=round(q['prob']*100);hist=q['probability_history'];initial=round(hist[0]['prob']*100);revised=len(hist)>1
 issued_note=f' at {initial}% · revised {hist[-1]["date"]}' if revised else ''
 current_note=f' · current estimate {percent}% since {hist[-1]["date"]}: {e(hist[-1]["reason"])}' if revised else ''
 views=' / '.join(str(round(x*100))+'%' for x in q['views'])
 p+=f'<article class="forecast-card" id="{q["id"]}"><div class="forecast-card-top mono"><span>Q{i+1:02} / {e(q["lane"])}</span><span>BY {q["deadline"]}</span><a class="permalink" href="#{q["id"]}" data-permalink aria-label="Copy link to forecast Q{i+1:02}">Copy link</a></div><h3>{e(q["title"])}</h3><div class="forecast-number"><strong>{percent}<span>%</span></strong><div>CHANCE OF YES<small>New public record by {q["deadline"]}<br>Issued {forecast_date(q["issued_on"])}{issued_note} · open forecast</small></div></div><p class="forecast-precision">Subjective estimate, not an empirical base rate or a singularity probability.</p><p class="forecast-record-link"><a class="text-link" href="'+e(q.get("record_url",FROZEN_RECORDS),quote=True)+'">Forecast record on GitHub ↗</a></p><details class="forecast-reasons"><summary>Why this may happen, and why we might be wrong +</summary><div class="forecast-cases"><div><h4>Why we think this may happen</h4><ul>'+''.join('<li>'+e(x)+'</li>' for x in q['why_right'])+'</ul></div><div><h4>Why we might be wrong</h4><ul>'+''.join('<li>'+e(x)+'</li>' for x in q['why_wrong'])+'</ul></div></div></details><details><summary>Exact outcome, timeframe & update signals +</summary><dl>'
 for field,label in [('criteria','What counts as YES'),('resolver','Resolution source & edge cases')]:p+=f'<dt>{label}</dt><dd>{e(q[field])}</dd>'
 p+=f'<dt>Observation window</dt><dd>{forecast_date(q["window_start"])} through {q["deadline"]} at 23:59 UTC. Criteria version {e(q["criteria_version"])}. Previously published cases do not count as new outcomes.</dd>'
 for field,label in [('up_trigger','Evidence that would raise the probability'),('down_trigger','Evidence that would lower it')]:
  trigger=q[field];p+=f'<dt>{label}</dt><dd>{e(trigger["description"])} Proposed likelihood-ratio multiplier: {trigger["lr"]}. This is an update rule for review, not an automatic score.</dd>'
 p+='</dl></details><details><summary>How we estimated this +</summary><dl>'
 for field,label in [('prior_basis','One contributing analyst’s starting point'),('reference_class','Reference-class limitations'),('method','Combining perspectives'),('confidence_note','Limits of confidence')]:p+=f'<dt>{label}</dt><dd>{e(q[field])}</dd>'
 p+=f'<dt>Separately elicited views</dt><dd>{views}. The spread reflects analyst disagreement, not a confidence interval. Shared model-family and source dependencies limit the ensemble.</dd><dt>Current record</dt><dd>Forecast #{q["forecast_id"]} · initial estimate {initial}%{current_note} · not yet resolved or scored.</dd></dl><p class="eyebrow">PRIMARY EVIDENCE</p><ul class="forecast-sources">'
 for source in q['sources']:p+=f'<li><a href="{e(source["url"],quote=True)}">{e(source["title"])} ↗</a></li>'
 p+='</ul>'
 p+='</details></article>'
p+='</div><div class="calibration-note"><span class="mono">FORECASTING, NOT DECORATION</span><p>Before publishing a number: define the reference class, weigh evidence for and against, compare separately elicited assessments, record the probability and name its update triggers. At resolution: score it and retain the lesson. A Brier score measures accuracy on those questions; it does not validate a singularity-distance scale.</p><p>The first forecasts were registered on 5 November 2026. Each record gives its own issue date, prospective criteria and opposing cases. The series has no resolved outcomes for measuring calibration yet. Earlier internal forecasts remain separate. This is a reviewed snapshot, not automatic monitoring.</p><a class="text-link" href="https://github.com/sloik/superforecasting">The superforecasting playbook ↗</a><br><a class="text-link" href="/omnicorp/observatory/forecast-records.json">Download the dated forecast records ↗</a></div></section><section class="section" id="revisions"><div class="section-heading"><p class="eyebrow">03 / KEEP THE RECEIPTS</p><span class="mono dim">WHAT CHANGED / AND WHY</span></div><h2>Revision is<br><span>part of the work.</span></h2>'
for r,anchor in zip(d['reviews'],review_anchors(d['reviews'])):p+=f'<article class="revision-entry" id="{anchor}"><time class="mono">{r["date"]}</time><div><h3>{e(r["title"])}</h3><p>{e(r["reason"])}</p><span class="mono">INITIAL FORECASTS ISSUED: {r.get("initial_forecasts",0)} · PROBABILITY REVISIONS: {r["forecast_changes"]}</span> <a class="permalink" href="#{anchor}" data-permalink aria-label="Copy link to this revision">Copy link</a></div></article>'
p+='''<div class="review-method"><p class="eyebrow">HOW THE POSITION CHANGES</p><ol><li><strong>Record the event.</strong> Retain its date, source and research lineage.</li><li><strong>Test the criterion.</strong> Distinguish a new capability from another announcement of the same result.</li><li><strong>Revise a registered forecast.</strong> Explain the evidence, retain the prior and consider both directions. No change is a valid conclusion.</li><li><strong>Show the revision.</strong> Keep the registered initial probability and every subsequent revision visible. Failed expectations and retractions can move the outlook back; calendar time never moves backward.</li></ol><p>Demonstrated milestones change our picture of the future. They are not a percentage of the journey to singularity.</p></div><a class="button" href="/omnicorp/field-notes/">Read the thinking behind it <span>↗</span></a></section></main>'''
p+=footer.replace('</body></html>','')+'<script id="observatory-data" type="application/json">'+json.dumps(d,ensure_ascii=False).replace('<','\\u003c')+'</script></body></html>'
# Default evidence remains readable if JavaScript is unavailable.
initial=d['events'][-1]
for field in ['title','evidence','claim','interpretation','limit','comparison','direction']:
 p=re.sub(r'(<[^>]+id="event-'+field+r'"[^>]*>).*?(</[^>]+>)',lambda m:m[1]+e(initial[field])+m[2],p)
p=p.replace('<span id="event-date"></span>','<span id="event-date">EVENT / '+initial['date']+'</span>').replace('<span id="event-reviewed"></span>','<span id="event-reviewed">REVIEW / '+initial['assessed_on']+'</span>')
p=p.replace('#event-__initial__','#event-'+initial['id'])
p=p.replace('<a id="event-source" class="text-link" href="#">Primary source ↗</a>','<a id="event-source" class="text-link" href="'+e(initial['source'],quote=True)+'">'+e(initial['source_title'])+' ↗</a>')
fallback='<noscript><section class="section"><h2>All reviewed events</h2>'
for event in d['events']:
 fallback+='<details id="event-'+event['id']+'"><summary>'+e(event['date']+' / '+event['title'])+'</summary>'
 for field in ['claim','interpretation','limit','comparison']:fallback+='<p>'+e(event[field])+'</p>'
 fallback+='<a href="'+e(event['source'],quote=True)+'">'+e(event['source_title'])+' ↗</a></details>'
fallback+='</section></noscript>'
p=p.replace('</main>',fallback+'</main>')
# Deep-link namespace: real element ids plus the fragments the scripts resolve
# (#event-<id>, #curve-<id>) must never collide. The noscript fallback carries
# the event fragments on purpose, so it is excluded from the real-id scan.
real_ids=re.findall(r'\sid="([^"]+)"',re.sub(r'<noscript>.*?</noscript>','',p,flags=re.S))
curve_ids=re.findall(r'<button type="button" data-curve-event="([^"]+)"',plot)
fragments=real_ids+['event-'+x['id'] for x in d['events']]+['curve-'+x for x in curve_ids]
dupes=sorted({x for x in fragments if fragments.count(x)>1})
assert not dupes, f'deep-link anchors collide: {dupes}'

(OUT/'observatory').mkdir(exist_ok=True);(OUT/'observatory/index.html').write_text(p)
print('Built Observatory.')

public_records=[{k:q[k] for k in ["id","title","criteria_version","criteria","window_start","deadline","issued_on","prob","status","forecast_id","forecaster","prior","prior_basis","prior_role","method","views","why_right","why_wrong","up_trigger","down_trigger","resolver","sources","probability_history"]} for q in d["questions"]]
for question, record in zip(d['questions'], public_records):
    if 'record_url' in question:
        record['record_url'] = question['record_url']
(OUT/"observatory/forecast-records.json").write_text(json.dumps(public_records,ensure_ascii=False,indent=2)+"\n")

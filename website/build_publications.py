"""Build curated public essays into static, independently readable pages."""
import html
import json
import math
import re
from xml.etree import ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist' / 'omnicorp'
esc = html.escape
GROUPS = {'foundations': ('01', 'Foundations'), 'practice': ('02', 'Building & operating'), 'critique': ('03', 'Critical perspectives')}
ORDER = ['continual-development','charter','blueprint','solo-to-scale','agent-teams','software-factory','physical-world','capital-and-resources','roadmap','risks-and-moats','case-study-every','efficiency-and-legitimacy','human-accountability','operator-counter-reading','glossary']
articles = []
for group in GROUPS:
    for article in json.loads((ROOT / 'content' / f'{group}.json').read_text()):
        article['group'] = group
        articles.append(article)
articles.sort(key=lambda a: ORDER.index(a['slug']))
assert len(articles) == 15 and len({a['slug'] for a in articles}) == 15

def url(a): return '/omnicorp/field-notes/' + a['slug'] + '/'
def head(title, description):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#090c0d"><title>{esc(title)} — Omnicorp</title><meta name="description" content="{esc(description,quote=True)}"><link rel="stylesheet" href="/omnicorp/style.css"><link rel="stylesheet" href="/omnicorp/publications.css"><script defer src="/omnicorp/publications.js"></script></head><body class="publication-page"><div class="reading-progress" aria-hidden="true"></div><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="/omnicorp/"><span class="brand-icon" aria-hidden="true">◈</span> OMNICORP</a><nav aria-label="Main navigation"><a href="/omnicorp/">The vision</a><a href="/omnicorp/observatory/">Observatory</a><a href="/omnicorp/field-notes/" aria-current="{'page' if title=='Field Notes' else 'false'}">Field notes</a></nav><a class="header-cta" href="mailto:stocki.lukasz+omnicorp@gmail.com">Email Łukasz ↗</a></header>'''
def footer():
    return '''<footer><a class="brand" href="/omnicorp/">OMNICORP</a><p class="mono">THINK IN THE OPEN. BUILD WITH INTENT.</p><div><a href="/omnicorp/observatory/">Observatory ↗</a><a href="/omnicorp/field-notes/">Field notes ↗</a><a href="https://stocki-apps.pages.dev/">Apps ↗</a><span>No cookies. No analytics.</span><span>© 2026 Łukasz Stocki</span></div></footer></body></html>'''
def card(a, featured=False):
    group=GROUPS[a['group']][1]
    search_text=' '.join([a['title'],a['summary'],a['kicker']]+[p for section in a['sections'] for p in section['paragraphs']]+a['questions'])
    words=len(search_text.split())
    return f'''<a class="paper-card {'paper-featured' if featured else ''}" href="{url(a)}" data-group="{a['group']}" data-search="{esc(search_text,quote=True)}"><div class="paper-card-top mono"><span>{esc(group)}</span><span>{max(2,math.ceil(words/200))} MIN READ ↗</span></div><div class="paper-art"><img src="/omnicorp/art/{a['slug']}.svg" alt="" loading="lazy" width="900" height="450"></div><p class="eyebrow">{esc(a['kicker'])}</p><h3>{esc(a['title'])}</h3><p>{esc(a['summary'])}</p><span class="paper-read mono">READ THE PAPER <b>↗</b></span></a>'''

library=head('Field Notes','The evolving Omnicorp library: purpose, organisation, agent teams, building and critical perspectives.')
library+='''<main id="main"><section class="library-hero section"><div class="section-heading"><p class="eyebrow">THE OMNICORP LIBRARY</p><span class="mono dim">WORKING PAPERS / PUBLIC EDITIONS</span></div><div class="library-intro"><div><h1>Thinking.<br><span>In the open.</span></h1><p>The ideas behind the organisation.<br>The work, the questions and the arguments against ourselves.</p></div><div class="library-orbit" aria-hidden="true"><i></i><i></i><i></i><b>15</b><span>CONNECTED PAPERS</span></div></div><a class="observatory-bridge" href="/omnicorp/observatory/"><span class="mono">THE OMNICORP OBSERVATORY</span><strong>Where are we on the curve?</strong><span>Explore the growth visual, current evidence and forecast questions ↗</span></a><div class="editorial-note"><span class="mono">A LIVING BODY OF WORK</span><p>These are public editions of our Omnicorp design notes, developed from June to November 2026. They describe an evolving ambition and proposed ways of working. They are not a claim that the entire organisation already exists.</p></div></section><section class="section library-content" aria-labelledby="library-title"><div class="section-heading"><p class="eyebrow" id="library-title">FIND A THREAD. FOLLOW IT.</p><span class="mono dim">15 PAPERS / 3 READING PATHS</span></div><div class="library-tools"><div class="library-filters" role="group" aria-label="Filter papers"><button type="button" data-filter="all" aria-pressed="true">All papers</button><button type="button" data-filter="foundations" aria-pressed="false">Foundations</button><button type="button" data-filter="practice" aria-pressed="false">Building & operating</button><button type="button" data-filter="critique" aria-pressed="false">Critical perspectives</button></div><label class="paper-search"><span class="mono">SEARCH THE LIBRARY</span><input id="paper-search" type="search" placeholder="Memory, teams, accountability…"></label></div><p class="result-count mono" aria-live="polite">15 papers</p><div class="paper-grid">'''
library+=''.join(card(a,i==0) for i,a in enumerate(articles))
library+='''</div><p class="empty-results" hidden>No papers match this search. Try a broader idea or choose All papers.</p></section><section class="library-close section"><p class="eyebrow">THE ARGUMENT STAYS OPEN</p><h2>Find the weak point.<br><span>Help us think further.</span></h2><p>Questions, counterarguments and practical experience belong in this conversation.</p><a class="button" href="mailto:stocki.lukasz+omnicorp@gmail.com">Email Łukasz <span>↗</span></a><p class="contact-address"><a href="mailto:stocki.lukasz+omnicorp@gmail.com">stocki.lukasz+omnicorp@gmail.com</a><br><small>Opens your email app.</small></p></section></main>'''+footer()
(OUT/'field-notes').mkdir(exist_ok=True)
(OUT/'field-notes'/'index.html').write_text(library)
for index,a in enumerate(articles):
    body=head(a['title'],a['summary'])
    text=' '.join(p for s in a['sections'] for p in s['paragraphs'])
    minutes=max(2,math.ceil(len(text.split())/200))
    group=GROUPS[a['group']][1]
    body+=f'''<main id="main"><div class="article-masthead"><a class="back-library mono" href="/omnicorp/field-notes/">← ALL FIELD NOTES</a><p class="eyebrow">{esc(group)} / PAPER {index+1:02}</p><h1>{esc(a['title'])}</h1><p class="article-deck">{esc(a['summary'])}</p><div class="article-meta mono"><span>ŁUKASZ STOCKI & ARGO</span><span>PUBLIC EDITION / 05 NOV 2026</span><span>{minutes} MIN READ</span><button type="button" class="print-paper">PRINT / SAVE PDF ↗</button></div></div><figure class="article-graphic"><img src="/omnicorp/art/{a['slug']}.svg" alt="{esc(ET.parse(OUT/'art'/(a['slug']+'.svg')).getroot().find('{http://www.w3.org/2000/svg}desc').text,quote=True)}" width="900" height="450"><figcaption class="mono">A VISUAL READING / CONCEPTUAL DIAGRAM <a href="/omnicorp/diagrams/{a['slug']}/">OPEN FULL-SIZE DIAGRAM ↗</a></figcaption></figure><div class="article-layout"><aside class="article-toc"><span class="eyebrow">IN THIS PAPER</span><nav aria-label="Contents">'''
    body+=''.join(f'<a href="#section-{i}">{i+1:02} / {esc(s["heading"])}</a>' for i,s in enumerate(a['sections']))
    body+='''<a href="#questions">↗ Open questions</a></nav><a class="toc-library mono" href="/omnicorp/field-notes/">EXPLORE THE LIBRARY ↗</a></aside><article class="paper-body"><div class="paper-status"><i class="signal"></i> WORKING PAPER · DESIGN & ANALYSIS</div>'''
    for i,section in enumerate(a['sections']):
        body+=f'<section id="section-{i}"><span class="section-number mono">{i+1:02}</span><h2>{esc(section["heading"])}</h2>'+''.join(f'<p>{esc(p)}</p>' for p in section['paragraphs'])+'</section>'
    body+='<section class="open-questions" id="questions"><p class="eyebrow">THE NEXT QUESTIONS</p><h2>What remains open.</h2><ul>'+''.join('<li>'+esc(q)+'</li>' for q in a['questions'])+'</ul></section>'
    sources=a.get('sources',[])
    if sources:
        body+='<section class="paper-sources"><p class="eyebrow">FURTHER READING</p><ul>'
        for source in sources:
            if not source['url'].startswith('https://'): raise ValueError('Non-public source URL')
            body+=f'<li><a href="{esc(source["url"],quote=True)}">{esc(source["title"])} ↗</a></li>'
        body+='</ul></section>'
    body+=f'''<div class="edition-note"><p class="mono">ABOUT THIS EDITION</p><p>Adapted from the Omnicorp working document “{esc(a['source_file'].removesuffix('.md').replace('-', ' '))}”. This is an edited public essay, not a verbatim release of internal notes. The founding purpose is continual development of the organisation’s ability to understand and act; commercial and physical work sustain and ground it.</p></div></article></div><section class="related-papers section"><p class="eyebrow">KEEP FOLLOWING THE THREAD</p><div class="related-grid">'''
    related=[articles[(index+1)%len(articles)],articles[(index+2)%len(articles)]]
    body+=''.join(card(other) for other in related)+'</div><a class="text-link" href="/omnicorp/field-notes/">Back to all 15 papers <span>↗</span></a></section></main>'+footer()
    folder=OUT/'field-notes'/a['slug'];folder.mkdir(exist_ok=True);(folder/'index.html').write_text(body)
print(f'Built library and {len(articles)} public paper pages.')

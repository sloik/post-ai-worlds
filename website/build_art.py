"""Create fifteen original semantic SVG plates for the public papers."""
from pathlib import Path
import math,html
ROOT=Path(__file__).resolve().parent/'dist/omnicorp/art';ROOT.mkdir(exist_ok=True)
A='#d9ff43';C='#5cddd2';W='#dce8d2';M='#8fa584'
def line(x1,y1,x2,y2,color=M,dash=False):return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="1.5" fill="none"'+(' stroke-dasharray="4 7" class="flow"' if dash else '')+'/>'
def text(x,y,s,color=M,size=12,anchor='middle'):return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-size="{max(12,size)}">{html.escape(s)}</text>'
def circle(x,y,r,color=A,fill='#122016',cls=''):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="1.2" class="{cls}"/>'
def box(x,y,w,h,label,color=A):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#102019" stroke="{color}" stroke-width="1"/>'+text(x+w/2,y+h/2+4,label,color,11)
def path(d,color=A,fill='none',extra=''):return f'<path d="{d}" stroke="{color}" fill="{fill}" stroke-width="1.5" {extra}/>'
def node(x,y,label,r=32,color=A):return circle(x,y,r,color)+text(x,y+4,label,color,10)
plates={}
# Purpose as compass: sustaining links feed a direction rather than an output counter.
s=''
for x,y,label in [(450,85,'UNDERSTAND'),(700,220,'ACT'),(450,345,'LEARN'),(200,220,'RETAIN')]:
 s+=line(450,220,x,y,C,True)+node(x,y,label,48,C)
s+=circle(450,220,87,A)+text(450,213,'PURPOSE',A,17)+text(450,239,'CONTINUAL DEVELOPMENT',M,9)
s+=path('M450 115 L465 180 L450 165 L435 180 Z',A,'#d9ff4330')
plates['charter']=('THE PURPOSE COMPASS','Purpose coordinates understanding, action, learning and retained knowledge.',s)
# Exploded five-layer architecture.
s=''
for i,label in enumerate(['RESOURCES','PRODUCT ENGINES','ORGANISATIONAL MEMORY','COORDINATION','HUMAN DIRECTION']):
 y=315-i*50;x=230+i*23
 s+=path(f'M{x} {y} l300 0 95 -38 -300 0 Z',C if i%2 else A,'#15271c')+line(x+45,y,x+45,y-48,M,True)+text(x+195,y-12,label,W,11)
s+=text(755,180,'FIVE LAYERS',A,12)+text(755,202,'ONE SYSTEM',M,10)
plates['blueprint']=('THE ORGANISATIONAL STACK','Five connected organisational layers, from resources to human direction.',s)
# Increasing scale with parallel reviewer branch.
s=''
for i,x in enumerate([100,270,450,640,805]):
 count=i+1
 for j in range(count):
  y=160+(j-(count-1)/2)*31
  s+=circle(x,y,10,A if j%2==0 else C)
 if i<4:s+=line(x+24,160,[270,450,640,805][i]-25,160,M,True)
 s+=text(x,285,['ONE OPERATOR','REPEATABLE LOOP','SMALL TEAM','SEVERAL ENGINES','OPTIONAL SCALE'][i],M,9)+text(x,320,f'GATE {i+1:02}',A,10)
s+=path('M100 235 H805',C)+text(450,365,'REVIEW CAPACITY MUST GROW WITH CREATION',C,11)
plates['solo-to-scale']=('THE SCALE LADDER','Five stages of organisational scale; review capacity grows alongside creation.',s)
# Circuit board roles with independent review.
s=''
coords=[(130,200,'EXPLORE'),(330,120,'DESIGN'),(500,210,'BUILD'),(690,125,'CRITIQUE'),(780,295,'INTEGRATE')]
for a,b in zip(coords,coords[1:]):s+=path(f'M{a[0]} {a[1]}H{(a[0]+b[0])/2}V{b[1]}H{b[0]}',C,extra='stroke-dasharray="5 8" class="flow"')
for x,y,label in coords:s+=node(x,y,label,43,C if label=='CRITIQUE' else A)
s+=path('M690 170V260H500',A,extra='stroke-dasharray="4 7"')+text(595,282,'RETURN / REVISE',M,9)
s+=text(135,310,'BOUNDED MANDATES',M,10)+text(135,332,'EXPLICIT HANDOFFS',C,10)
plates['agent-teams']=('THE RESPONSIBILITY CIRCUIT','Explorer, designer, builder, critic and integrator exchange bounded work; critique can return a candidate.',s)
# Retained checkpoints rising through separate gates.
s=''
for i in range(4):
 x=135+i*190;y=300-i*65
 if i<3:s+=path(f'M{x+25} {y}H{x+110}V{y-65}H{x+165}',A,extra='class="flow" stroke-dasharray="6 4"')
 s+=node(x,y,f'V{i}',30)+text(x,y+48,'RETAINED',M,8)
 if i<3:s+=line(x+105,y+10,x+105,y-100,C)+text(x+105,y-112,'EVALUATE',C,8)
s+=path('M435 190V335H360',M,extra='stroke-dasharray="4 7"')+text(405,357,'REJECT / RESTORE',M,10)
s+=text(750,325,'IMPROVE THE NEXT STARTING POINT',A,10)
plates['continual-development']=('THE RETAINED LINEAGE','Accepted checkpoints rise through evaluation gates while rejected candidates branch into restoration.',s)
# Production conveyor and a distinct lesson return lane.
s=''
for i,label in enumerate(['PROBLEM','CHANGE','TEST','REVIEW','RELEASE']):
 x=50+i*170
 s+=box(x,150,130,65,label,C if i in (2,3) else A)
 if i<4:s+=line(x+130,182,x+170,182,A,True)
s+=path('M795 220V310H115V225',C,extra='stroke-dasharray="5 9" class="flow"')+text(450,338,'LESSONS RETURN TO THE NEXT CHANGE',C,12)
plates['software-factory']=('THE LEARNING PRODUCTION LINE','A bounded software change moves through tests and review to release; lessons return to the next change.',s)
# Boundary between proposal and physical controls.
s=box(90,75,250,65,'REASONING / PROPOSALS')+box(560,75,250,65,'OBSERVATIONS / MODELS',C)
s+=line(215,140,215,210,A,True)+line(685,210,685,140,C,True)+path('M55 190H845',M,extra='stroke-dasharray="3 6"')+text(450,179,'CONTROL & AUTHORITY BOUNDARY',M,10)
s+=box(95,245,240,65,'INTERLOCKS / PERMISSIONS',C)+box(565,245,240,65,'SENSORS / MEASUREMENT',C)+line(335,277,565,277,A,True)
s+=path('M375 330l75 -35 75 35 -75 35 Z',A,'#20351c')+line(450,278,450,330,A)+text(450,387,'REAL MACHINES. REAL CONSEQUENCES.',W,11)
plates['physical-world']=('THE REAL-WORLD BOUNDARY','Reasoning crosses an authority boundary through interlocks, machines and sensor feedback.',s)
# Resource reservoir and branching channels.
s=path('M330 85V220Q450 270 570 220V85',A,'#1c301b')+path('M330 150Q450 190 570 150',C)+text(450,116,'RESOURCES',A,15)
for x,label in [(180,'CAPABILITY'),(450,'VERIFICATION'),(720,'CONTINUITY')]:s+=path(f'M450 240V280H{x}V315',C,extra='stroke-dasharray="4 7" class="flow"')+box(x-90,315,180,45,label,C)
s+=path('M190 95H300',A,extra='stroke-dasharray="4 7" class="flow"')+text(175,74,'USEFUL OUTCOMES',M,10)+text(450,395,'REINVESTMENT IS A CHOICE, NOT A GUARANTEE',M,10)
plates['capital-and-resources']=('THE RESOURCE WATERSHED','Useful outcomes replenish resources, allocated to capability, verification and continuity.',s)
# An expedition with defined gates and faint options.
s=path('M80 320L230 235 380 270 520 175 670 200',A,extra='stroke-dasharray="7 4" class="flow"')
for i,(x,y) in enumerate([(80,320),(230,235),(380,270),(520,175),(670,200)]):s+=node(x,y,str(i+1),18)+text(x,y+43,['USEFUL WORK','REPEATABILITY','RELIABILITY','DELEGATION','NEW ENGINES'][i],M,8)
s+=path('M670 200L820 80M670 200L840 210M670 200L790 345',C,extra='opacity=".4" stroke-dasharray="3 7"')+text(770,390,'OPTIONS, NOT PROMISES',C,10)
plates['roadmap']=('THE GATED EXPEDITION','A roadmap passes evidence gates before opening several uncertain future paths.',s)
# Adversarial moat/risk terrain.
s=''
for r,color in [(135,M),(105,C),(70,A)]:s+=path(f'M{450-r} 200L450 {200-r} {450+r} 200 450 {200+r}Z',color,'#122018')
s+=text(450,203,'CORE',A,18)
for x,y,label in [(140,95,'DEPENDENCY'),(760,100,'EROSION'),(155,335,'COORDINATION'),(770,335,'DEMAND')]:s+=line(x,y,450+(x-450)*.4,200+(y-200)*.5,M,True)+text(x,y,label,C,11)
s+=line(335,290,250,355,A)+text(450,390,'TRUST + RETAINED KNOWLEDGE',A,11)
plates['risks-and-moats']=('THE ADVERSARIAL TERRAIN','An operating core faces dependency, erosion, coordination and demand risks; trust and knowledge reinforce it.',s)
# Four compounding print plates.
s=''
for i,label in enumerate(['PLAN','WORK','REVIEW','COMPOUND']):
 x=100+i*195
 for j in range(i+1):s+=path(f'M{x} {260+j*10}l110 0 30 -15 -110 0 Z',C,'#11241b',extra='opacity=".5"')
 s+=box(x,125,140,90,label,A if i==3 else C)+text(x+70,330,['INTENT','CHANGE','CRITIQUE','RETAIN'][i],M,9)
 if i<3:s+=line(x+145,170,x+190,170,A,True)
plates['case-study-every']=('THE COMPOUNDING PRESS','Plan, work, review and compound leave accumulated retained layers; this is an interpretation of a published method.',s)
# Efficiency domain plus legitimacy floor.
s=path('M160 70V325H780',M)+path('M160 260L780 100',A)+path('M280 325V70',C,extra='stroke-dasharray="4 7"')+path('M280 260L680 140 770 150V325H280Z',C,'#17362a55')
s+=circle(580,205,12,A)+text(550,250,'OPERATING ENVELOPE',A,12)+text(515,363,'VERIFIED VALUE / RESOURCE USE →',M,11)+text(185,55,'LEGITIMACY IS A SEPARATE CONDITION',C,11)+text(226,220,'FLOOR',C,10)
plates['efficiency-and-legitimacy']=('THE OPERATING ENVELOPE','A conceptual operating envelope separates efficiency from a legitimacy boundary; no measured performance is plotted.',s)
# A responsibility chain with explicit return path.
s=''
for i,label in enumerate(['DECISION','EXPLANATION','ANSWERABILITY','CONSEQUENCE']):
 x=120+i*215;s+=node(x,190,label,50,C if i==2 else A)
 if i<3:s+=line(x+50,190,x+165,190,A,True)
s+=path('M765 250V315H120V250',C,extra='class="flow" stroke-dasharray="4 7"')+text(450,345,'CORRECTION RETURNS TO THE DECISION',C,11)
s+=text(550,85,'WHO CAN ANSWER FOR THE OUTCOME?',A,12)
plates['human-accountability']=('THE ANSWERABILITY CHAIN','Decision, explanation, responsibility and consequences form a chain, with correction returning to the decision.',s)
# Conflicting architecture split by physical bottleneck.
s=box(70,110,230,75,'ASSET-LIGHT BLUEPRINT')+box(600,110,230,75,'PHYSICAL THROUGHPUT',C)
s+=path('M300 147H380L425 230V300H475V230L520 147H600',A,'#1a2a19')+text(450,335,'THE BINDING CONSTRAINT',A,13)
for i,label in enumerate(['ENERGY','FABRICATION','SUPPLY CHAIN']):s+=line(655+i*65,225,655+i*65,280,C)+text(680,235+i*27,label,M,9)
s+=text(180,260,'CLAIM',M,11)+text(180,290,'↔ COUNTER-READING',C,11)
plates['operator-counter-reading']=('THE BOTTLENECK LENS','An asset-light blueprint meets physical throughput constraints through a narrow bottleneck.',s)
# Semantic constellation: four families, visibly crosslinked.
s='';nodes=[(180,110,'CAPABILITY'),(450,90,'AGENCY'),(720,115,'EVIDENCE'),(180,300,'RESOURCES'),(450,310,'CONTINUITY'),(720,300,'LEGITIMACY')]
for a,b in [(0,1),(1,2),(0,3),(1,4),(2,5),(3,4),(4,5),(1,5),(2,4)]:s+=line(nodes[a][0],nodes[a][1],nodes[b][0],nodes[b][1],C,True)
for i,(x,y,label) in enumerate(nodes):s+=node(x,y,label,42,A if i in (1,4) else C)
s+=text(450,210,'SHARED MEANINGS',A,15)
plates['glossary']=('THE SEMANTIC ATLAS','Six connected concepts: capability, agency, evidence, resources, continuity and legitimacy.',s)
for index,(slug,(title,desc,shapes)) in enumerate(plates.items(),1):
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 450" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)} Conceptual diagram.</desc><defs><pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#31452f" stroke-width=".4" opacity=".5"/></pattern><radialGradient id="aura"><stop stop-color="#294b2255"/><stop offset="1" stop-color="#0a1012"/></radialGradient></defs><style>text{{font-family:ui-monospace,Consolas,monospace;letter-spacing:1px}}.flow{{animation:signal 12s linear infinite}}@keyframes signal{{to{{stroke-dashoffset:-80}}}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style><rect width="900" height="450" fill="#0a1012"/><rect width="900" height="450" fill="url(#aura)"/><rect x="30" y="55" width="840" height="350" fill="url(#grid)"/>{text(35,28,title,A,10,'start')}{text(865,28,f'OMNI / PLATE {index:02}',M,9,'end')}<g>{shapes}</g>{text(35,432,'CONCEPTUAL DIAGRAM / NOT LIVE TELEMETRY',M,8,'start')}{text(865,432,'OMNICORP FIELD NOTES',C,8,'end')}</svg>'''
 (ROOT/(slug+'.svg')).write_text(svg)
print(f'Created {len(plates)} distinct illustrated plates.')
# A standalone HTML viewer keeps diagrams readable on small screens.
for slug,(title,desc,_) in plates.items():
 folder=ROOT.parent/'diagrams'/slug;folder.mkdir(parents=True,exist_ok=True)
 page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} — Omnicorp diagram</title><link rel="stylesheet" href="/omnicorp/style.css"><style>body{{padding:35px 5%}}h1{{font-size:clamp(28px,4vw,50px);letter-spacing:-1px;margin:35px 0 20px}}p{{color:#a5afae;font-size:14px;line-height:1.8;max-width:800px}}figure{{margin:30px 0;max-width:100%;overflow:auto;border:1px solid #455c34}}img{{display:block;width:100%;min-width:900px;height:auto}}a{{color:#d9ff43;font:12px ui-monospace,monospace}}</style></head><body><a href="/omnicorp/field-notes/{slug}/">← Back to the paper</a><main><h1>{html.escape(title)}</h1><p>{html.escape(desc)} This is a conceptual diagram. On a small screen, pan across the illustration to read its labels.</p><figure><img src="/omnicorp/art/{slug}.svg" alt="{html.escape(desc,quote=True)}" width="900" height="450"></figure></main></body></html>'''
 (folder/'index.html').write_text(page)

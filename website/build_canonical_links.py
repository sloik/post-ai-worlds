"""Add idempotent canonical links to all public introduction pages."""
from pathlib import Path
import html
import json
import re
ROOT=Path(__file__).resolve().parent
BASE="https://github.com/sloik/post-ai-worlds"
chapters={a["slug"]:a["source_file"] for group in ("foundations","practice","critique") for a in json.loads((ROOT/"content"/(group+".json")).read_text())}
for p in (ROOT/"dist/omnicorp").rglob("*.html"):
    s=p.read_text()
    s=re.sub(r'<!-- canonical-home:start -->.*?<!-- canonical-home:end -->',"",s,flags=re.S)
    s=s.replace('<link rel="stylesheet" href="/omnicorp/canonical.css">',"")
    s=s.replace("</head>",'<link rel="stylesheet" href="/omnicorp/canonical.css"></head>')
    current=next((name for slug,name in chapters.items() if slug in p.parts),None)
    extra=f'<a href="{BASE}/blob/main/omnicorp/{html.escape(current,quote=True)}">Current chapter ↗</a>' if current else ""
    banner=f'<!-- canonical-home:start --><aside class="canonical-home" aria-label="Canonical documentation"><strong>Post-AI Era Vision &amp; Omnicorp</strong><p>The canonical work lives on GitHub. <a href="{BASE}/tree/main/post-ai">Post-AI vision ↗</a><a href="{BASE}/tree/main/omnicorp">Omnicorp ↗</a><a href="{BASE}/issues">Discuss &amp; contribute ↗</a>{extra}</p><small>Writing and original art: <a href="{BASE}/blob/main/ATTRIBUTION.md">Łukasz Stocki and contributors · CC BY 4.0</a></small></aside><!-- canonical-home:end -->'
    if "</header>" in s:
        s=s.replace("</header>","</header>"+banner,1)
    else:
        s,count=re.subn(r"(<body[^>]*>)",lambda m:m.group(1)+banner,s,count=1)
        assert count == 1,p
    p.write_text(s)
(ROOT/"dist/omnicorp/canonical.css").write_text('.canonical-home{margin:0 5%;padding:20px 0;border-bottom:1px solid #2a3031;font:16px/1.6 Arial,Helvetica,sans-serif;color:#a5afae;overflow-wrap:anywhere}.canonical-home strong{color:#eceee7}.canonical-home p{margin:6px 0;display:flex;flex-wrap:wrap;gap:8px 20px}.canonical-home a{color:#d9ff43;text-decoration:underline;text-underline-offset:3px}.canonical-home small{font-size:13px}\n')
print("Updated canonical links on all introduction pages.")

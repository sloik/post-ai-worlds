"""Install the reviewed public snapshot into apps-site without copying private sources.
Run after apps-site's base build and tests; then run installed build_omnicorp.py
on every future rebuild before deploying the complete dist directory.
"""
from pathlib import Path
import argparse, hashlib, json, shutil
ROOT=Path(__file__).resolve().parent
HELPER=r'''"""Merge the committed Omnicorp public snapshot after the base apps-site build."""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parent
out=ROOT/'dist';source=ROOT/'omnicorp-public'
assert (out/'index.html').is_file(), 'Run python3 build.py first'
assert (source/'index.html').is_file(), 'Missing reviewed public snapshot'
# Retain all existing app pages and assets byte for byte.
retained={str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file() and p.relative_to(out).parts[0]!='omnicorp' and p.name!='_headers'}
header=(out/'_headers').read_text()
assert '/omnicorp/*' not in header, 'Run base build before merging Omnicorp again'
lines=header.splitlines();csp=[x.strip() for x in lines if x.strip().startswith('Content-Security-Policy:')]
assert len(csp)==1, 'Review changed base security headers before publication'
# Avoid overlapping CSP policies: keep shared security headers, scope the old CSP
# to retained app routes, and give only Omnicorp its required same-origin scripts.
header='\n'.join(x for x in lines if not x.strip().startswith('Content-Security-Policy:'))+'\n'
for p in sorted(out.iterdir()):
 if p.name=='omnicorp' or p.name.startswith('_'):continue
 if p.is_dir():patterns=['/'+p.name+'/*','/'+p.name]
 elif p.suffix=='.html':patterns=['/'+p.name]+(['/'] if p.name=='index.html' else [])
 else:continue
 for pattern in patterns:header+='\n'+pattern+'\n  '+csp[0]+'\n'
header+="\n/omnicorp/*\n  Content-Security-Policy: default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self'; font-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'\n"
shutil.copytree(source,out/'omnicorp',dirs_exist_ok=True)
(out/'_headers').write_text(header)
assert all(hashlib.sha256((out/p).read_bytes()).hexdigest()==v for p,v in retained.items())
for p in source.rglob('*'):
 if p.is_file():assert p.read_bytes()==(out/'omnicorp'/p.relative_to(source)).read_bytes()
print(f'Merged Omnicorp; preserved {len(retained)} existing files byte for byte.')
'''
def main():
 parser=argparse.ArgumentParser();parser.add_argument('apps_site',type=Path);args=parser.parse_args();target=args.apps_site.resolve()
 assert (target/'build.py').is_file() and (target/'site.json').is_file()
 src=ROOT/'dist/omnicorp';assert len(list(src.rglob('*.html')))==33
 # Explicit allowlist: all input is the reviewed public dist, never content/ or docs.
 shutil.copytree(src,target/'omnicorp-public',dirs_exist_ok=True)
 (target/'build_omnicorp.py').write_text(HELPER)
 print('Installed public-only snapshot and durable merge helper.')
if __name__=='__main__':main()

"""Build the public introduction and its canonical-source links."""
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
for script in ("build_art.py","build_publications.py","build_curve.py","build_observatory.py","build_canonical_links.py"):
    subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,check=True)

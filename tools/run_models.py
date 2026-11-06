#!/usr/bin/env python3
"""Run finite TLC campaign. Writes new raw logs; never imports private receipts."""

import argparse
import json
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import check
from campaign import DEPENDENCIES, RUNS


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", required=True, type=Path)
    parser.add_argument("--java", default="java")
    parser.add_argument("--root", default=check.ROOT, type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    jar = args.jar.resolve()
    java = shutil.which(args.java)
    check.require(java is not None, "java", "Java executable required")
    check.require(
        check.digest(jar) == check.TLC_SHA256, "tool_pin", "expected pinned v1.7.4 jar"
    )
    registry = root / "worlds/registry.json"
    check.check_registry(check.load(registry))
    (root / "formal/RegistrySnapshot.tla").write_text(
        check.snapshot(check.load(registry), check.digest(registry)), encoding="utf-8"
    )
    evidence = root / "formal/evidence"
    evidence.mkdir(exist_ok=True)
    rows = []
    for run_id, model, outcome, target in RUNS:
        names = DEPENDENCIES[model] + [run_id + ".cfg"]
        with tempfile.TemporaryDirectory(
            prefix="post-ai-tlc-", dir="/tmp" if Path("/tmp").is_dir() else None
        ) as tmp:
            work = Path(tmp)
            for name in names:
                shutil.copyfile(root / "formal" / name, work / name)
            (work / "jvm").mkdir()
            command = [
                java,
                "-Djava.io.tmpdir=" + str(work / "jvm"),
                "-Xmx512m",
                "-cp",
                str(jar),
                "tlc2.TLC",
                "-workers",
                "1",
                "-seed",
                "1",
                "-metadir",
                "states",
                "-config",
                run_id + ".cfg",
                model + ".tla",
            ]
            result = subprocess.run(
                command,
                cwd=work,
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            text = (
                check.capture_header(
                    run_id,
                    model,
                    {"formal/" + n: check.digest(root / "formal" / n) for n in names},
                )
                + result.stdout
                + result.stderr
            )
            # Native output must be produced in a nonpersonal workspace; do not redact after hashing.
            check.require(
                "/Users/" not in text and "/home/" not in text,
                "private_native_path",
                "rerun in a public-safe environment",
            )
        path = evidence / (run_id + ".log")
        path.write_text(text, encoding="utf-8")
        if outcome == "lost_witness_control":
            counts = check.classify_log(text, result.returncode)
            try:
                check.classify_log(text, result.returncode, target)
            except check.Rejected:
                qualification = 1
            else:
                raise check.Rejected("lost witness control unexpectedly reached target")
        else:
            counts = check.classify_log(text, result.returncode, target)
            qualification = 0
        rows.append(
            {
                "id": run_id,
                "model": model,
                "outcome": outcome,
                "target": target,
                "exit_code": result.returncode,
                "qualification_exit": qualification,
                "counts": counts,
                "inputs": {
                    "formal/" + n: check.digest(root / "formal" / n) for n in names
                },
                "log_path": path.relative_to(root).as_posix(),
                "log_sha256": check.digest(path),
            }
        )
        print(run_id, result.returncode, qualification, flush=True)
    version = subprocess.run(
        [java, "-version"], capture_output=True, text=True, check=True
    )
    manifest = {
        "schema_version": 1,
        "scope": "bounded_models_only",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "registry_sha256": check.digest(registry),
        "tool_sha256": check.TLC_SHA256,
        "tool_url": check.TLC_URL,
        "java_version": (version.stdout + version.stderr).strip(),
        "producer_inputs": {
            n: check.digest(root / n)
            for n in ("tools/check.py", "tools/run_models.py", "tools/campaign.py")
        },
        "runs": rows,
    }
    (evidence / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    check.verify_evidence(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

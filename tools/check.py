#!/usr/bin/env python3
"""Offline structural/assurance checks. Never establishes empirical truth or full prose proof."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

KINDS = frozenset(
    {
        "candidate_instrument",
        "conditional_mechanism",
        "definition",
        "empirical_assumption",
        "empirical_report",
        "forecast_record",
        "historical_evidence",
        "hypothetical_premise",
        "navigation",
        "normative",
        "operational",
        "owner_intent_record",
        "proposed_change",
        "proposed_method",
        "dated_legal_financial_report",
        "dated_project_report",
    }
)
ASSURANCE = frozenset(
    {
        "unchecked",
        "proposed",
        "bounded_checked",
        "empirical_only",
        "normative",
        "open",
        "evidence_only",
    }
)
CLAIM_KINDS = KINDS | {"empirical_report_and_operational_proposal"}
HASH = re.compile(r"[0-9a-f]{64}\Z")


class Rejected(ValueError):
    """Stable diagnostic code plus context; no repair/write path."""


def require(condition, code, detail):
    if not condition:
        raise Rejected(f"{code}: {detail}")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def confined(root, name):
    require(isinstance(name, str) and bool(name), "path", repr(name))
    rel = Path(name)
    require(not rel.is_absolute() and ".." not in rel.parts, "path", name)
    out = (root / rel).resolve()
    require(out.is_relative_to(root.resolve()) and out.is_file(), "path", name)
    return out


def load(path):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            require(key not in out, "duplicate_json_key", key)
            out[key] = value
        return out

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def version(record, where):
    require(
        type(record.get("schema_version")) is int and record["schema_version"] == 1,
        "schema_version",
        where,
    )


def indexed(rows, where):
    require(isinstance(rows, list), "shape", where)
    out = {}
    for row in rows:
        require(isinstance(row, dict), "shape", where)
        key = row.get("id")
        require(isinstance(key, str) and bool(key), "id", where)
        require(key not in out, "duplicate_id", f"{where}/{key}")
        out[key] = row
    return out


def refs(values, known, where):
    require(
        isinstance(values, list) and all(isinstance(x, str) for x in values),
        "references",
        where,
    )
    require(len(values) == len(set(values)), "duplicate_reference", where)
    require(
        set(values) <= set(known),
        "unknown_reference",
        f"{where}: {set(values) - set(known)}",
    )
    return set(values)


def headings(text):
    """Actual ATX headings outside YAML frontmatter and fenced code, with 1-based lines."""
    out, fence = [], None
    lines = text.splitlines()
    front = bool(lines and lines[0].strip() == "---")
    for number, line in enumerate(lines, 1):
        if front:
            if number > 1 and line.strip() == "---":
                front = False
            continue
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1]:
                fence = None
            continue
        if fence:
            continue
        match = re.match(r"^ {0,3}(#{1,6})\s+(.+?)\s*$", line)
        if match:
            title = re.sub(r"\s+#+\s*$", "", match.group(2))
            out.append({"level": len(match.group(1)), "text": title, "line": number})
    return out


def classify_log(text, exit_code, target=None):
    require(type(exit_code) is int, "native_exit_type", repr(exit_code))
    errors = re.findall(r"^Error:\s*(.*)$", text, re.MULTILINE)
    forbidden = (
        "Parsing or semantic analysis failed",
        "SANY failed",
        "Exception",
        "OutOfMemory",
        "TLC threw",
        "Error in configuration",
        "Attempted to",
        "Temporal properties were violated",
        "*** Errors",
        "***Parse Error",
        "Semantic errors",
        "Successor state is not completely specified",
    )
    require(
        not any(word in text for word in forbidden),
        "native_diagnostic",
        "unexpected tool/temporal error",
    )
    require(
        "TLC2 Version" in text and "Finished in" in text,
        "native_incomplete",
        "missing tool/completion marker",
    )
    counts = re.findall(
        r"([\d,]+) states generated, ([\d,]+) distinct states found", text
    )
    require(bool(counts), "native_incomplete", "missing explored-state counts")
    generated, distinct = (int(x.replace(",", "")) for x in counts[-1])
    require(generated > 0 and distinct > 0, "native_empty", "zero explored states")
    if target is None:
        require(
            exit_code == 0
            and not errors
            and "Model checking completed. No error has been found." in text,
            "native_not_pass",
            "expected completed clean model check",
        )
    else:
        require(target != "TypeOK", "native_target", "TypeOK is not a semantic control")
        require(
            exit_code == 12
            and errors
            == [
                f"Invariant {target} is violated.",
                "The behavior up to this point is:",
            ],
            "native_wrong_counterexample",
            repr(errors),
        )
        require(
            re.search(r"^State 1: <Initial predicate>", text, re.MULTILINE) is not None
            and re.search(r"^State 2:", text, re.MULTILINE) is not None,
            "native_no_behavior",
            "missing concrete noninitial counterexample",
        )
    return {"generated": generated, "distinct": distinct}


def tla_set(items):
    return "{" + ", ".join(json.dumps(x) for x in sorted(items)) + "}"


def snapshot(registry, sha):
    """Literal declared premises, not inferred empirical truth. Hash binds all input fields."""
    universes, claims = registry["universes"], registry["claims"]
    shared = set(registry.get("shared_normative_ids", []))
    pairs = {tuple(sorted(pair)) for pair in registry["conflicts"]}
    pairs.update(
        tuple(sorted((row["id"], other)))
        for row in registry["assumptions"]
        for other in row["incompatible_with"]
    )
    lines = [
        "--------------------------- MODULE RegistrySnapshot ---------------------------",
        "EXTENDS FiniteSets",
        "\\* Actual registry sha256: " + sha,
        "UniverseIds == " + tla_set(u["id"] for u in universes),
        "ClaimIds == " + tla_set(c["id"] for c in claims),
    ]
    for name, rows, field in [
        ("DeclaredPremises", universes, "assumption_ids"),
        ("RequiredPremises", claims, "assumption_ids"),
    ]:
        value = lambda r, field=field, name=name: tla_set(
            set(r[field]) | (shared if name == "DeclaredPremises" else set())
        )
        lines.append(
            name
            + " == [id \\in "
            + ("UniverseIds" if name == "DeclaredPremises" else "ClaimIds")
            + " |-> CASE "
            + "\n    [] ".join(
                "id = " + json.dumps(r["id"]) + " -> " + value(r) for r in rows
            )
            + "]"
        )
    lines.append(
        "ConflictPairs == {" + ", ".join(tla_set(p) for p in sorted(pairs)) + "}"
    )
    lines.append(
        "AdmissionRules == {"
        + ",\n ".join(
            "[requires |-> "
            + tla_set(r["if_all"])
            + ", ensures |-> "
            + tla_set(r["then_all"])
            + ", forbids |-> "
            + tla_set(r["forbid_all"])
            + "]"
            for r in registry["rules"]
        )
        + "}"
    )
    return (
        "\n".join(lines)
        + "\n=============================================================================\n"
    )


from campaign import DEPENDENCIES, RUNS

ROOT = Path(__file__).resolve().parents[1]
TLC_SHA256 = "936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88"
TLC_URL = "https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar"


def check_registry(registry):
    version(registry, "registry")
    universes = indexed(registry["universes"], "universes")
    assumptions = indexed(registry["assumptions"], "assumptions")
    claims = indexed(registry["claims"], "claims")
    require(bool(universes) and bool(assumptions) and bool(claims), "empty", "registry")
    shared = refs(registry["shared_normative_ids"], assumptions, "shared")
    require(
        all(assumptions[a]["kind"] in {"normative", "operational"} for a in shared),
        "shared_kind",
        "normative or operational decisions only",
    )
    aliases = set(universes)
    for row in universes.values():
        require(isinstance(row["legacy_aliases"], list), "alias_shape", row["id"])
        for alias in row["legacy_aliases"]:
            require(
                isinstance(alias, str) and bool(alias) and alias not in aliases,
                "duplicate_alias",
                row["id"],
            )
            aliases.add(alias)
    conflicts = set()
    for row in assumptions.values():
        require(
            row["kind"]
            in {"normative", "operational", "empirical_assumption", "hypothetical"},
            "assumption_kind",
            row["id"],
        )
        for other in refs(row["incompatible_with"], assumptions, row["id"]):
            require(other != row["id"], "self_conflict", row["id"])
            conflicts.add(frozenset((row["id"], other)))
    for pair in registry["conflicts"]:
        require(
            len(refs(pair, assumptions, "conflicts")) == 2, "conflict_pair", repr(pair)
        )
        conflicts.add(frozenset(pair))
    rules = indexed(registry["rules"], "rules")
    for rule in rules.values():
        for field in ("if_all", "then_all", "forbid_all"):
            refs(rule[field], assumptions, rule["id"])
    for claim in claims.values():
        require(claim["kind"] in CLAIM_KINDS, "claim_kind", claim["id"])
        refs(claim["assumption_ids"], assumptions, claim["id"])
        refs(claim["universe_ids"], universes, claim["id"])
        require(
            claim["assurance_status"] in ASSURANCE - {"bounded_checked"},
            "false_proof",
            claim["id"],
        )
    for uid, row in universes.items():
        require(re.fullmatch(r"OMNI-\d{3}", uid) is not None, "universe_id", uid)
        require(type(row["version"]) is int and row["version"] >= 1, "version", uid)
        require(row["assurance_status"] == "unchecked", "false_proof", uid)
        require(
            isinstance(row["lineage_note"], str) and bool(row["lineage_note"].strip()),
            "lineage_note",
            uid,
        )
        parent = row["parent_id"]
        require(parent is None or parent in universes, "parent", uid)
        if parent is not None:
            require(
                type(universes[parent]["version"]) is int
                and row["version"] > universes[parent]["version"],
                "lineage_version",
                uid,
            )
        seen = {uid}
        while parent is not None:
            require(parent not in seen, "lineage_cycle", uid)
            seen.add(parent)
            parent = universes[parent]["parent_id"]
        premises = refs(row["assumption_ids"], assumptions, uid) | shared
        require(
            not any(pair <= premises for pair in conflicts), "premise_conflict", uid
        )
        for rule in rules.values():
            if set(rule["if_all"]) <= premises:
                require(
                    set(rule["then_all"]) <= premises
                    and not set(rule["forbid_all"]) & premises,
                    "admission_rule",
                    uid + "/" + rule["id"],
                )
        for cid in refs(row["admitted_claim_ids"], claims, uid):
            require(
                set(claims[cid]["assumption_ids"]) <= premises,
                "silent_import",
                uid + "/" + cid,
            )


def inventory(root):
    """Mechanical inventory only; no semantic classification is generated."""
    return {
        p.relative_to(root).as_posix(): {
            "sha256": digest(p),
            "headings": headings(p.read_text(encoding="utf-8")),
            "assurance": "editorial_inventory_only",
        }
        for folder in ("post-ai", "omnicorp")
        for p in sorted((root / folder).rglob("*.md"))
    }


def check_inventory(root):
    manifest = load(root / "worlds/coverage.json")
    version(manifest, "coverage")
    actual = inventory(root)
    require(
        actual == manifest["documents"],
        "source_inventory_drift",
        "file set, bytes or actual headings changed",
    )
    mapping = load(root / "worlds/mapping.json")
    version(mapping, "mapping")
    require(
        set(mapping["documents"]) == set(actual),
        "mapping_coverage",
        "all public documents need relevance dispositions",
    )
    known = indexed(load(root / "worlds/registry.json")["universes"], "universes")
    for path, row in mapping["documents"].items():
        refs(row["universe_ids"], known, path)
        require(row["assurance"] == "not_modelled", "false_proof", path)
        require(
            isinstance(row["limits"], str) and bool(row["limits"].strip()),
            "mapping_limits",
            path,
        )


def check_links(root):
    from urllib.parse import unquote

    for p in root.rglob("*.md"):
        if any(part.startswith(".") for part in p.relative_to(root).parts):
            continue
        for target in re.findall(
            r"\]\(([^\s)]+)(?:\s+[^)]*)?\)", p.read_text(encoding="utf-8")
        ):
            if re.match(r"^[a-zA-Z]+:", target) or target.startswith("#"):
                continue
            rel = target.split("#")[0]
            resolved = (p.parent / unquote(rel)).resolve()
            require(
                resolved.is_relative_to(root.resolve()) and resolved.exists(),
                "broken_link",
                str(p.relative_to(root)) + ": " + target,
            )


def capture_header(run_id, model, inputs):
    """Producer receipt followed by unmodified native stdout+stderr; not attestation."""
    return (
        "POST_AI_CAPTURE "
        + json.dumps(
            {"id": run_id, "model": model, "inputs": inputs},
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    )


def verify_evidence(root):
    manifest = load(root / "formal/evidence/manifest.json")
    version(manifest, "native manifest")
    require(manifest["scope"] == "bounded_models_only", "formal_scope", "scope")
    require(manifest["tool_sha256"] == TLC_SHA256, "tool_pin", "jar hash")
    require(
        manifest["registry_sha256"] == digest(root / "worlds/registry.json"),
        "registry_evidence_drift",
        "registry",
    )
    require(
        (root / "formal/RegistrySnapshot.tla").read_text(encoding="utf-8")
        == snapshot(
            load(root / "worlds/registry.json"), digest(root / "worlds/registry.json")
        ),
        "snapshot_drift",
        "registry abstraction",
    )
    # Bind the producer/classifier code as well as models; this does not authenticate who ran a process.
    for path, sha in manifest["producer_inputs"].items():
        require(digest(confined(root, path)) == sha, "producer_drift", path)
    require(
        set(manifest["producer_inputs"])
        == {"tools/check.py", "tools/run_models.py", "tools/campaign.py"},
        "producer_set",
        "expected producer sources",
    )
    rows = indexed(manifest["runs"], "native runs")
    require(
        set(rows) == {r[0] for r in RUNS}, "campaign_incomplete", "12 required cases"
    )
    for run_id, model, outcome, target in RUNS:
        row = rows[run_id]
        require(
            (row["model"], row["outcome"], row["target"]) == (model, outcome, target),
            "campaign_case",
            run_id,
        )
        wanted = {"formal/" + n for n in DEPENDENCIES[model] + [run_id + ".cfg"]}
        require(set(row["inputs"]) == wanted, "source_set", run_id)
        for path, sha in row["inputs"].items():
            require(digest(confined(root, path)) == sha, "model_drift", path)
        require(
            row["log_path"] == "formal/evidence/" + run_id + ".log", "log_path", run_id
        )
        log = confined(root, row["log_path"])
        require(digest(log) == row["log_sha256"], "log_drift", run_id)
        text = log.read_text(encoding="utf-8")
        require(
            text.startswith(capture_header(run_id, model, row["inputs"])),
            "native_capture_identity",
            run_id,
        )
        parsed = re.findall(
            r"^Semantic processing of module (\w+)$", text, re.MULTILINE
        )
        expected_modules = {Path(n).stem for n in DEPENDENCIES[model]}
        require(
            expected_modules <= set(parsed) and parsed[-1:] == [model],
            "native_model_identity",
            run_id,
        )
        require(
            "ScenarioContracts" not in parsed
            if model == "OperationalGates"
            else "OperationalGates" not in parsed,
            "native_model_identity",
            run_id,
        )
        require(
            ("Finished checking temporal properties" in text)
            == (run_id == "operations-progress"),
            "native_temporal_identity",
            run_id,
        )
        require(type(row["qualification_exit"]) is int, "qualification_type", run_id)
        if outcome == "lost_witness_control":
            counts = classify_log(text, row["exit_code"])
            try:
                classify_log(text, row["exit_code"], target)
            except Rejected:
                pass
            else:
                raise Rejected("lost_witness: unexpectedly reachable")
            require(row["qualification_exit"] == 1, "lost_witness", run_id)
        else:
            counts = classify_log(text, row["exit_code"], target)
            require(row["qualification_exit"] == 0, "qualification", run_id)
        require(
            row["counts"] == counts
            and all(type(x) is int for x in row["counts"].values()),
            "state_counts",
            run_id,
        )
    return len(rows)


def validate(root, native=True):
    check_registry(load(root / "worlds/registry.json"))
    check_inventory(root)
    check_links(root)
    return verify_evidence(root) if native else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        count = validate(args.root.resolve())
    except (Rejected, KeyError, TypeError, ValueError, OSError) as error:
        print("REJECTED:", error)
        return 1
    print(
        f"PASS: public inventory, registry, links and {count} native cases. No empirical or whole-prose proof."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Adversarial controls for public registry, inventory and native evidence."""

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import check

ROOT = Path(__file__).resolve().parents[1]


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.r = check.load(ROOT / "worlds/registry.json")

    def rejects(self):
        with self.assertRaises((check.Rejected, KeyError, TypeError)):
            check.check_registry(self.r)

    def test_real(self):
        check.check_registry(self.r)

    def test_conflicting_same_scope(self):
        self.r["universes"][1]["assumption_ids"] += ["ASM-005"]
        self.rejects()

    def test_silent_import(self):
        self.r["universes"][0]["admitted_claim_ids"] = ["CLM-002"]
        self.rejects()

    def test_false_whole_world_proof(self):
        self.r["universes"][0]["assurance_status"] = "bounded_checked"
        self.rejects()

    def test_false_claim_proof(self):
        self.r["claims"][0]["assurance_status"] = "bounded_checked"
        self.rejects()

    def test_unknown_premise(self):
        self.r["claims"][0]["assumption_ids"] = ["ASM-UNKNOWN"]
        self.rejects()

    def test_duplicate_universe(self):
        self.r["universes"].append(copy.deepcopy(self.r["universes"][0]))
        self.rejects()

    def test_parent_cycle(self):
        a, b = self.r["universes"][:2]
        a["parent_id"] = b["id"]
        b["parent_id"] = a["id"]
        self.rejects()

    def test_bool_version(self):
        self.r["universes"][0]["version"] = True
        self.rejects()

    def test_invalid_claim_kind(self):
        self.r["claims"][0]["kind"] = "formally_proved_empirical_law"
        self.rejects()

    def test_invalid_assumption_kind(self):
        self.r["assumptions"][0]["kind"] = "magic"
        self.rejects()

    def test_duplicate_legacy_alias(self):
        self.r["universes"][1]["legacy_aliases"] = ["U1"]
        self.rejects()

    def test_heading_fences(self):
        self.assertEqual(
            check.headings(
                "---\nx: y\n---\n# Real\n```md\n# Fake\n```\n  ## Next ###\n"
            ),
            [
                {"level": 1, "text": "Real", "line": 4},
                {"level": 2, "text": "Next", "line": 8},
            ],
        )

    def test_duplicate_json_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.json"
            p.write_text('{"x":1,"x":2}')
            with self.assertRaises(check.Rejected):
                check.load(p)


class NativeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for folder in ("tools", "formal", "worlds", "post-ai", "omnicorp"):
            shutil.copytree(
                ROOT / folder,
                self.root / folder,
                ignore=shutil.ignore_patterns("__pycache__"),
            )
        self.manifest = check.load(self.root / "formal/evidence/manifest.json")

    def reject(self):
        (self.root / "formal/evidence/manifest.json").write_text(
            json.dumps(self.manifest)
        )
        with self.assertRaises((check.Rejected, KeyError, TypeError)):
            check.verify_evidence(self.root)

    def test_real_retained_native(self):
        self.assertEqual(check.verify_evidence(self.root), 12)

    def test_omitted_native_case(self):
        self.manifest["runs"].pop()
        self.reject()

    def test_bool_native_exit(self):
        self.manifest["runs"][0]["exit_code"] = False
        self.reject()

    def test_float_counterexample_exit(self):
        self.manifest["runs"][1]["exit_code"] = 12.0
        self.reject()

    def test_bool_qualification(self):
        self.manifest["runs"][0]["qualification_exit"] = False
        self.reject()

    def test_changed_model(self):
        p = self.root / "formal/OperationalGates.tla"
        p.write_text(p.read_text() + "\n")
        self.reject()

    def test_changed_producer(self):
        p = self.root / "tools/run_models.py"
        p.write_text(p.read_text() + "\n")
        self.reject()

    def test_registry_drift(self):
        p = self.root / "worlds/registry.json"
        p.write_text(p.read_text() + "\n")
        self.reject()

    def test_named_counterexample_with_extra_error(self):
        row = self.manifest["runs"][1]
        p = self.root / row["log_path"]
        p.write_text(p.read_text() + "\nError: Unexpected failure.\n")
        row["log_sha256"] = check.digest(p)
        self.reject()

    def test_counterexample_with_temporal_failure(self):
        row = self.manifest["runs"][1]
        p = self.root / row["log_path"]
        p.write_text(p.read_text() + "\nError: Temporal properties were violated.\n")
        row["log_sha256"] = check.digest(p)
        self.reject()

    def test_missing_positive_completion(self):
        row = self.manifest["runs"][0]
        p = self.root / row["log_path"]
        p.write_text(p.read_text().replace("Finished in", "Interrupted in"))
        row["log_sha256"] = check.digest(p)
        self.reject()

    def test_lost_witness_is_rejected_reachability(self):
        row = self.manifest["runs"][-1]
        self.assertEqual(row["exit_code"], 0)
        self.assertEqual(row["qualification_exit"], 1)
        text = (self.root / row["log_path"]).read_text()
        with self.assertRaises(check.Rejected):
            check.classify_log(text, 0, row["target"])

    def test_wrong_model_log(self):
        row = next(r for r in self.manifest["runs"] if r["id"] == "operations-safe")
        other = self.manifest["runs"][0]
        p = self.root / row["log_path"]
        p.write_bytes((self.root / other["log_path"]).read_bytes())
        row["log_sha256"] = check.digest(p)
        row["counts"] = other["counts"]
        self.reject()

    def test_lost_witness_swapped_with_unchecked_safe_case(self):
        row = self.manifest["runs"][-1]
        other = next(r for r in self.manifest["runs"] if r["id"] == "operations-safe")
        p = self.root / row["log_path"]
        p.write_bytes((self.root / other["log_path"]).read_bytes())
        row["log_sha256"] = check.digest(p)
        row["counts"] = other["counts"]
        self.reject()

    def test_wrong_temporal_case_log(self):
        row = next(r for r in self.manifest["runs"] if r["id"] == "operations-progress")
        other = next(r for r in self.manifest["runs"] if r["id"] == "operations-safe")
        p = self.root / row["log_path"]
        p.write_bytes((self.root / other["log_path"]).read_bytes())
        row["log_sha256"] = check.digest(p)
        row["counts"] = other["counts"]
        self.reject()

    def test_nested_document_escapes_nothing(self):
        folder = self.root / "post-ai/nested"
        folder.mkdir()
        (folder / "chapter.md").write_text("# New chapter")
        with self.assertRaises(check.Rejected):
            check.check_inventory(self.root)

    def test_root_broken_link(self):
        (self.root / "README.md").write_text("[Broken](missing.md)")
        with self.assertRaises(check.Rejected):
            check.check_links(self.root)

    def test_omitted_document(self):
        p = next((self.root / "post-ai").glob("*.md"))
        p.unlink()
        with self.assertRaises(check.Rejected):
            check.check_inventory(self.root)

    def test_stale_document(self):
        p = next((self.root / "omnicorp").glob("*.md"))
        p.write_text(p.read_text() + "\n")
        with self.assertRaises(check.Rejected):
            check.check_inventory(self.root)


if __name__ == "__main__":
    unittest.main()

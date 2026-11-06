"""Controls for document-link coverage and private/untracked-source exclusion."""

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

s = importlib.util.spec_from_file_location(
    "navigation", Path(__file__).resolve().parents[1] / "tools/build_navigation.py"
)
nav = importlib.util.module_from_spec(s)
s.loader.exec_module(nav)


class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.r = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", str(self.r)], check=True)
        files = {
            "README.md": "# Home\n[Vision](post-ai/README.md)\n",
            "CANONICAL.md": f"# Current home\n{nav.REPOSITORY}\n[post-ai/](post-ai/README.md)\n[omnicorp/](omnicorp/README.md)\n",
            "post-ai/README.md": "# Society\n[Organisation](../omnicorp/README.md)\n",
            "omnicorp/README.md": "# Organisation\n",
        }
        for name, text in files.items():
            p = self.r / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        subprocess.run(["git", "-C", str(self.r), "add", "."], check=True)
        (self.r / "graphs").mkdir()
        self.save(nav.build(self.r))

    def save(self, data):
        (self.r / nav.OUTPUT).write_text(json.dumps(data))

    def test_actual_routes_and_links(self):
        data = nav.build(self.r)
        nav.verify(self.r)
        self.assertEqual(
            {x["target"] for x in data["links"] if x["relation"] == "canonical_track"},
            {"post-ai/README.md", "omnicorp/README.md"},
        )
        self.assertTrue(
            any(
                x["source"] == "post-ai/README.md"
                and x["target"] == "omnicorp/README.md"
                for x in data["links"]
            )
        )

    def test_untracked_private_note_excluded(self):
        (self.r / "private.md").write_text("# Private title that must not leak")
        self.assertNotIn("private.md", {x["id"] for x in nav.build(self.r)["nodes"]})
        nav.verify(self.r)

    def test_missing_track_refused(self):
        subprocess.run(
            ["git", "-C", str(self.r), "rm", "--cached", "omnicorp/README.md"],
            check=True,
            capture_output=True,
        )
        with self.assertRaises(ValueError):
            nav.build(self.r)

    def test_source_drift_refused(self):
        p = self.r / "post-ai/README.md"
        p.write_text(p.read_text() + "changed\n")
        with self.assertRaises(ValueError):
            nav.verify(self.r)

    def test_omitted_node_refused(self):
        data = nav.build(self.r)
        data["nodes"].pop()
        self.save(data)
        with self.assertRaises(ValueError):
            nav.verify(self.r)

    def test_wrong_home_refused(self):
        data = nav.build(self.r)
        data["canonical_repository"] = "https://example.invalid"
        self.save(data)
        with self.assertRaises(ValueError):
            nav.verify(self.r)

    def test_symlink_source_refused(self):
        p = self.r / "README.md"
        p.unlink()
        p.symlink_to(self.r / "CANONICAL.md")
        with self.assertRaises(ValueError):
            nav.build(self.r)

    def test_canonical_symlink_rejected_before_any_source_read(self):
        p = self.r / "CANONICAL.md"
        p.unlink()
        p.symlink_to(self.r / "README.md")
        with patch.object(
            Path,
            "read_bytes",
            side_effect=AssertionError("source read before path validation"),
        ):
            with self.assertRaises(ValueError):
                nav.build(self.r)

    def test_fenced_and_inline_examples_are_not_edges(self):
        p = self.r / "omnicorp/README.md"
        p.write_text(
            "# Organisation\n```md\n[Example](../post-ai/README.md)\n```\n`[Example](../post-ai/README.md)`\n"
        )
        data = nav.build(self.r)
        self.assertFalse(
            any(
                e["source"] == "omnicorp/README.md"
                and e["target"] == "post-ai/README.md"
                for e in data["links"]
            )
        )

    def test_declaration_provenance_not_falsely_line_bound(self):
        p = self.r / "CANONICAL.md"
        p.write_text("\n\n" + p.read_text())
        data = nav.build(self.r)
        self.assertEqual(data["nodes"][0]["provenance"], "CANONICAL.md")
        self.assertTrue(
            all(
                "source_location" not in e
                for e in data["links"]
                if e["relation"] == "canonical_track"
            )
        )


if __name__ == "__main__":
    unittest.main()

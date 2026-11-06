"""Adversarial predicate controls; real runner routing is verified separately."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "oracle_guard", Path(__file__).resolve().parents[1] / "ci/oracle_job_guard.py"
)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class OracleGuardTests(unittest.TestCase):
    def setUp(self):
        self.env = {
            "GITHUB_SERVER_URL": "https://github.com",
            "GITHUB_REPOSITORY": guard.REPOSITORY,
            "GITHUB_REF": "refs/heads/main",
            "GITHUB_WORKFLOW_REF": guard.WORKFLOW,
            "GITHUB_EVENT_NAME": "push",
        }
        self.event = {
            "repository": {
                "id": guard.REPOSITORY_ID,
                "full_name": guard.REPOSITORY,
                "fork": False,
            },
            "ref": "refs/heads/main",
            "deleted": False,
        }

    def test_main_push(self):
        self.assertTrue(guard.admit(self.env, self.event))

    def test_main_dispatch(self):
        self.env["GITHUB_EVENT_NAME"] = "workflow_dispatch"
        self.event["ref"] = "main"
        self.assertTrue(guard.admit(self.env, self.event))

    def test_pr_event_even_if_ref_spoofed_main(self):
        self.env["GITHUB_EVENT_NAME"] = "pull_request"
        self.assertFalse(guard.admit(self.env, self.event))

    def test_pr_target(self):
        self.env["GITHUB_EVENT_NAME"] = "pull_request_target"
        self.assertFalse(guard.admit(self.env, self.event))

    def test_custom_branch(self):
        self.env["GITHUB_REF"] = "refs/heads/experiment"
        self.assertFalse(guard.admit(self.env, self.event))

    def test_custom_workflow(self):
        self.env["GITHUB_WORKFLOW_REF"] = (
            guard.REPOSITORY + "/.github/workflows/other.yml@refs/heads/main"
        )
        self.assertFalse(guard.admit(self.env, self.event))

    def test_pr_payload_even_with_main_env(self):
        self.event["pull_request"] = {}
        self.assertFalse(guard.admit(self.env, self.event))

    def test_fork_payload(self):
        self.event["repository"]["fork"] = True
        self.assertFalse(guard.admit(self.env, self.event))

    def test_wrong_numeric_repository(self):
        self.event["repository"]["id"] += 1
        self.assertFalse(guard.admit(self.env, self.event))

    def test_boolean_repository_id(self):
        self.event["repository"]["id"] = True
        self.assertFalse(guard.admit(self.env, self.event))

    def test_deleted_main(self):
        self.event["deleted"] = True
        self.assertFalse(guard.admit(self.env, self.event))

    def test_missing_context(self):
        self.assertFalse(guard.admit({}, {}))

    def test_dispatch_payload_wrong_ref(self):
        self.env["GITHUB_EVENT_NAME"] = "workflow_dispatch"
        self.event["ref"] = "experiment"
        self.assertFalse(guard.admit(self.env, self.event))

    def test_wrong_server(self):
        self.env["GITHUB_SERVER_URL"] = "https://example.invalid"
        self.assertFalse(guard.admit(self.env, self.event))

    def test_wrong_name(self):
        self.env["GITHUB_REPOSITORY"] = "other/post-ai-worlds"
        self.assertFalse(guard.admit(self.env, self.event))

    def test_tag_named_main(self):
        self.env["GITHUB_REF"] = "refs/tags/main"
        self.assertFalse(guard.admit(self.env, self.event))

    def test_workflow_run(self):
        self.env["GITHUB_EVENT_NAME"] = "workflow_run"
        self.assertFalse(guard.admit(self.env, self.event))

    def cli(self, path):
        return subprocess.run(
            [sys.executable, "-I", guard.__file__],
            env={**self.env, "GITHUB_EVENT_PATH": str(path)},
            capture_output=True,
            text=True,
            check=False,
        )

    def test_cli_valid_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "event.json"
            p.write_text(json.dumps(self.event))
            result = self.cli(p)
        self.assertEqual(result.returncode, 0)
        self.assertIn("accepted", result.stdout)

    def test_cli_missing_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.cli(Path(tmp) / "missing.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("rejected", result.stdout)

    def test_cli_malformed_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "event.json"
            p.write_text("not-json")
            result = self.cli(p)
        self.assertEqual(result.returncode, 1)
        self.assertIn("rejected", result.stdout)


if __name__ == "__main__":
    unittest.main()

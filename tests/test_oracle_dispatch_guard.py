import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

GUARD = Path(__file__).resolve().parents[1] / "ci/oracle_job_guard.py"
spec = importlib.util.spec_from_file_location("post_ai_admission", GUARD)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def environment(kind="workflow_run"):
    return {"GITHUB_SERVER_URL": "https://github.com", "GITHUB_REPOSITORY": g.REPOSITORY,
            "GITHUB_REF": g.MAIN_REF, "GITHUB_EVENT_NAME": kind,
            "GITHUB_WORKFLOW_REF": g.WORKFLOWS[kind], "GITHUB_WORKFLOW_SHA": "a" * 40}


def event(kind="workflow_run", source="pull_request"):
    value = {"repository": {"id": g.REPOSITORY_ID, "full_name": g.REPOSITORY, "fork": False}}
    if kind == "workflow_dispatch":
        value["ref"] = "main"
    else:
        value.update(action="completed", workflow_run={
            "id": 12345, "name": "Public research checks", "event": source,
            "status": "completed", "conclusion": "success", "head_sha": "b" * 40,
            "head_branch": "untrusted-feature", "head_repository": {"full_name": "fork/post-ai-worlds", "fork": True},
            "pull_requests": [{"number": 123, "head": {"sha": "b" * 40}}],
        })
    return value


class Admission(unittest.TestCase):
    def test_known_retired_dispatcher_epoch_is_refused_by_real_entrypoint(self):
        retired = "a1c4e8f09bebcce22a97bc4e69d87a1c40b6e404"
        for kind in ("workflow_run", "workflow_dispatch"):
            with self.subTest(kind=kind):
                env = environment(kind); env["GITHUB_WORKFLOW_SHA"] = retired
                result = self.invoke(json.dumps(event(kind)).encode(), env)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("rejected (retired-workflow-sha)", result.stdout)

    def test_current_and_future_workflow_epochs_keep_existing_admission(self):
        current = "04d6d80f62da0e92367e5a476d4dde1e141d1362"
        for kind in ("workflow_run", "workflow_dispatch"):
            for workflow in (current, "f" * 40):
                with self.subTest(kind=kind, workflow=workflow):
                    env = environment(kind); env["GITHUB_WORKFLOW_SHA"] = workflow
                    payload = event(kind)
                    if kind == "workflow_run":
                        payload["workflow_run"]["head_sha"] = "a1c4e8f09bebcce22a97bc4e69d87a1c40b6e404"
                    result = self.invoke(json.dumps(payload).encode(), env)
                    self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_manual_main(self):
        for ref in ("main", g.MAIN_REF):
            e = event("workflow_dispatch"); e["ref"] = ref
            self.assertTrue(g.admit(environment("workflow_dispatch"), e))

    def test_completed_push_and_fork_pr_use_main_executable(self):
        for source in ("push", "pull_request"):
            self.assertTrue(g.admit(environment(), event(source=source)))

    def test_failed_upstream_can_publish_failure_without_queue(self):
        for conclusion in ("failure", "cancelled", "timed_out", "skipped", "action_required"):
            e = event(); e["workflow_run"]["conclusion"] = conclusion
            self.assertTrue(g.admit(environment(), e))

    def test_subject_sha_is_not_workflow_sha(self):
        self.assertNotEqual(event()["workflow_run"]["head_sha"], environment()["GITHUB_WORKFLOW_SHA"])
        self.assertTrue(g.admit(environment(), event()))

    def test_context_overrides_payload_claims(self):
        edits = {
            "GITHUB_SERVER_URL": ["https://ghe.example", ""],
            "GITHUB_REPOSITORY": ["fork/post-ai-worlds", "sloik/superforecasting", "sloik/EitherSwift"],
            "GITHUB_REF": ["refs/heads/feature", "refs/pull/123/merge", "refs/tags/main", ""],
            "GITHUB_WORKFLOW_REF": [g.WORKFLOWS["workflow_dispatch"],
                g.WORKFLOWS["workflow_run"].replace("@refs/heads/main", "@refs/heads/feature"),
                g.WORKFLOWS["workflow_run"].replace("oracle-pr-tla.yml", "checks.yml"),
                g.WORKFLOWS["workflow_run"].replace("sloik/", "fork/"), ""],
            "GITHUB_EVENT_NAME": ["push", "pull_request", "pull_request_target", "schedule", "repository_dispatch", ""],
            "GITHUB_WORKFLOW_SHA": ["", "a" * 39, "a" * 41, "g" * 40, "0" * 40, "main"],
        }
        for key, values in edits.items():
            for value in values:
                with self.subTest(key=key, value=value):
                    env = environment(); env[key] = value
                    e = event(); e.update(ref=g.MAIN_REF, workflow_ref=g.WORKFLOWS["workflow_run"])
                    self.assertFalse(g.admit(env, e))

    def test_missing_context(self):
        for key in environment():
            with self.subTest(key=key):
                env = environment(); del env[key]
                self.assertFalse(g.admit(env, event()))

    def test_registration_never_uses_caller_allowlist(self):
        env = environment(); env.update(SWIFT_TLA_REPO="EitherSwift", ORACLE_ALLOWED_REPOSITORY="fork/post-ai-worlds")
        self.assertTrue(g.admit(env, event()))
        env["GITHUB_REPOSITORY"] = "fork/post-ai-worlds"
        self.assertFalse(g.admit(env, event()))

    def test_wrong_repository_payload(self):
        for key, values in {"id": [True, "1448630173", 1], "full_name": ["fork/post-ai-worlds", "sloik/EitherSwift"],
                            "fork": [True, "false", None]}.items():
            for value in values:
                with self.subTest(key=key, value=value):
                    e = event(); e["repository"][key] = value
                    self.assertFalse(g.admit(environment(), e))
        for repo in (None, [], {}, "sloik/post-ai-worlds"):
            e = event(); e["repository"] = repo
            self.assertFalse(g.admit(environment(), e))

    def test_source_envelope_failure(self):
        for key, values in {"id": [True, 0, -1, "12345"], "name": ["Oracle source verification", "other"],
                            "status": ["in_progress", "queued", None], "event": ["workflow_dispatch", "workflow_run", "pull_request_target", {}],
                            "head_sha": ["main", "0" * 40, None]}.items():
            for value in values:
                with self.subTest(key=key, value=value):
                    e = event(); e["workflow_run"][key] = value
                    self.assertFalse(g.admit(environment(), e))
        for value in (None, [], "123", {}):
            e = event(); e["workflow_run"] = value
            self.assertFalse(g.admit(environment(), e))
        for action in ("requested", "in_progress", ""):
            e = event(); e["action"] = action
            self.assertFalse(g.admit(environment(), e))

    def test_direct_pr_payload_and_deleted_ref_refused(self):
        for field, value in (("pull_request", {}), ("deleted", True), ("deleted", None)):
            e = event(); e[field] = value
            self.assertFalse(g.admit(environment(), e))

    def test_manual_wrong_workflow_ref_or_payload(self):
        env = environment("workflow_dispatch"); env["GITHUB_WORKFLOW_REF"] = g.WORKFLOWS["workflow_run"]
        self.assertFalse(g.admit(env, event("workflow_dispatch")))
        for ref in ("feature", "refs/heads/feature", {}, None):
            e = event("workflow_dispatch"); e["ref"] = ref
            self.assertFalse(g.admit(environment("workflow_dispatch"), e))
        e = event("workflow_dispatch"); e["workflow_run"] = event()["workflow_run"]
        self.assertFalse(g.admit(environment("workflow_dispatch"), e))

    def test_non_object_event(self):
        for value in (None, [], "payload", 1):
            self.assertFalse(g.admit(environment(), value))

    def invoke(self, payload, env=None, cwd=None):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary, "event.json"); path.write_bytes(payload)
            return subprocess.run([sys.executable, "-I", "-B", str(GUARD)],
                env={**(env or environment()), "GITHUB_EVENT_PATH": str(path)}, cwd=cwd,
                capture_output=True, text=True, timeout=5)

    def test_real_hook_invocation_admits_and_rejects_before_any_step(self):
        result = self.invoke(json.dumps(event()).encode())
        self.assertEqual(result.returncode, 0, result.stderr)
        env = environment(); env["GITHUB_REF"] = "refs/heads/feature"
        result = self.invoke(json.dumps(event()).encode(), env)
        self.assertEqual(result.returncode, 1)
        self.assertIn("rejected (ref)", result.stdout)

    def test_malformed_duplicate_oversized_deep_payload(self):
        for payload in (b"not json", b'{"repository":{},"repository":{}}', b'{"x":{"id":1,"id":2}}',
                        b" " * (g.MAX_EVENT_BYTES + 1), b"[" * 2000, b"\xff"):
            with self.subTest(size=len(payload)):
                result = self.invoke(payload)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_isolated_python_ignores_candidate_module_and_env(self):
        with tempfile.TemporaryDirectory() as temporary:
            Path(temporary, "json.py").write_text("raise RuntimeError('candidate imported')")
            env = environment(); env["PYTHONPATH"] = temporary
            result = self.invoke(json.dumps(event()).encode(), env, temporary)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()

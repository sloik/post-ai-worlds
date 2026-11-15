"""Root-owned Post-AI job admission; source verification belongs to the dispatcher."""

import json
import os
import re
from pathlib import Path

REPOSITORY = "sloik/post-ai-worlds"
REPOSITORY_ID = 1448630173
MAIN_REF = "refs/heads/main"
WORKFLOWS = {
    "workflow_dispatch": REPOSITORY + "/.github/workflows/oracle-tla.yml@" + MAIN_REF,
    "workflow_run": REPOSITORY + "/.github/workflows/oracle-pr-tla.yml@" + MAIN_REF,
}
MAX_EVENT_BYTES = 2 * 1024 * 1024
# GitHub reruns may execute this historical definition even after main advances.
# Its dispatcher predates the attempt/fork fixes; retire only that known epoch.
RETIRED_WORKFLOW_SHAS = frozenset({"a1c4e8f09bebcce22a97bc4e69d87a1c40b6e404"})


def commit_sha(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None and value != "0" * 40


def refusal(env, event):
    """Trust runner GitHub context, never a claimed workflow/ref inside subject data."""
    if env.get("GITHUB_SERVER_URL") != "https://github.com":
        return "server"
    if env.get("GITHUB_REPOSITORY") != REPOSITORY:
        return "repository"
    if env.get("GITHUB_REF") != MAIN_REF:
        return "ref"
    kind = env.get("GITHUB_EVENT_NAME")
    if kind not in WORKFLOWS:
        return "event-name"
    if env.get("GITHUB_WORKFLOW_REF") != WORKFLOWS[kind]:
        return "workflow-ref"
    if not commit_sha(env.get("GITHUB_WORKFLOW_SHA")):
        return "workflow-sha"
    if env["GITHUB_WORKFLOW_SHA"] in RETIRED_WORKFLOW_SHAS:
        return "retired-workflow-sha"
    if not isinstance(event, dict) or "pull_request" in event:
        return "event-shape"
    repo = event.get("repository")
    if not isinstance(repo, dict) or type(repo.get("id")) is not int or repo["id"] != REPOSITORY_ID:
        return "repository-id"
    if repo.get("full_name") != REPOSITORY or repo.get("fork") is not False:
        return "repository-payload"
    if event.get("deleted", False) is not False:
        return "deleted"
    if kind == "workflow_dispatch":
        return None if event.get("ref") in ("main", MAIN_REF) and "workflow_run" not in event else "dispatch-ref"
    run = event.get("workflow_run")
    if event.get("action") != "completed" or not isinstance(run, dict):
        return "source-envelope"
    if (type(run.get("id")) is not int or run["id"] <= 0
            or run.get("status") != "completed"
            or run.get("name") != "Public research checks"
            or run.get("event") not in ("push", "pull_request")
            or not commit_sha(run.get("head_sha"))):
        return "source-envelope"
    # Deliberately no branch, fork or conclusion success restriction here: these
    # describe the subject, not executable code. The trusted dispatcher checks the
    # authoritative API run/workflow/head and publishes failures without queueing.
    return None


def admit(env, event):
    return refusal(env, event) is None


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate event key")
        result[key] = value
    return result


def main():
    try:
        with Path(os.environ["GITHUB_EVENT_PATH"]).open("rb") as stream:
            raw = stream.read(MAX_EVENT_BYTES + 1)
        if len(raw) > MAX_EVENT_BYTES:
            raise ValueError("event too large")
        event = json.loads(raw, object_pairs_hook=unique_object)
        reason = refusal(os.environ, event)
    except (OSError, KeyError, ValueError, TypeError, AttributeError, RecursionError):
        reason = "malformed-event"
    print("Oracle maintained-main admission: " + ("accepted" if reason is None else "rejected (" + reason + ")"))
    return 0 if reason is None else 1


if __name__ == "__main__":
    raise SystemExit(main())

# Oracle-backed TLA verification

We reuse the existing Oracle ARM64 machine also used for Petcare, with **a separate repository registration, service account and workspace**. GitHub's repository-scoped Petcare registration cannot be reused directly by a repository under a different owner. No new VM or paid compute is provisioned, and Petcare's registration/service is not changed.

## Which jobs run where

[Public research checks](../.github/workflows/checks.yml) runs structural,
navigation and site checks on GitHub-hosted machines for every original push and
pull-request event. Its job is named **Public source checks**, so it cannot give
a premature green result under the former combined `validate` context.

[Oracle source verification](../.github/workflows/oracle-pr-tla.yml) is a trusted
default-main `workflow_run` dispatcher. It verifies the completed source run,
workflow path, repository and exact head through GitHub's API. Failed/cancelled
hosted work produces non-success `validate` without queue submission. Approved
successful PR work and every push head proceed to Oracle; a moved/deleted push
branch does not erase its original exact-commit check. PR heads must remain open
and current before and after execution. Existing external fork approval remains
in force; `pull_request_target` is not used.

The persistent runner checks out only `github.workflow_sha` from the trusted
default-branch workflow. It downloads bounded, hash-verified regular Git blobs as
data, rejects links/submodules/path escapes, and never imports or executes
candidate Python on that runner. The GitHub token is used only by the trusted
control plane for source/API lookup and exact-head check publication; it is not
forwarded to submitted jobs.

Two separate queue jobs preserve authority:

1. **Native authority A:** maintained-main producer/classifier code executes
   against candidate model/configuration/registry data. All four candidate
   producer blobs must match the reviewed maintained baseline; a producer/schema
   change fails explicitly and requires a reviewed baseline update. Candidate
   Python is never the authority for fresh native captures. After A stops, its
   root-owned immutable raw captures are checked by the trusted ordinary verifier
   against candidate inputs, actual tool identity and all twelve required cases.
2. **Candidate tests B:** a trusted `python -I` bootstrap receives the full regular
   candidate snapshot plus A's derived evidence. It creates a safe local Git
   index from the authoritative filename list, without hooks, global/system
   configuration, Git network access or a fabricated commit/HEAD. The original
   complete candidate unit suite, ordinary check, navigation and site checks run
   inside Oracle's isolated sandbox. Tests requiring an actual historical Git
   HEAD fail visibly rather than receiving invented provenance. B's writable
   phase JSON is diagnostic only; the actual trusted driver's exit composes its
   required phases. B can never replace A's native authority or artifacts.

Only upstream structural success, verified immutable A captures, successful B
phases and the exact-head checks together yield `validate: success`. Native exit0,
stdout PASS or a candidate-generated manifest alone is insufficient. Unsupported
future producer/campaign contracts fail visibly; the generic queue and local
adapter still route new TLA+ work to Oracle, but privileged CI authority changes
require review.

[Oracle TLA verification](../.github/workflows/oracle-tla.yml) preserves explicit
manual dispatch of maintained main, with all structural/native/full-test phases
on Oracle and no fabricated upstream success. Its former direct push trigger is
removed because the workflow-run path already verifies main pushes once.

Queue requests and combined-check identities bind the exact source run attempt,
subject commit, and trusted dispatcher run ID/attempt/workflow revision. The
dispatcher reads the source's exact API attempt rather than a moving latest run.
Repeating submission within one attempt is idempotent; rerunning either the
upstream check or the Oracle dispatcher creates new native and test jobs. It cannot
reuse a previous failed job or describe an earlier successful capture as fresh.
Each native job retains an attempt receipt that the host compares before accepting
its captures; candidate-test reports also carry the context for diagnosis and
remain separate from native authority. Missing or mismatched attempts fail visibly.

Fork runs can have empty commit-to-PR associations. In that case the dispatcher
queries open PRs using the authoritative source-run head owner and branch, with
URL-encoded query data. It still requires an exact open PR with matching base
repository, head repository ID/name, branch and SHA. Direct PR reads repeat those
checks before queue submission and after Oracle completion; unverified webhook PR
metadata never selects the target. Missing, ambiguous or truncated results fail
visibly rather than relaxing the identity checks.

Both control-plane workflows have read-only contents/actions permissions and
checks-write only for result publication (PR dispatch also reads PR metadata).
Checkout credentials are not persisted. Payloads have private bounded storage,
loopback-only networking and no repository credentials. The repository runner's
dedicated queue principal is authorized only for `sloik/post-ai-worlds`.

## Baseline updates and first deployment

Before enabling a new dispatcher/admission boundary, retain an independently
reviewed exact-head native A and complete B proof for its initial reviewed
baseline. The first transport PR cannot pretend that a not-yet-installed
workflow has run: record this owner-authorized bootstrap explicitly, then prove
real push/PR/fork-approval/manual routing after integration. A later producer or
schema change follows the same reviewed baseline-update procedure; do not bless
rehash-only receipts or auto-import candidate verifier code into the control
plane. Parent-owned host installation/admission review is required before this
workflow is activated.

## Admission before job steps

The host installs [oracle_job_guard.py](../ci/oracle_job_guard.py) and [its hook](../ci/oracle-job-started.sh) root-owned outside the checkout. The service's `ACTIONS_RUNNER_HOOK_JOB_STARTED` points to that fixed hook. Its reviewed deployment must admit only this repository's name and numeric ID, GitHub.com, maintained-main workflow definitions, the exact approved workflow-run dispatcher/source context or explicit manual-main context. Direct PR/PR-target execution, arbitrary checkout refs, deleted/foreign identities, missing context and malformed or duplicate-key event JSON remain rejected. The old push/manual-only hook cannot activate the new dispatcher unchanged; retain before/after allow/deny evidence for the scoped extension.

This is a gate before step execution. The Actions runner downloads/prepares actions before the hook; it is not a claim that no untrusted metadata is processed. On runner v2.338.2 the hook path comes from the service process and the hook handler receives trusted GitHub context rather than ordinary workflow environment overrides. The local adversarial tests establish the predicate; actual runner execution establishes installation compatibility. Neither proves all future runner versions preserve those implementation details.

## Host installation contract

Use the existing host, create a dedicated non-login account without sudo/Docker groups, and register only this repository. Registration tokens are short-lived; keep them out of Git, logs and command history. The checked runner application is v2.338.2, official Linux ARM64 artifact SHA-256 `670adb2f268fe21dcbb58b3db0e0aa9d5b3bddfe2c651481336e561ff86de945` from [Actions runner releases](https://github.com/actions/runner/releases/tag/v2.338.2).

When using the custom unit, copy the distribution’s `bin/runsvc.sh` into its installation root before starting it. Give the service group read access to `.credentials` and `.credentials_rsaparams` (root-owned, mode 0640), without making the application/configuration writable.

After registration, the application, configuration, hook and unit are root-owned/read-only to the service account. Only its diagnostic directory and dedicated workspace are writable. [The service template](../ci/oracle-runner.service) applies `ProtectHome`, `ProtectSystem`, `PrivateTmp`, `NoNewPrivileges`, an empty capability set and limits of one CPU core and 2 GiB memory. These are scoped to the new service, not changes to the other runner.

GitHub's 30-day update window is kept by the host: runner updates are applied by the host's verified updater (`swift-tla-runner-update.timer`, daily). GitHub's own auto-update stays disabled so the installation stays root-owned. The updater requires the release-notes SHA-256 and the asset digest to agree with the download, refuses a runner that no longer supports `ACTIONS_RUNNER_HOOK_JOB_STARTED`, never interrupts a running job, swaps only the runner code (registration, credentials, `.env`, hook and file modes are untouched), waits for the listener to reconnect, and restores the previous version on failure. After a real version change, run one real job before claiming compatibility. Tested on 2026-11-13 with a forced same-version swap followed by a green manual-dispatch run.

Treat write access to maintained main and runner administration as trusted authority. Do not execute PR code on the persistent runner, allow arbitrary checkout refs, or add privileged PR-target workflows. Candidate code is confined to the shared queue sandbox; source materialization and evidence verification stay in the reviewed control plane. Changes to these boundaries need explicit review. The host registration is independent of whether a scientific hypothesis is true, probable or desirable.

[Formal assurance scope](../formal/README.md) · [Prediction standard](forecasting-guide.md)

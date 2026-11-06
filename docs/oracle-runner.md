# Oracle-backed TLA verification

We reuse the existing Oracle ARM64 machine also used for Petcare, with **a separate repository registration, service account and workspace**. GitHub's repository-scoped Petcare registration cannot be reused directly by a repository under a different owner. No new VM or paid compute is provisioned, and Petcare's registration/service is not changed.

## Which jobs run where

[Public PR checks](../.github/workflows/checks.yml) remain GitHub-hosted. [Oracle TLA verification](../.github/workflows/oracle-tla.yml) runs only on maintained `main` pushes or an authorised manual dispatch of `main`. It validates the retained public inventory/evidence, regression suite, exact pinned TLC JAR and fresh 12-case finite campaign. Missing formal attachments on prediction issues never prevent submission or acceptance; this job verifies the models already in the repository.

Both workflows use read-only contents permissions and disable persisted checkout credentials. The Oracle registration has repository-specific `post-ai-worlds` and `oracle` labels. The host provides Python 3.12, Java 21 and the pinned `/opt/tla/tla2tools-1.7.4.jar`; the normal offline validator still needs none of those private installation paths.

## Admission before job steps

The host installs [oracle_job_guard.py](../ci/oracle_job_guard.py) and [its hook](../ci/oracle-job-started.sh) root-owned outside the checkout. The service's `ACTIONS_RUNNER_HOOK_JOB_STARTED` points to that fixed hook. It accepts only this repository's name and numeric ID, GitHub.com, the exact Oracle workflow at `refs/heads/main`, and push/manual-dispatch events with a matching main ref. Fork, PR payload, deleted push, other workflow/ref and missing context are rejected.

This is a gate before step execution. The Actions runner downloads/prepares actions before the hook; it is not a claim that no untrusted metadata is processed. On runner v2.338.2 the hook path comes from the service process and the hook handler receives trusted GitHub context rather than ordinary workflow environment overrides. The local adversarial tests establish the predicate; actual runner execution establishes installation compatibility. Neither proves all future runner versions preserve those implementation details.

## Host installation contract

Use the existing host, create a dedicated non-login account without sudo/Docker groups, and register only this repository. Registration tokens are short-lived; keep them out of Git, logs and command history. The checked runner application is v2.338.2, official Linux ARM64 artifact SHA-256 `670adb2f268fe21dcbb58b3db0e0aa9d5b3bddfe2c651481336e561ff86de945` from [Actions runner releases](https://github.com/actions/runner/releases/tag/v2.338.2).

After registration, the application, configuration, hook and unit are root-owned/read-only to the service account. Only its diagnostic directory and dedicated workspace are writable. [The service template](../ci/oracle-runner.service) applies `ProtectHome`, `ProtectSystem`, `PrivateTmp`, `NoNewPrivileges`, an empty capability set and limits of one CPU core and 2 GiB memory. These are scoped to the new service, not changes to the other runner.

Automatic application update is disabled to preserve immutable installation ownership. An administrator must verify and install supported runner updates **within GitHub's 30-day update window, or sooner for critical updates**, rechecking hook semantics and admission controls. Update the pin and perform a real job before claiming compatibility with a new version. This document does not install an automatic updater or monitoring service.

Treat write access to maintained main and runner administration as trusted authority. Do not add Oracle PR execution, arbitrary checkout refs or privileged PR-target workflows. Changes to these boundaries need explicit review. The host registration is independent of whether a scientific hypothesis is true, probable or desirable.

[Formal assurance scope](../formal/README.md) · [Prediction standard](forecasting-guide.md)

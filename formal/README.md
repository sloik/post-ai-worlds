# Bounded formal assurance

TLA+ describes selected rules; TLC explores their finite states. This is executable specification and bounded model checking, not an unbounded theorem, proof of the chapters, empirical prediction or evidence that deployed software follows these rules.

The public edition has its own registry binding and fresh native campaign. Historical results from another source snapshot are not imported as public assurance. Every universe remains `unchecked`: model qualification does not certify a world.

## What the models say

`ScenarioContracts` explores **one accepted claim at a time** across the ten declared universes and 24 selected editorial qualifications. A transfer requires the claim's declared prerequisites; a premise-version change clears assurance until refreshed. It also checks each registered bundle against declared conflicts and admission rules. This does not infer whether a premise is true, discover every contradiction in prose, or check arbitrary combinations of admitted claims.

`OperationalGates` composes `ExpansionContract` and `AuthorityContract` using a shared vocabulary. Phase is finite (0/1); four readiness gates are Boolean; capability, export, alternatives, requests and completed exit are bounded flags. Permission and a public mandate have distinct meanings. The model keeps capability from automatically creating a mandate, and requires all readiness gates before expansion. These are proposed contracts, not a mathematical justification of political legitimacy.

Exit completion requires both exported records and an available alternative. The liveness property assumes those prerequisites already exist and weak fairness for completion. A supplier refusing export before it happens can prevent that premise. This is **conditional completion**, not guaranteed portability against any provider.

## Campaign and controls

There are 12 cases: three clean positive checks, five deliberately broken semantic controls, three reachable witnesses, and one lost-witness composition control. Expected named invariant violations use native exit 12. Those are successful experimental controls, not positive invariant proofs.

The compatible composition reaches an authorised phase-1 state with completed exit despite a later supplier refusal. The incompatible composition forbids public-authorised expansion: TLC exits cleanly on the unreachable-witness invariant, while qualification deliberately rejects the requested reachability (exit 1). Individual properties passing would miss this obstruction.

Inspect [campaign.py](../tools/campaign.py), configurations, captured [evidence](evidence/manifest.json), and model source together. Each capture starts with a producer header binding case, model and input hashes, followed by unmodified native stdout and stderr. This rejects accidental cross-case log substitution. Stored hashes and diagnostics support integrity and consistency review; they do not cryptographically attest who ran a process. A contributor changing a model should rerun it, rather than relabel old logs.

## Reproduce

Use Python 3.11+ and Java 11+. Obtain `tla2tools.jar` from the [official v1.7.4 release](https://github.com/tlaplus/tlaplus/releases/tag/v1.7.4). The exact artifact SHA-256 is `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`; a filename or release tag alone is insufficient.

```sh
python3 tools/run_models.py --jar /path/to/tla2tools.jar
python3 tools/check.py
python3 -m unittest discover -s tests -v
```

Run in a workspace whose native output contains no personal filesystem identities. The runner stores fresh output captures and refuses personal home paths; it does not redact logs and retain old hashes. The offline check needs only the repository, not Java, network access, the producer's installation path, private Git objects or credentials. CI executes the native campaign afresh.

[Shared worlds](../worlds/README.md) · [Contribution guidance](../CONTRIBUTING.md)

## Oracle execution

Maintained-main checks also run on the existing shared Oracle host through a separate repository registration and isolated service account. Public PR checks stay GitHub-hosted. See [runner operation and admission boundary](../docs/oracle-runner.md). Prediction proposals may include formal work, but its absence is nonblocking; the [forecasting standard](../docs/forecasting-guide.md) governs their empirical reasoning.

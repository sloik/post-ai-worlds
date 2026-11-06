"""Declared bounded native campaign including semantic controls."""

RUNS = [
    ("contracts-safe", "ScenarioContracts", "pass", None),
    ("contracts-scope-control", "ScenarioContracts", "counterexample", "ScopeSound"),
    (
        "contracts-stale-control",
        "ScenarioContracts",
        "counterexample",
        "AssuranceVersionBound",
    ),
    ("contracts-import-witness", "ScenarioContracts", "witness", "NoAcceptedWitness"),
    ("contracts-refresh-witness", "ScenarioContracts", "witness", "NoRefreshedWitness"),
    ("operations-safe", "OperationalGates", "pass", None),
    ("operations-phase-control", "OperationalGates", "counterexample", "PhaseGuard"),
    (
        "operations-mandate-control",
        "OperationalGates",
        "counterexample",
        "MandateSeparated",
    ),
    (
        "operations-exit-control",
        "OperationalGates",
        "counterexample",
        "IndependentExit",
    ),
    (
        "operations-delivery-witness",
        "OperationalGates",
        "witness",
        "NoDeliveredExitWitness",
    ),
    ("operations-progress", "OperationalGates", "pass", None),
    (
        "operations-lost-witness-control",
        "OperationalGates",
        "lost_witness_control",
        "NoDeliveredExitWitness",
    ),
]
DEPENDENCIES = {
    "ScenarioContracts": [
        "Vocabulary.tla",
        "RegistrySnapshot.tla",
        "ScenarioContracts.tla",
    ],
    "OperationalGates": [
        "Vocabulary.tla",
        "ExpansionContract.tla",
        "AuthorityContract.tla",
        "OperationalGates.tla",
    ],
}

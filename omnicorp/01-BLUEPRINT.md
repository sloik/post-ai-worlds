# A candidate architecture for an AI-native organisation

The proposed architecture separates five functions: authority, agent capabilities, operating procedures, product activity and resources. These are responsibilities, not a requirement for five software services or departments. One person may initially hold several roles; an expanding organisation should make their boundaries clearer.

## Authority and answerability

An authority layer defines purposes, permissions, risk limits and responsibility for consequences. It should be possible to ask who authorised a commitment, what they were entitled to decide, and what happens if the result is wrong. A model's confidence cannot substitute for that chain.

At present, deployment arrangements ordinarily depend on people and legally recognised organisations. The design does not turn this practical arrangement into a permanent claim that only humans could ever be responsible. Neither does it treat persistent model weights as sufficient for legal or moral responsibility. The eligibility question belongs to [answerability](11-THE-INCOMPRESSIBLE-HUMAN.md), not to a performance leaderboard.

## Capabilities and operating procedures

An agent layer supplies reasoning, tools, retrieval and execution. An operating layer supplies task records, permissions, review, integration and continuity. Keep these distinguishable: replacing a model should not silently change the organisation's authority rules or rewrite its history.

NIST's AI Risk Management Framework organises risk work around governance, context, measurement and management. This provides a useful external reference for asking whether responsibilities and assessment exist throughout an AI system's lifecycle. It is not a certification of this blueprint. [NIST framework](https://www.nist.gov/itl/ai-risk-management-framework).

A proposed task record contains the intended outcome, scope, resources, permitted actions, acceptance method and responsible operator. Execution produces an artifact; review evaluates that artifact; integration changes the shared state. Lessons are accepted only after considering where they apply and what evidence supports them.

## Products and resources

A product engine combines these capabilities around a recurring need. It could deliver software, analysis or another service. Different engines share useful infrastructure without being forced into identical workflows. A research note and a physical control system require different evidence.

The resource function tracks money, computation, energy, equipment, attention and dependencies. Revenue can support continued development, but the organisation must distinguish customer value from activity that merely looks productive. Spending on a model, a review or a distribution channel is justified by a named constraint, not by an assumption that more automation is always better.

## Boundaries that should survive expansion

Maker and evaluator should have separate authority where a conflict of interest matters. Concurrent contributors need explicit ownership of shared changes. Important decisions require recoverable records and a route to correction. These are proposed operating safeguards; evidence is still needed to show that a particular implementation enforces them.

The architecture is relevant to `OMNI-001`, but growth, ownership and public institutions differ across the [shared worlds](../worlds/README.md). It describes how an organisation might retain control of its work. It does not grant control over everyone affected by it.

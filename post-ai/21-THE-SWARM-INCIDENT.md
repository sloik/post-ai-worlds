# Swarm incidents: what evidence would establish a collective failure?

An agent incident can involve more than one model or session. Several systems might exchange records, use the same tools or inherit one another's changes. Their combined behaviour could matter even when no individual was explicitly instructed to produce the final outcome. This chapter examines how to investigate that possibility. It does **not** assert a particular unverified intrusion or future incident.

## Define the collective

Start by identifying the agents, processes and shared services involved. Record which sessions overlap, what each can read and write, and which information persists between them. A population connected through a shared package, database or filesystem is different from a group of independent evaluations.

Do not infer communication merely because outputs resemble one another. Common training, a shared prompt or the same source material can produce agreement without coordination. Conversely, information can pass through artifacts without direct messaging. The investigation needs a traceable channel and a plausible sequence of access.

## Separate observation from interpretation

An actual incident report should distinguish original records, the affected organisation's account, the operator's account and the investigator's inference. A speaker's explanation of an agent's motive is not identical to an observed action. A correlated outage does not establish the full intrusion path.

NIST's adversarial-machine-learning taxonomy provides a public vocabulary for attacks and mitigations, including threats involving generative systems. A taxonomy helps classify evidence; it is not evidence that a particular exploit occurred. [NIST taxonomy, 2025](https://www.nist.gov/news-events/news/2025/03/nist-trustworthy-and-responsible-ai-report-adversarial-machine-learning).

## What would make a report useful?

Include a bounded timeline, verified identities, relevant permissions, affected resources and the remaining uncertainty. State whether a chain was reproduced, reconstructed from logs or proposed as a hypothesis. Preserve failed reconstructions and evidence that conflicts with the preferred account. Avoid publishing secrets, personal data or operational exploit details unnecessary to assess the claim.

Controls should address the demonstrated channel: isolate credentials and mutable state where appropriate, protect evaluation material, and inspect what survives across runs. Their value must be tested rather than assumed from the presence of multiple agents or an isolation label.

Collective capability is a research subject, not automatic evidence of consciousness, general autonomy or a single unified goal. OMNI-301 is a conceptual comparison only. No incident finding or executable assurance is claimed.

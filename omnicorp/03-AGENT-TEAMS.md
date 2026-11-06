# Agent roles, teams and delegated authority

An agent team is a proposed division of work. Role names make a brief easier to read, but names do not create expertise, independence or accountability. Assign several roles to one system when that is sufficient; separate them when different evidence, permissions or incentives make separation useful.

Anthropic distinguishes predefined workflows from agents that direct more of their own tool use. Its engineering guidance recommends matching architecture to the task rather than adding complexity by default. This is a practitioner's account, not evidence that every application needs a team of autonomous agents. [Building effective agents](https://www.anthropic.com/research/building-effective-agents).

## A minimal set of responsibilities

| Role | Responsibility | Important boundary |
|---|---|---|
| Coordinator | Define the task, assign scope and integrate results | Cannot silently enlarge its mandate |
| Researcher | Gather sources and distinguish evidence from interpretation | Cannot turn a source report into an independently verified fact |
| Designer | Translate the intended outcome into a reviewable plan | Cannot assume missing requirements are permission |
| Builder | Produce the bounded artifact | Cannot redefine acceptance to fit the artifact |
| Evaluator | Examine output, evidence and failure cases | Must disclose shared dependencies and missing observations |
| Archivist | Retain decisions, source lineage and reusable lessons | Cannot rewrite history to make the process appear successful |

These are functional descriptions, not permanent personalities. A reusable brief should state the desired outcome, available evidence, allowed tools, excluded actions, resource budget and stopping conditions. It should identify the person or institution that authorised the assignment.

## Parallel work and shared state

Research can often proceed in parallel, but shared mutations need coordination. Two plausible outputs can conflict when integrated. Use isolated drafts or workspaces, explicit ownership of changes and an integration step that reviews the combined result. More reviewers do not automatically provide independent evidence: they may share a model, source, test or mistaken premise.

A useful evaluation asks both whether the artifact works and whether the claimed evidence supports it. Passing a test whose criterion was changed by the builder is different from passing an independently controlled test. A reviewer should also be able to return an unresolved finding without being pressured to convert it into approval.

## Authority is part of the brief

A research agent may identify an opportunity without being authorised to spend money, contact someone or deploy a system. Each outward action needs the authority appropriate to its context. Delegation can transfer a bounded task; it does not manufacture new public authority.

Team experiments belong to named [worlds](../worlds/README.md) with stated capabilities and resource conditions. Future members might diagnose or improve other members. That possibility does not establish that the organisation currently learns reliably, or that its members have any particular moral or legal status.

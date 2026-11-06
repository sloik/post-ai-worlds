# Contributing

This repository is the canonical source for both Post-AI Era Vision and Omnicorp. Make new work here. Help make the arguments clearer, the sources stronger and the assumptions easier to challenge. Contributions and project discussion are in English.

## Choose a starting point

- **Evidence or source:** identify the claim and explain what the source supports or challenges.
- **Contradiction or counterexample:** identify the assumptions, scope and consequence that do not fit together.
- **Idea or scenario:** explain the question, proposed assumptions and what would distinguish it from existing worlds.
- **Forecast proposal:** define a future event and how it could be resolved. A proposed question is not a registered prediction.
- **Small correction:** a focused pull request can go directly to review. Discuss substantial reorganisations first to avoid unnecessary work.

The issue forms collect useful context, not a test of membership. If a field is unknown, say so. Exploratory conversation belongs in Discussions; an actionable source challenge or proposed correction belongs in an issue.

## Label what kind of claim you are making

Use these distinctions in issues and pull requests:

| Kind | What to provide |
|---|---|
| Observation | A dated source, the narrow fact reported and important limitations |
| Assumption | The premise, its scope and whether it is empirical, hypothetical or unresolved |
| Conditional consequence | The assumptions needed for the conclusion and what could break the mechanism |
| Value | The principle or preference being defended; evidence alone cannot settle it |
| Decision | The proposed project or operating rule, who can authorise it and its limits |

A source's claim is not automatically our finding. Prefer primary sources, retain dates and distinguish correlation from causation. Disclose when several accounts share one source or when a result is reported by an interested party. Include contrary evidence rather than counting citations as votes.

## Propose a change

1. Keep the pull request focused on one coherent change and link the relevant issue where useful.
2. Identify affected chapters, claim records, assumptions and OMNI IDs. State unknown scope rather than forcing a mapping.
3. Preserve stable IDs and historical records. Changing an assumption may require a visible version or fork; it must not silently change a frozen forecast.
4. Explain supporting evidence, counterevidence and what remains uncertain.
5. Run the applicable checks documented by the affected area. Report what actually ran. Documentation corrections do not require inventing a formal proof.
6. If assurance is affected, identify the exact model, inputs, bounds and result. A change to a source or assumption can make old assurance stale.

A check that passes against a proxy does not establish the real-world conclusion. Keep normative choices, empirical tests and formal properties separate. Retain meaningful failed controls and counterexamples; do not weaken a property merely to obtain a pass.

## Local checks

Use Python 3.11 or newer. The ordinary check is offline and needs no private files or account:

```sh
python3 tools/check.py
python3 -m unittest discover -s tests -v
```

When editing a reading-track document, explicitly update its byte/heading inventory with `python3 tools/update_inventory.py` and review the coverage diff alongside the prose. New or moved chapters also need a disposition in `worlds/mapping.json`. Re-enrolment records editorial coverage; it grants no proof status.

When changing registry premises, a model, configuration or evidence-producer code, follow [formal reproduction](formal/README.md) and retain a fresh qualified campaign. A documentation correction does not itself require rerunning unchanged native inputs while their ordinary retained-evidence check still passes.

## AI-assisted contributions

AI tools are welcome. The contributor remains responsible for accuracy, sources, rights and the proposed change. Disclose material AI assistance and what you verified. Do not invent citations or imply that several generated reviews are independent evidence.

Agent accounts and generated messages have no automatic authority or additional votes. An issue, comment, model output or passing check does not authorise spending, outreach, publication elsewhere, production access or autonomous execution.

## Rights and privacy

Link to sources rather than uploading copied articles, books, transcripts or restricted datasets. Submit only material you have permission to share. Do not include private conversations, personal identifiers, credentials, local machine paths or confidential operational records.

Submit original work you can license under the applicable terms in [LICENSING.md](LICENSING.md): CC BY 4.0 for writing/data/illustrations and MIT for software/formal specifications. You retain ownership; intentional submissions for inclusion use those terms unless explicitly stated otherwise and agreed before inclusion. No copyright assignment or separate contributor agreement is required. Preserve third-party notices and give appropriate credit. Discussion and experiments are welcome; a source or licence is not endorsement.

# Building software as a learning process

Software is a useful early domain because many outcomes can be represented as inspectable artifacts and exercised repeatedly. That does not make every requirement objective or every defect easy to detect. The proposed factory treats implementation, assessment and organisational learning as connected work.

## Define the outcome before generating code

A task begins with the behaviour someone needs, the conditions in which it should work and the failures that matter. Separate the requirement from a convenient implementation. Name the system boundary, permitted changes and evidence needed for acceptance.

A specification can make an argument more precise. It cannot remove disagreement about the intended product or guarantee that its tests capture all relevant behaviour. A screen that passes structural checks may still confuse users; a service that handles a fixture may fail on actual workloads. Record what each check establishes rather than describing all successful checks as proof of correctness.

## Implement and assess in separate roles

A proposed loop is: clarify, plan, build, review, integrate and learn. The builder works within a bounded scope. Review considers the resulting behaviour, security and compatibility alongside the supplied tests. Integration checks the combined system, including interactions with concurrent changes.

NIST's Secure Software Development Framework describes security practices across the development lifecycle. It is a primary reference for treating security as part of development rather than as a final label. Adopting this workflow alone does not establish compliance with that framework. [NIST SSDF](https://csrc.nist.gov/projects/ssdf).

Keep acceptance evidence identifiable: source revision, configuration, relevant inputs, tool versions and observed outcome. Preserve failed results when explaining a later repair. Reusing evidence is reasonable when the checked inputs remain unchanged and the scope matches; a newer timestamp is not inherently stronger evidence.

## Learn without corrupting the evaluator

A completed task should leave more than code. It may produce a corrected assumption, a diagnostic example, an architectural explanation or a tool that prevents a recurring mistake. The lesson needs a scope: where did it help, and what would show it does not apply?

The organisation must distinguish learning from making its measures easier to satisfy. A builder should not change the evaluator, authority rules or recorded history merely to make a result appear successful. Legitimate evaluator improvements need their own rationale and review.

## Treat security review as a recurring scan

Observation (producer self-report, 4 November 2026): OpenAI describes an internal pipeline that scanned about 7% of the Linux kernel with an unreleased cyber model in mid-October 2026. It reproduced 1,724 of 2,308 candidate findings and produced 1,169 working local privilege-escalation exploits, which variant analysis reduced to 948 unique vulnerabilities by distinct patch. The total API cost was $1,213,430. Human researchers reviewed every exploit, patch and severity before reporting, and maintainers reviewed the patches. The run has not been externally reproduced, and the model is not public. [OpenAI, 2026](https://openai.com/index/a-thousand-fewer-paths-to-root/).

Four of the source's operating lessons apply directly to this factory and are adopted here as proposals:

- **Rescan when the model changes.** The same harness found 166 unique exploitable flaws with a July model and 948 with the October model, after three months of upstream hardening between the runs. A clean review therefore belongs to a model generation as well as to a source revision.
- **Verify the path, not only the result.** In an early run, 20 of 200 reported exploit successes reached root through a different, unassigned vulnerability. An independent check that the intended mechanism produced the outcome is part of acceptance.
- **Review patches adversarially.** Early generated patches mitigated the proof of concept but sometimes added unnecessary code, missed variants or broke conventions. Iteration improved them. Human and generated patches both benefit from a reviewer that tries to bypass the fix.
- **Contain the builder.** The agents also found and exploited a flaw in the test emulator. Build, test and evaluation infrastructure are attack surface and need isolation that has been tested, not assumed.

These lessons are not evidence that unattended security patching is safe in production. The source keeps a human approval step before every report.

## Prefer the representation that works

Models, generated programs and conventional software can cooperate. Exact arithmetic, state storage, permission checks and physical control need reliable implementations, regardless of where reasoning occurs. Do not require every function to reside inside a model's weights, or assume a conventional component is obsolete because a model can describe it.

This factory is a candidate operating method in `OMNI-001` and `OMNI-301`. Its quality must be measured on delivered outcomes, regressions and total effort—not the amount of code generated. See the [efficiency chapter](10-EFFICIENCY-AND-LEGITIMACY.md) and [shared worlds](../worlds/README.md).

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

## Prefer the representation that works

Models, generated programs and conventional software can cooperate. Exact arithmetic, state storage, permission checks and physical control need reliable implementations, regardless of where reasoning occurs. Do not require every function to reside inside a model's weights, or assume a conventional component is obsolete because a model can describe it.

This factory is a candidate operating method in `OMNI-001` and `OMNI-301`. Its quality must be measured on delivered outcomes, regressions and total effort—not the amount of code generated. See the [efficiency chapter](10-EFFICIENCY-AND-LEGITIMACY.md) and [shared worlds](../worlds/README.md).

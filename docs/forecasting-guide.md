# Making a forecast others can inspect

A useful prediction connects a numerical belief to a question that can later be resolved. It also exposes why the belief might change. We prefer the [public Superforecasting playbook](https://github.com/sloik/superforecasting), while accepting an equivalent manual analysis. This guide defines the contribution standard; using a particular tool does not establish forecasting skill.

If you are still designing a question or exploring a scenario without odds, use an Idea issue. A scenario's OMNI identifier supplies assumptions, not its likelihood. A value judgment about a desirable world is likewise different from a prediction.

## Define the future event

Fix the observable outcome, scope, cutoff and resolution source before committing a probability. Establish the current baseline so an already realised event cannot become a retrospective forecast. Explain partial fulfilment, changed definitions, unavailable evidence and conditional antecedents that never occur. Distinguish the event deadline from the later date when authoritative evidence may arrive. Narrow a question when ambiguity makes it impossible to resolve fairly. [Question design reference](https://github.com/sloik/superforecasting/blob/main/references/question-typing.md).

## Build and challenge the estimate

Begin with comparable cases rather than only the vivid story of this case. Explain the reference class, sources, numerator/denominator and relevant differences. Seek independent corroboration where available; several articles repeating one source are not independent evidence. When reliable counts or comparisons are unavailable, say what you searched and why the analogues fail. A subjective anchor is permissible when labelled and reasoned; fabricated precision is not.

Separate drivers you can estimate from conjectures. Explain opposing mechanisms and the observation that would reverse your conclusion. A decomposition helps only when its parts and dependencies make sense. Do not multiply marginal subevent probabilities as if they were independent. Conditional chains must use conditional probabilities. If using Bayesian adjustments, explain the prior, evidence likelihoods and dependence; unexplained likelihood ratios are judgments disguised as measurements. Manual arithmetic or a spreadsheet is sufficient. [Workflow reference](https://github.com/sloik/superforecasting/blob/main/references/workflow.md).

Provide the strongest supporting and opposing cases with primary sources where possible. Explain why the chosen number fits the balance, where uncertainty lies and what could make your reasoning fail. Precision should reflect evidence, not the number of digits a tool prints. A source's reputation or a polished explanation does not replace the inference. [Rationale checklist](https://github.com/sloik/superforecasting/blob/main/references/rationale-quality.md).

## Commit a coherent numerical belief

For a binary event, state its probability explicitly. For outcome distributions, fix mutually exclusive, exhaustive outcomes and ensure probabilities sum to one. Numeric bins need ordered boundaries and tails; a percentile range alone is not a scored bin distribution. Avoid certainty without an adequate logical or evidential basis. Record who authored the estimate and the information cutoff. Other people can disagree without being averaged into a single project view. [Forecast record reference](https://github.com/sloik/superforecasting/blob/main/templates/forecast-record.md).

Invite another perspective without manufacturing independence. Several agents can share training, sources and assumptions; repeated prompts can echo the same error. Pooling is optional. If used, disclose component forecasts, weights, method and differences before relying on the aggregate. Do not automatically extremize an all-AI panel or claim consensus supplies new evidence.

## Preserve, update and learn

An editable issue alone is not an immutable registration. For an accepted forecast, preserve an identifiable initial record and append dated updates with old/new beliefs, new evidence and reasoning. Specify review dates and signals for movement in both directions. Correct defective questions visibly; supersede rather than silently rewrite them after observing outcomes.

Agree on scoring before resolution. Binary Brier is `(p − outcome)^2` with outcome 0 or 1; lower is better. Ordered distributions may use Ranked Probability Score with its precise normalization stated. Keep differently scaled scores separate. Declare whether scoring uses initial beliefs, a fixed cutoff, latest pre-outcome beliefs or a time-weighted trajectory; preserve all versions and avoid after-the-fact selection. Report missing/withdrawn cases transparently rather than silently dropping poor results. Compare baselines on the same questions and information timing. One favourable result does not demonstrate calibration. [Aggregation and scoring reference](https://github.com/sloik/superforecasting/blob/main/references/aggregation-and-scoring.md).

At resolution, retain the decisive evidence, outcome and one lesson about the process. TLA+, proofs and simulations may clarify a particular mechanism; they cannot supply empirical odds or turn assumptions into observations. They remain optional. Installing the skill, running its tools or publishing a forecast is a separate action, not something this guide performs automatically.


## Acceptance and optional formal work

Maintainers review this substantive structure before treating a Prediction as ready for project registration. Required issue fields collect evidence; they cannot establish the quality or truth of that evidence. A blank/API-created issue that bypasses the form still needs the same content. Incomplete submissions remain question-design ideas until completed, rather than being treated as accepted forecasts.

TLA+ verification is encouraged when a forecast depends on formalizable mechanisms, but **absence of a model or proof is never a blocker** for submitting or accepting a prediction. If attached, identify source, assumptions, properties, finite bounds, tool version and positive/negative controls. Distinguish a proposed unrun model from executed evidence. Checking logical consistency does not establish empirical probability. Changing an existing checked model still requires its normal integrity and regression checks.

[Contribution guidance](../CONTRIBUTING.md) · [Formal assurance boundaries](../formal/README.md)

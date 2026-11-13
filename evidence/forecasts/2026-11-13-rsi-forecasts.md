# Forecasts issued 13 November 2026: research-automation claims

These four forecasts were issued at the maintainer's request after a review of Dwarkesh Patel's essay and video *Recursive self-improvement has started* (13 November 2026). They are separate from the four Observatory questions. The [frozen export](2026-11-05-records.json) is unchanged, and no registered probability moved.

Forecaster: Argo, operator mode, using the [Superforecasting playbook](https://github.com/sloik/superforecasting). Information cutoff: 13 November 2026. Scoring: binary Brier on the latest probability before resolution, with the initial values below preserved. Updates are appended with a date and never overwrite an earlier value.

## Why these questions

The essay's own forecasts cannot be resolved as stated. "As good as the best human AI researchers" and "at least as good as the best human experts in every field" have no public resolver. The questions below take the nearest public records that would look different if the essay is right than if it is wrong. Three of them score a publication or a company statement, which is easier to observe than the capability itself and is not the same thing.

## The forecasts

| ID | Question | Deadline | Probability | Three views |
|---|---|---|---|---|
| F1 | METR, or another evaluator unaffiliated with the developer, publishes an assessment whose central estimate is that a named frontier developer is improving model capabilities at four times or more its historical rate before the acceleration. Producer self-reports do not count. | 2027-12-31 | 11% | 15 / 14 / 7 |
| F2 | Anthropic publishes an update to its R&D Automation Index, or a successor it states is comparable, reporting that AI "leads" (level AL4) or higher on 50% or more of its AI R&D work. | 2027-12-31 | 39% | 50 / 40 / 27 |
| F3 | OpenAI officially declares its "true automated AI researcher" goal achieved; or OpenAI, Anthropic, Google DeepMind, Meta or xAI officially states that its AI can fully substitute for its top human AI researchers, or that its AI research is fully automated; or Anthropic reports a model scoring 85% or more on CoBench. Official company publications only. | 2028-12-31 | 38% | 42 / 42 / 30 |
| F4 | OpenAI's Navier–Stokes proof, or a corrected version, is accepted for publication by a refereed mathematics journal; or the Clay Mathematics Institute publicly states that it accepts the solution as correct. | 2027-12-31 | 10% | 19 / 6 / 9 |

For every question, the absence of a qualifying public record by the deadline resolves NO. A methodology change that the publisher does not describe as comparable resolves F2 as NO. The baseline for each event was checked on 13 November 2026 and none had occurred.

## Method and dependence

Each probability pools three views by geometric mean of odds, with no extremizing: Argo's own estimate, and two separately elicited views that were each assigned a named outside position (short timelines; "AI as normal technology"). All three ran on one model family and received one fact sheet, so they are correlated. The spread between them is disagreement, not a confidence interval. No calibration is claimed.

There is no matched reference class for F1 to F3. Their anchors are labelled subjective priors. F4 uses a small class of famous claimed solutions (about two of seven accepted within sixteen months), recalled from general knowledge and not re-verified.

## Reasoning

**F1 (11%).** The only series is METR's single pilot: about 2x, with 1.3x to 3x unsurprising to METR and a benchmark-index estimate of 1.9x (95% interval 1.5 to 2.8). [METR, 2026](https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/).
- For: a smooth-acceleration reading implies another doubling within about six months, and METR found no clear bottleneck for the next twelve months. [Cotra, 2026](https://www.planned-obsolescence.org/p/ai-is-dramatically-accelerating-ai).
- Against: the developer redacted most of the evidence and narrowed the scope midway, so repeat access is uncertain. Evaluators hedge, and a central estimate of 4x lies above the top of every published interval.
- Could be wrong if: the feedback loop compounds as the naive model says (higher), or no second assessment is published at all (lower).

**F2 (39%).** The baseline is 26% as of August 2026, up from under 1% in February 2026, with over 90% of work already at "AI collaborates" or above. [Anthropic, 2026](https://www.anthropic.com/institute/measuring-pace-of-ai-development).
- For: the trend is steep, the task basket is frozen at July 2026, and the judge is one of the producer's own models, which can drift upward on borderline cases.
- Against: the index is a prototype that may be dropped or re-based, and early adoption curves flatten on the hard tail.
- Most of the spread between the views is the chance that no comparable update is published.

**F3 (38%).** This scores a claim. OpenAI set the goals in October 2025 and declared the first one, an "automated research intern", met on schedule in September 2026 by its own measurements. That is one case and no base rate.
- For: the March 2028 target falls inside the window, there are several routes to YES, and labs have an incentive to announce milestones.
- Against: "fully substitute" is a costly statement to make, the goal's author said "we may totally fail", and Anthropic's August 2026 risk report says its strongest models still fall short of the CoBench level it would expect from a full substitute.
- A YES here would not show that the capability exists. It would show that a developer was willing to say so.

**F4 (10%).** Clay has not certified the result, and its rules require refereed publication followed by a waiting period. Independent review was still under way in mid-November 2026. A preprint argues that the accompanying Lean statement does not match the written proof. [arXiv:2610.08144](https://arxiv.org/abs/2610.08144).
- Argo's first estimate was 39%, from a chain of likelihood ratios. One of the other views came back at 6%. A decomposition then gave 19%: correct and accepted by the field (0.6), submitted to a journal (0.7), accepted within about fourteen months (0.4), plus a small Clay route. The first chain had counted the Lean proof as strong support although its fidelity is the disputed point. This revision was made after seeing another view, so anchoring is possible.
- Could be wrong if: a leading analyst endorses the proof and a journal fast-tracks it (higher), or a gap is found in a core lemma (lower).

## Two judgments that are not scored

These have no resolver and are recorded only to show where this review stands against the essay.

| Claim in the essay | Essay | This review (three views) |
|---|---|---|
| AI at least as good as the best human AI researchers by the end of 2028 | about 50% (median 2028) | 25% (20 / 42 / 17) |
| AI at least as good as the best human experts in every field by the end of 2030 | expected | 13% (8 / 35 / 6) |

## Update triggers

- F1 up: a second unaffiliated assessment with a central estimate of 3x or more. Down: restricted access, or a repeat at 2x or below.
- F2 up: a second index release at 40% or more. Down: a methodology change, or a plateau.
- F3 up: a published CoBench score of 70% or more. Down: OpenAI revises or drops its March 2028 target.
- F4 up: a journal announces refereeing with a timetable, or a leading analyst endorses the proof. Down: a credible gap in a core lemma.

Review these with the registered questions on 5 February 2027.

[Forecast review queue](../FORECAST-REVIEWS.md) · [Forecasting guide](../../docs/forecasting-guide.md)

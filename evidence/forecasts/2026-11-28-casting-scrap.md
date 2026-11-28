# Sustained AI-driven casting scrap reduction

**Issued 28 November 2026.** The evidence cutoff is the issue date. The maintainer asked for the draft of 27 November to be registered. The observation window opens on 29 November 2026 at 00:00 UTC, one day later than the draft proposed.

| Record | Observable milestone | Deadline, 23:59 UTC | Initial probability |
|---|---|---|---:|
| Q13 | Two foundry operators under different control publicly document a sustained 20% scrap reduction after adopting a machine-learning recommendation in regular production. | 2029-12-31 | **14%** |

## Resolution rule

From 29 November 2026 through 31 December 2029 (UTC), at least two metals foundry operators under different ultimate control publicly document at least a **20% relative reduction in casting scrap sustained over 90 consecutive calendar days**. Each case concerns a named production line and an identified casting pattern or part family, and follows a machine-learning recommendation adopted in regular production.

Both cases need their post-change measurement windows and first public results inside the forecast window. Each must name the operator, site and line (a stable plant-specific label suffices) and specify the AI-influenced process change. It must give dates plus counts of scrapped and produced units for the 90-day post-change window and the immediately preceding 90-day baseline. The part scope and scrap definition must be the same, the baseline rate nonzero, and material changes in mix, inspection and concurrent interventions disclosed. A suitable matched comparison may account for a concurrent change. An operator’s detailed report or an unaffiliated published audit may qualify. A vendor claim alone, a pilot outside regular production, a simulation, inspection-only automation or unreported denominators cannot. Human approval of a recommended change is allowed. Each operator counts once.

Review public records through 28 February 2030 for results first published by 31 December 2029. Resolve YES for two qualifying operators and NO for fewer, including missing or confidential results. Record source URLs and calculations.

## Estimate

The [27 November review](../2026-11-27-prometheus-physical-ai.md#proposed-forecast-on-sustained-casting-scrap-reduction) gives the outside view, opposing cases and Argo’s 40% judgment as lead forecaster. A specialist then received the criteria and evidence summary without that number. It put the chance that any one operator publishes a fully compliant case at about 11%, and a second unrelated operator following given the first at about 35%, giving 4%. It argued that scrap counts are treated as confidential and that marketing cases report percentages without denominators.

| Lead estimate | Separately elicited estimate | Pooled |
|---:|---:|---:|
| 40% | 4% | 14.29% |

The `aggregate.py` script pools the two with equal weights in odds space and no extremizing. The lead puts more weight on demand, instrumentation and the existing supplier market. The specialist puts more weight on the disclosure bar, which every case must clear. Both used the same model family and overlapping sources. The 36-point spread is disagreement, not a confidence interval. [Superforecasting playbook](https://github.com/sloik/superforecasting)

## Update signals and scoring

Raise the estimate on the first qualifying case, or when a funded multi-operator programme publishes its measurement plan (suggested 2.0×). Lower it if case studies published through 2027 still omit unit counts, or if controlled comparisons show early gains fading (0.6×). Review on **5 February 2027** and annually thereafter. Keep the initial odds and dated updates append-only. Score with binary Brier loss, `(p − outcome)²`, using the latest public estimate strictly before outcome evidence became public, and report the initial-estimate score for comparison. Record one lesson at resolution.

[Forecast review queue](../FORECAST-REVIEWS.md) · [Omnicorp Observatory](https://stocki-apps.pages.dev/omnicorp/observatory/#foundry-scrap-reduction)

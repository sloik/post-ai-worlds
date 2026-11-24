# OpenAI pretraining loss and the prospect of AI accelerating AI

**Assessed 24 November 2026.** Jakub Pachocki published OpenAI’s fixed-snapshot internal code evaluation on 22 November. Lower log-perplexity, or cross-entropy loss, means better next-token prediction on that dataset. This is a base-model measure. Reasoning at inference time and other post-training improvements can change downstream performance without improving this number. [OpenAI, Perplexity and Intelligence](https://openai.com/index/perplexity-and-intelligence/)

## Where the graph changes

The plot starts with GPT-3.5. GPT-2 and GPT-3 appear in the article as historical examples outside the plotted series. The first large drop is GPT-3.5 to GPT-4. The drop resumes in a sustained sequence in late 2025 and steepens in 2026, starting visibly with GPT-5.3-Codex / 5.4 and GPT-5.5. The 2025 reversal from GPT-4.5 to GPT-4.1 / o3 is part of the published series. The dates below are the chart’s coordinates and can differ from product launch dates.

| Chart month | Model as plotted | Log-perplexity |
|---|---|---:|
| 2022-03 | GPT-3.5 | 0.986 |
| 2023-03 | GPT-4 | 0.913 |
| 2023-11 | GPT-4 Turbo | 0.909 |
| 2024-05 | GPT-4o / o1 | 0.904 |
| 2025-02 | GPT-4.5 | 0.876 |
| 2025-04 | GPT-4.1 / o3 | 0.902 |
| 2025-08 | GPT-5 / 5.1 | 0.893 |
| 2025-12 | GPT-5.2 | 0.888 |
| 2026-02 | GPT-5.3-Codex / 5.4 | 0.871 |
| 2026-04 | GPT-5.5 | 0.848 |
| 2026-07 | GPT-5.6 Sol | 0.828 |
| 2026-09 | GPT-6 Astra | 0.783 |
| 2026-11 | GPT-6.2 Astra | 0.761 |
| 2026-11 | Internal model (unreleased) | 0.732 |

The released-model comparison from GPT-5.2 through GPT-6.2 Astra is a 0.127 drop in log-perplexity across 11 chart months. Including the unreleased point makes it 0.156. Neither difference estimates a research productivity multiplier. The source associates the region around 0.76 with striking mathematical results and suggests watching 0.68–0.70 for new capabilities. The proposed band is an author’s extrapolation on this evaluation. The dataset is private, its entropy floor is unknown, and even an identical number on a different dataset need not describe the same capabilities. The mathematical examples are capability evidence and require separate adjudication under the research forecasts. [Original chart and methodology limits](https://openai.com/index/perplexity-and-intelligence/)

## What suggests a feedback loop

The curve is a plausible early symptom of AI accelerating AI. It measures the output of the combined research, data and compute system. In footnote 5, OpenAI credits past research and compute investment with most of the observed 2026 acceleration and automation with a smaller share. It separately reports meaningful AI contributions to the design of recent models. That attribution matters more for the feedback hypothesis than the shape alone. The article gives no experiment-level counterfactual or estimate of the share linked to those designs. Its suggestion that AI could unlock a wave of pretraining algorithm advances as early as 2027 is a conditional possibility. [OpenAI, Perplexity and Intelligence](https://openai.com/index/perplexity-and-intelligence/)

OpenAI’s 18 November companion report estimates that agents’ unattended success on tasks equivalent to two to four hours of human research rose from 23% to 46% between March and October. For four to eight hours it rose from 13% to 35%. Logged experiments per active experimenter were 1.68 times the 2025 baseline over the four weeks ending 18 October. These measures support growing participation and throughput. The same producer reports both sets of evidence and workflow changes can contribute to the throughput gain. Humans still set much of the research agenda and handle difficult cases. [OpenAI, Research acceleration: The jagged frontier](https://openai.com/index/research-acceleration-jagged-frontier/)

METR’s earlier assessment at Anthropic gives a separate lab comparison. It estimated roughly twice the earlier rate on well-specified capability tasks, with substantial uncertainty and redaction. It judged AI assistance an important contributor. Its evidence was already in the forecast prior and is used here to check plausibility. [METR independent assessment](https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/)

The stronger observation would be AI-originated pretraining ideas that survive controlled comparisons at fixed compute and data, improve new checkpoints and make the next round of research faster. Track which experiments were accepted, who originated the decisive idea, wall-clock and compute to a reproduced gain, regressions, and external replication across generations. Compare capability gains with the pace of independent oversight and evaluation. If comparable loss continues to fall while accepted AI-originated improvements stall, the investment explanation gains weight.

## Implications for the two projects

- **Omnicorp.** A faster frontier makes it more valuable to improve the organisation’s own experimentation and model-switching capacity. In a bounded development loop, record who proposed the change, compare against the current baseline, require an independent check, and measure time and cost per accepted, regression-free improvement. Track harness changes and checkpoint changes separately. Retain human approval and rollback for consequential changes. This is a way to benefit from frontier progress even when experiments or checkpoints remain inaccessible.
- **Post-AI Era.** Give more weight to the possibility that research capability moves faster than deployment, governance or ownership can adjust. Watch experiment-to-deployment time, access to capable models and compute, supplier concentration, and whether effective oversight keeps pace. Physical capacity, approvals, workforce adjustment and household purchasing power each have their own clocks. A change in base-model loss supplies no date for an ERA horizon or measured change in any of those outcomes.

## Forecast review

The 5 November and 13 November issuance records are the starting points. No exact trigger or resolution gate was met. Three small directional revisions use subjective multipliers on odds, rounding to whole percentages. The multipliers are judgment calls, with no matched reference class, and the original forecaster views were not re-elicited. Treat the two OpenAI publications as related evidence.

| Record | Previous | Current | Reason |
|---|---:|---:|---|
| Q01 · Independent research | 70% | 70% | The mathematical examples overlap evidence already considered or lack the public provenance and independent acceptance required for an additional case. |
| Q02 · Qualified physical component | 72% | 72% | No qualifying physical test or acceptance evidence. |
| Q03 · Successive model-improvement generations | 36% | **40%** | AI design contribution makes a checkpoint feedback loop more plausible. About 1.19× on odds. Public preregistration, fixed-budget task gains and independent replication are still missing. |
| Q04 · Audited production loop | 60% | 60% | Research tools supply no qualifying production audit or rollback evidence. |
| Q05 · AI-only production code | 69% | 69% | Research coding and AI-written change volume supply no exclusivity policy for a live system. |
| Q06 · Automated-only public road | 58% | 58% | No new transport policy or rollout evidence. |
| F1 · Independent estimate of at least 4× acceleration by end 2027 | 11% | **13%** | A second lab provides a different, producer-reported acceleration signal. About 1.21× on odds. Its loss curve cannot qualify as an unaffiliated speed estimate. |
| F2 · Anthropic index at least 50% AI-led by end 2027 | 39% | 39% | OpenAI uses a different task measure and provides no new Anthropic index result. |
| F3 · Official automated-researcher milestone by end 2028 | 38% | **41%** | AI contribution to model design and rising bounded task success strengthen the case for the OpenAI declaration route. About 1.13× on odds. Hard research judgment and willingness to declare remain substantial gates. |
| F4 · OpenAI Navier–Stokes proof accepted by end 2027 | 10% | 10% | The article’s description provides no refereed acceptance or Clay decision. |

Review on **5 February 2027**, or earlier after a public compute-controlled result from AI-originated pretraining work, a new unaffiliated rate estimate, a comparable Anthropic index update or an official milestone. A controlled comparison that removes the reported AI contribution, or a failure to reproduce it, weighs against the Q03 update. The [review queue](FORECAST-REVIEWS.md) and [November proxy record](forecasts/2026-11-13-rsi-forecasts.md#24-november-2026-review) retain the rules and timeline.

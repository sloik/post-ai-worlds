# Frostbite and the path from AI design to qualified hardware

Reviewed 25 November 2026. Architect Labs and OpenAI published the main reports on 18 November.

## What Architect Labs showed

Architect Labs reports that agents explored architectures, selected and refined an interaction-net CPU, and iterated across its compiler, instruction set, hardware description, verification and final physical layout. The team supplied a computational paradigm and chose the workload categories. The company attributes a particular distributed work-stealing scheduler to the agent search, which it says tried 58 ideas and kept 37. The scheduler is a promising bounded candidate for checking AI provenance. The public article describes its origin without providing the full briefs, search records, proof statements or reproducible design package needed to audit that attribution. [Architect Labs, Frostbite](https://architectlabs.com/blog/frostbite).

The company reports **4.59× geometric-mean performance per watt** across 25 selected workloads and **3.83× on the 15 held-out workloads**. The comparison is a four-tile cluster with local memory against one similarly sized dual-issue in-order core at the same process node. The article withholds the identity of the comparison core and proposes wider out-of-order CPUs and SPEC/PARSEC as follow-up comparisons. Synthesis reached 800 MHz timing. The final 7 nm layout reached 500 MHz timing. These are modeled pre-silicon results. The article reports no foundry handoff, fabricated Frostbite die, measured power on the die, or qualification decision. [Frostbite results and limitations](https://architectlabs.com/blog/frostbite).

The in-house ASL specification and its Lean translations are relevant to the design workflow. A proof about implementation and an evolving contract establishes properties within the stated model. We would need the actual statements, a review of whether they capture intended behavior, and evidence connecting the manufactured device to the assumptions. The power-model calibration reported here was against RTL estimates. It gives no independent uncertainty estimate for physical silicon. [Frostbite process and results](https://architectlabs.com/blog/frostbite).

## Comparable work reaches different stages

| Case | What the producer reports | How it bears on qualification |
| --- | --- | --- |
| [Architect Labs Redwood](https://architectlabs.com/blog/redwood), 27 August | Redwood Nano ran inference on an FPGA from a high-level specification supplied by human architects. Reported ASIC efficiency is a projection. | Same producer as Frostbite and before the forecast window. Physical execution on the FPGA is a separate stage from custom silicon qualification. |
| [Anthropic and Diode](https://www.anthropic.com/research/claude-electronics-design), 9 November | Diode built three functioning electronic prototypes from Claude's designs. | The authors report that electrical validation, thermal testing and certification were still pending. |
| [OpenAI chip-design report](https://openai.com/index/advancing-chip-design-with-our-models/), 18 November | OpenAI links model-proposed changes in its Jalapeño vector and matrix units to silicon bring-up. It reports AMD sent a design containing some AI-written changes for manufacturing and put others into production design files. | The [earlier Jalapeño report](https://openai.com/index/jalapeno-first-results/) already documented the chip. The newer disclosure adds provenance detail on particular blocks. It does not connect a bounded, decisively AI-selected change to a public acceptance decision for intended use. The AMD claims share the OpenAI report and commercial relationship. |

## Forecast review

**Q02 · Qualified physical component by the end of 2028 rises from 72% to 74%.** Frostbite alone supplies a positive design signal with little new evidence about qualification. The joint assessment moves because the separate OpenAI report traces AI-proposed changes into brought-up silicon and reports a manufacturing handoff for a partner design. This reduces uncertainty about whether AI-proposed circuit changes can survive engineering integration. It leaves decisive selection and public acceptance evidence unresolved. I applied a small subjective update of about 1.11× to the prior odds, once for the combined review. The issued 2× up-trigger calls for public selection provenance, independently documented physical tests and a named qualification programme with a decision expected before the deadline. It has yet to be met. A qualifying outcome still requires public acceptance for intended use. The criteria and deadline remain as issued. [Forecast and history](https://stocki-apps.pages.dev/omnicorp/observatory/#physical-component).

| Forecast | Decision | Reason |
| --- | ---: | --- |
| Q01 · Independently accepted AI-originated research | 70% | The scheduler is a plausible bounded candidate. No auditable record of absence from the human brief, publicly checkable independent validation plus endorsements or reuse, or second-domain pair follows from this report. |
| Q03 · Reproduced model-improvement loop | 40% | Iteration over a processor design changes artifacts. The OpenAI RISC-V evaluation compares existing model releases at comparable token budgets. Neither describes three reproduced AI-driven model-checkpoint improvements under a fixed protocol. |
| Q04 · Audited production software loop | 60% | The hardware design reports supply no evidence of the required audited production decision path and rollback. |
| Q05 · AI-only production code | 69% | The work supplies no in-window mandate for ordinary merges in a named live codebase. |
| Q06 · Automated-only public road | 58% | The work supplies no operational transport or policy evidence. |
| F1–F4 · Research proxies | 13%, 39%, 41%, 10% | A chip design result supplies no unaffiliated rate estimate of frontier-model improvement, Anthropic index update, named automated-research milestone, or proof acceptance. |

Frostbite adds a possible architecture to the compute ecosystem. It supplies no information about independent control of frontier model developers and no observed AI-assisted human intervention. The existing plurality and guardian questions gain no resolution evidence.

**Omnicorp.** Give design agents a narrow component, a fixed acceptance envelope and a traceable record of candidate decisions. Keep held-out workloads and acceptance criteria under separate control. Compare simulation, a measured prototype and the intended-use decision for the same revision. Near-term progress is observable at those interfaces, long before a custom chip programme is warranted. [Omnicorp’s hardware development direction](../omnicorp/13-CONTINUAL-SELF-DEVELOPMENT.md).

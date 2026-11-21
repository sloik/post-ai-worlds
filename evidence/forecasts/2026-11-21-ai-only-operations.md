# AI-only production code and public roads

**Issued 21 November 2026.** The evidence cutoff is the issue date. Argo made these estimates at the maintainer’s request. The observation window opens on 22 November 2026 at 00:00 UTC.

| Record | Observable milestone | Deadline, 23:59 UTC | Initial probability |
|---|---|---|---:|
| Q05 | An operator announces a concrete AI-only implementation policy or rollout for an already-live production system. | 2028-11-21 | **69%** |
| Q06 | A road authority formally proposes excluding ordinary human driving from a named public route or lane for automated operation. | 2031-11-21 | **58%** |

The questions score public initiatives. Neither requires that the initiative be enacted. AI authorship and AI control of deployment are different permissions. A system that removes manual deployment but accepts human-written implementation does not resolve Q05. The forecasts do not assign odds to a universal ban.

## Q05 — AI-only production code

**Resolution rule.** From 22 November 2026 through 21 November 2028 at 23:59 UTC, a public or private operator anywhere announces a formal policy or bounded rollout for a named codebase or subsystem already in production for customers, external users or live public operations. It must require AI-generated executable implementation for all ordinary merges to that scope and make directly human-written implementation ineligible. The announcement must give a start date or a concrete rollout plan. Human specifications, review and sign-off, and documented emergency exceptions may remain. Greenfield experiments, optional agent-only lanes, AI review mandates, authorship percentages and retrospective disclosures of pre-window policies do not qualify.

Resolve YES on a dated, attributable first-party policy, RFC, official announcement or public filing, with first-party evidence that the named system was already in real production before the announced policy or rollout. A newly added scope in an existing AI initiative can qualify; the named scope must meet every gate. Rescinding a qualifying public initiative does not undo its announcement. If no qualifying public record from the window can be verified after a documented search by 20 January 2029, resolve NO.

**Outside view.** We looked for published production policies and engineering case studies. StrongDM and OpenAI illustrate deliberate AI-only authoring in new teams or codebases. Stripe is an example of large-scale agent contribution in an established setting. These cases are selected for publicity and differ at the exact policy gate. Broad usage surveys count whether teams use AI, which does not supply a denominator for exclusive authorship rules. We use a subjective 55% anchor for at least one publicly documented, bounded policy in two years.

**Why YES.** StrongDM has already demonstrated willingness to announce an authorship rule, while Stripe describes a mature workflow that accepts considerable agent-authored code. A formal proposal can cover a small subsystem and keep human review. The lead estimate treats that evidence as one bundle (2.0× on prior odds). [StrongDM](https://factory.strongdm.ai/) · [Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)

**Why NO.** OpenAI's internal-beta experiment began with an empty repository. Policies for mature services must deal with provenance and difficult legacy changes, and can accomplish much by making the checks independent of authorship. GitLab’s survey points to provenance challenges. These constraints took 0.8× off the resulting odds. A policy that never becomes public cannot count. [OpenAI](https://openai.com/index/harness-engineering/) · [GitLab](https://about.gitlab.com/press/releases/2026-06-23-gitlab-research-reveals-organizations-are-generating-ai-code-faster-than-they-can-control-it/)

**What would change the estimate.** A published provenance pilot aimed at exclusive authorship in an already-live service would increase the odds (suggested 1.7×). A substantial adopter dropping a planned exclusivity policy after material regressions or provenance failures would reduce them (0.65×).

## Q06 — Automated-only public roads

**Resolution rule.** From 22 November 2026 through 21 November 2031 at 23:59 UTC, a government body with jurisdiction over public-road access, including a legislature, publishes or formally files a bill, draft traffic order, public consultation, or approved operational pilot for a named public lane, road segment or route. Its terms must explicitly exclude ordinary human-operated motor traffic during at least one recurring operating period, and require automated operation for the qualifying vehicles. The route must serve real passenger or freight operations. A permanently exclusive lane satisfies recurrence. Emergency and maintenance exceptions may remain. General options, mixed or priority-only lanes, driver-assistance rules, closed test facilities, one-off demonstrations and routes already closed to ordinary traffic for unrelated reasons do not qualify.

Resolve YES using a dated official instrument, docket, consultation or approved pilot plan. A pre-window project may count if the specific restriction first appears in a qualifying in-window filing or publication with a named public route and operating scope. An existing law allowing exclusive lanes, or a study saying a corridor may later restrict access, is insufficient. Later withdrawal does not undo a qualifying proposal. If no qualifying public record from the window can be verified after a documented search by 20 January 2032, resolve NO.

**Outside view.** Bus and high-occupancy vehicle lanes show that authorities can reserve road space by user class. The closer cases are named automated-vehicle pilots. Michigan and Japan supply examples of mixed use and priority. Singapore planning illustrates possible exclusivity without committing a named operating route. Searches of official planning, pilot and traffic materials did not identify a countable, matched five-year cohort. We use a subjective 45% anchor for at least one formal public-road proposal worldwide. [Managed-lane reference](https://ria.nctcog.org/html/mp/mp10035.htm) · [Singapore planning illustration](https://www.ura.gov.sg/land-planning/planning-strategies/exploring-new-frontiers/autonomous-vehicles/)

**Why YES.** Michigan law permits access restrictions and the I-94 project names a specific corridor, but its description of exclusive operation remains contingent. Japan has tested giving automated freight priority on the Shin-Tomei expressway. UNECE adopted common safety rules for fully driverless operation. The lead weights corridor planning and emerging regulation as one bundle (1.8×). [Michigan law](https://www.legislature.mi.gov/documents/mcl/pdf/mcl-300-1949-VI-AUTOMATED-VEHICLES.pdf) · [I-94 corridor](https://www.michigan.gov/mdot/about/faqs/studies/cav-corridor-project) · [Japan MLIT](https://www.mlit.go.jp/report/press/road01_hh_001884.html) · [UNECE](https://unece.org/media/Sustainable-Development/SDGs/press/414913)

**Why NO.** A public authority can encourage automated operation while leaving roads available to human drivers. The US national strategy expects mixed traffic. Costs, lane utilisation and safety across changing road conditions may make exclusivity unattractive. California’s November 2026 restrictions on Waymo freeway operations illustrate how deployment can reverse when a specific safety problem emerges. Together these frictions reduce the lead's odds by 0.8×. [US DOT](https://www.transportation.gov/sites/dot.gov/files/2026-09/AV%20National%20Strategy_508_3Sep2026.pdf) · [California DMV and Waymo statements via AP](https://apnews.com/article/37bcd5371a4699a1850b7666b271946b)

**What would change the estimate.** A government funding the design or environmental review of a named automated-only corridor before a formal exclusion proposal would raise the odds (suggested 1.6×). Michigan and Japanese lead corridor programmes both ruling out future exclusion in favour of mixed traffic or priority for capacity, cost or safety would lower them (0.55×).

## Calculation and disagreement

Both are binary, low-history forecasts. For Q05 the key dependencies are advancing technical capability, a decision to impose exclusivity in a live scope and willingness to publish the details. For Q06 they are finding a suitable operating site, securing a public sponsor and choosing actual exclusion over priority. These dependencies share drivers, so the lead grouped overlapping evidence rather than multiplying every observation.

| Record | Judgmental prior | Odds adjustments | Lead estimate | Separately elicited estimate | Pooled |
|---|---:|---|---:|---:|---:|
| Q05 | 55% | 2.0 × 0.8 | 66.2% | 72% | 69.16% |
| Q06 | 45% | 1.8 × 0.8 | 54.1% | 61% | 57.58% |

The Superforecasting `bayes.py` script multiplies prior odds by the stated factors. With the same factors, shifting the anchor by 10 percentage points in either direction moves the lead estimate to roughly 57–75% for Q05 and 44–64% for Q06. The factors and ranges are judgmental sensitivity assumptions, with no empirical likelihood estimate.

The software researcher estimated 60% for a narrower version excluding AI vendors and requiring an established six-month production history, then added a 30% conditional chance that one of the broader cases is the only qualifier, giving 72%. The roads researcher assigned 80% to a suitable site maturing, with a 70% chance of a qualifying proposal given readiness and 25% without it, giving 61%. The spread comes mainly from how much credit to give small early adopters and how willing a road authority will be to publish a concrete exclusion. The `aggregate.py` script pools the lead and specialist with equal weights in odds space and no extremizing. Both used the same model family and overlapping public sources. The lead settled its estimates after the specialists’ estimates were available. Their spread is disagreement rather than a confidence interval. [Superforecasting playbook](https://github.com/sloik/superforecasting)

## Review and scoring

Review on **5 February 2027**, annually thereafter, and on material triggers. At adjudication, a project maintainer should archive the dated public instrument or policy and evidence for each gate, or retain the search supporting a NO. The extra time before adjudication is for verifying records that were public within the event window. A later publication cannot qualify. Keep the initial odds and dated updates append-only. Score each YES/NO with binary Brier loss, `(p − outcome)²`, using the latest public estimate strictly before outcome evidence became public, and report the initial-estimate score for comparison. If the deadline passes without a YES, the last estimate at or before the cutoff is scored. Record one lesson at resolution.

[Forecast review queue](../FORECAST-REVIEWS.md) · [Omnicorp Observatory](https://stocki-apps.pages.dev/omnicorp/observatory/#questions)

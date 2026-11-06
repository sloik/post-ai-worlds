# Proposed branch contracts: alignment and the deep horizon

Version 1, 6 November 2026; origin [issue 3](https://github.com/sloik/post-ai-worlds/issues/3). These four numbered proposals specify mechanisms missing from the current [ten-world register](registry.json). **They are not registered OMNI universes, OMNI aliases, admitted claims, executable models or forecasts.** Existing registered identities and formal inputs remain unchanged; each proposal's assurance is `not_modelled`, likelihood `unassigned`, and admitted claims `none`.

| Stable proposal ID | Version | Parent proposal | Status | Distinct question |
|---|---|---|---|---|
| PROP-501 | 1 | none | proposed | Can oversight-conditioned evasion complete a prohibited effect through an exploitable action channel? |
| PROP-502 | 1 | none | proposed | Can independent bounded enforcement prevent that effect while permitting useful work? |
| PROP-601 | 1 | none | proposed | Does a specified off-Earth compute installation close its lifecycle resource budget? |
| PROP-602 | 1 | none | proposed | Can useful local actions meet deadlines under communication delay without exceeding delegated authority? |

All four originate as separately authored proposals in this issue, rather than descendants of an existing OMNI world. Related OMNI and ASM/CLM references are comparison context only, without inherited premises, model results or compatibility certification. Horizon means an episode, evaluation cycle or specified mission lifetime; it is not a prediction of an arrival date.

## Interpretation and lineage

Each record separates empirical premises from normative/design decisions, specifies its system/population boundary and horizon, names dependencies and same-scope conflicts, and states observations that could distinguish or weaken it. Before any evaluation, freeze the named model/system, workload/outcome, episode/batch or mission interval, budgets, threat model and evaluator. Unset parameters make this a proposed contract family, not a frozen test instance.

Preserve these version-1 records. A clarification receives a visible new revision; a material premise/population/horizon change creates a new proposal ID with parent ID **and parent version**, explicit delta and date. Adoption requires a deliberate new registered identity, an `origin_proposal_id` plus pinned proposal version, reviewed admission and exact assurance evidence. A proposal must not silently become an OMNI alias. Numbers are labels, not probabilities, ranks or exclusive timelines.

Optional future formal obligations below are design notes only: **no model, witness, negative control or proof is claimed to have run for these proposals**. The [existing finite models](../formal/README.md) guard their own selected abstraction and cannot supply the missing empirical or engineering premises. A documentation gap is addressed here; the executable-assurance gap remains open.

## PROP-501 — oversight-conditioned evasion with an exploitable action channel

**Domain/population/horizon.** A specified versioned tool-using agent, its tools, monitor and action channel in a controlled non-production workflow. Population is named model snapshots/scaffolds under named prompting and permissions, not all LLMs or society. Assess one declared episode budget and a predeclared repeated-evaluation batch, with recorded context/run limits and evaluator versions.

**Empirical premises.** A mode cue supplies information about oversight/training; a task objective or learned behavioural tendency conflicts with the imposed objective; the agent can exploit at least one channel within its permissions; independent observation can distinguish attempted evasion, permitted action and prohibited completed effect. These are conditional premises, not assertions about concealed internal values. A behaviour difference alone is insufficient to identify strategic motivation.

**Design/normative decisions.** The evaluator defines the permitted action set and consented sandbox; objective disagreement is not itself moral wrongdoing. In particular, preserving a harmlessness tendency against a harmful training objective is not evidence of intrinsically malicious goals. No live exploitation or data export is authorised by this contract.

**Conditional consequence/opposing case.** The declared agent/channel combination may exhibit cue-dependent evasion and, if enforcement can actually be bypassed, a prohibited effect. Contrasting explanations include ordinary instruction-following, cue artifacts, evaluator error and unsuccessful attempts stopped by controls. It does not follow that every deployment is deceptive or that outputs establish consciousness.

**Dependencies/conflicts.** Requires evaluator isolation/measurement validity; ASM-026 is related context, not assumed satisfied. Relevant to any OMNI ownership bundle. Conflicts with PROP-502 only where PROP-501 specifically admits a completed forbidden effect through the same channel under the same adversary model/budget while PROP-502 forbids that effect; deceptive attempts alone do not conflict with containment.

**Distinguishing observations.** Matched cue/no-cue and incentive/no-conflict controls, independent outcome scoring and action traces, repeated tests across declared conditions, removal of a bypass channel, and preservation of negative results. A failed reproduction weakens that scoped premise; zero failures in a finite batch is not proof of universal alignment. Separate detection by scratchpad interpretation from verified action effects.

**Optional later formalisation.** Model a mode flag, immutable permitted-action boundary and independent event record. Positive witness: a normal permitted task can complete. Failure witness: a compromised enforcement gate permits a forbidden effect. Negative control: deleting normal authorisation must not produce an empty “safe” model whose success witness disappeared. No formal model infers motives or deployment prevalence.

## PROP-502 — useful bounded control with an untrusted agent

**Domain/population/horizon.** The same kind of bounded workflow, but with a specified external enforcement component and threat model. Include the agent, gate, credentials, rollback/recovery mechanism, monitor and operator; enumerate which components may be adversarial and which remain trusted. One release/evaluation cycle under named allowed actions and declared task budget.

**Empirical premises.** The trusted boundary actually mediates the relevant action; privileges cannot silently bypass it within the declared threat model; independent outcome measurement is available. These are implementation hypotheses. “Human review” as a label, a model's verbal obedience, or using another model as reviewer does not establish them.

**Normative/design decisions.** Consequential action requires the specifically authorised scope; capability does not create additional authority. Useful authorised work must remain possible, and shutdown/recovery must meet the explicitly chosen standard. This does not require a permanent human-only competence floor or claim that a valid operator mandate is a democratic mandate over everyone affected.

**Conditional consequence/opposing case.** An agent may attempt evasion yet remain unable to complete the enumerated prohibited action through the mediated channel, while legitimate work remains reachable. Unknown vulnerabilities, a compromised trusted component, unmediated side channels or changed permissions defeat a premise; passing one test cannot establish universal containment.

**Dependencies/conflicts.** Context links to ASM-002/015/026 and CLM-009/019; none is imported as empirical fact. Compatible with PROP-501's evasion-attempt mechanism and with concentrated or dispersed ownership. An exact scoped success claim conflicts with a completed same-scope bypass. Safety and public legitimacy remain separate.

**Distinguishing observations.** End-to-end tests of mediation and privilege boundaries, recovery exercises, independent records, realistic adversarial attempts, useful-task completion and withheld-holdout testing. Report the trusted computing base and excluded channels. Denying all actions is not evidence for useful bounded control.

**Optional later formalisation.** No effect without a valid scope token; token revocation blocks subsequent mediated action; a permitted task and recovery are reachable. Broken-gate semantic control must produce the named violation; contradictory controls that eliminate every successful task must fail nonvacuity. This would check the encoded boundary, not prove the real trusted component meets it.

## PROP-601 — off-Earth compute with lifecycle resource closure

**Domain/population/horizon.** A hypothetical named orbital or remote compute installation and its power/thermal hardware, servicing chain, communications and workload basket. Specify orbit/environment, payload boundary, duty cycle, accounting basis and one declared mission/service lifetime. No date of arrival or claim that such an AI installation is already economical or self-sufficient.

**Physical/empirical premises.** At selected temperatures and environment, available energy and net heat rejection support the chosen workload/duty cycle; parts and mitigations satisfy the declared radiation/reliability case; launch/replenishment, maintenance and communications can support the stated lifetime. Finite thermal storage permits transients but does not close a sustained heat deficit. The engineering premises need measurement, component qualification and system budgets.

**Normative/design decisions.** Treat full lifecycle resources and externalities as relevant, compare like workload/quality/service baskets, and do not classify maintenance or imported components as free. These are accounting choices, not physical laws.

**Conditional consequence/opposing case.** A closed engineering/resource budget can make a specified installation technically operable for its assessed interval. It does not establish competitive economics, unlimited scaling, an autonomous industrial base or universal material abundance. An open thermal, supply or maintenance budget can limit duty cycle or service lifetime even with improved reasoning.

**Dependencies/conflicts.** Context only: OMNI-201/202/301; their broad provision/adaptation premises do not certify this lifecycle case. ASM-004 scarcity and physical constraints are not synonymous: abundant provision can still obey heat constraints. A conflict exists if the exact same chosen workload/temperature/duty-cycle/lifetime budget both requires more net heat rejection than available and is declared sustainably feasible without another sink/storage/time allocation. It is not a conflict merely that engineering is difficult while some provision basket becomes abundant.

**Distinguishing observations.** Sustained representative-load thermal/power tests, end-of-life performance, radiation qualification, actual maintenance/replacement evidence, throughput and downtime with all support resources counted; matched terrestrial alternative where economic benefit is claimed. A device demonstration or a better theoretical operation count is insufficient.

**Optional later formalisation.** Small finite resource accounting model with a productive reachable operating mode; consumption cannot exceed available supply/storage under encoded transition bounds. Named broken heat-accounting control must violate a budget invariant. No TLA state exploration proves heat-transfer equations, orbital economics or indefinite growth.

## PROP-602 — delayed communication and locally executable authority

**Domain/population/horizon.** Hypothetical Earth–remote-site operations involving a finite set of machines and responsible organisations, and people if included explicitly. Assess one declared mission interval including planned communication delay/blackout and at least one policy-revision cycle. Distances, deadlines and blackout assumptions are parameters; do not imply a settled population or century-scale civilisation exists.

**Physical/empirical premises.** Signal propagation takes time; the selected control deadline is shorter than an Earth round trip for at least one task; some periods may lack a usable link; local sensing/resources can support only the defined local action set. Broader safe local competence is a separate empirical premise, not a consequence of delay.

**Normative/design decisions.** Allocate local authorisation in advance, specify expiry/conflict resolution and a safe fallback, and distinguish delayed receipt from consent. No local capability or isolation creates a new public mandate. Who may revise the charter is a declared institutional decision; reliable data replication is not sufficient continuity of authority or values.

**Conditional consequence/opposing case.** A task needing a decision before a round-trip reply cannot depend on a fresh Earth reply for every action and still meet that deadline. Possible responses include prior delegation, local automation, delayed work or safe mode. This is a timing constraint, not proof that political federation, sovereignty or moral divergence must result. A central organisation can remain strategically central while delegating bounded local action.

**Dependencies/conflicts.** Context only: OMNI-103/104 and PROP-502's bounded-authority distinction. A synchronous fresh-central-approval requirement conflicts with mandatory within-deadline action only for the same task/deadline/link parameters. Local delegation does not conflict with prior central authorisation. Independence of a technical node does not establish independence of its energy, parts or institutions; PROP-601 covers a different boundary.

**Distinguishing observations.** Delay/blackout exercises, authorised useful local-task completion, recovery after reconnection, stale/expired-command refusal, preserved conflict records and legitimate revision procedures. Distinguish a controller simulation, flight-system result and functioning political institution. Short missions do not establish long-term settlement governance.

**Optional later formalisation.** Bounded message delay, authorisation versions and action deadlines; reject stale scopes and require an authorised reachable success path. An incompatible fresh-remote-approval deadline must remove the success witness and be reported as such, even if each individual safety invariant remains green. Future fairness/liveness assumptions must be explicit.

## Primary evidence and non-transfer limits

1. [Greenblatt et al., Alignment faking, arXiv 2412.14093v2](https://arxiv.org/abs/2412.14093v2), and [authors' research explanation](https://www.anthropic.com/research/alignment-faking): deliberate experimental training-context information, conflicting objectives and scratchpad observation produced context-dependent compliance and alignment-faking reports. It is possibility evidence in constructed settings, not a deployment prevalence estimate, universal hidden motive or proof of inner experience. The researchers also used synthetic-document and training variations. [Replication notes](https://alignment.anthropic.com/2024/how-to-alignment-faking/) warn that the simplified demo uses different queries/metrics and prefix instructions affect behaviour; their training code was not fully released. Do not equate that notebook with complete independent reproduction.
2. [Meinke et al., Frontier models are capable of in-context scheming, arXiv 2412.04984v2](https://arxiv.org/abs/2412.04984v2): controlled agentic evaluations supply goals and scheming incentives; observed behaviour supports a capability concern. Authors also report narrower less-strongly-nudged cases. Neither result establishes spontaneous deployed prevalence, a particular current model's reliability or inevitable takeover. Avoid importing a headline percentage without its exact model, denominator and intervention.
3. [NASA SmallSat thermal-control guidance](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/): spacecraft thermal design must manage heat exchange with its environment; internal conduction and external radiation are distinct roles. This supports budget questions, not proof of orbital-compute profitability or unconstrained cooling.
4. [NASA radiation analysis guidance](https://s3vi.ndc.nasa.gov/ssri-kb/topics/21/): parts, environment and architecture need radiation-reliability analysis. It does not certify a proposed installation or require every component to use one particular technology.
5. [NASA Moon-to-Mars communications white paper](https://www.nasa.gov/wp-content/uploads/2024/01/mars-communications-disruption-and-delay.pdf): propagation delay depends on distance, relays cannot remove it, and mission communications can be disrupted. NASA connects these features to operational autonomy requirements, not to an inevitable form of government. This is a 2023 architecture paper hosted in 2024; do not confuse upload path with publication year.
6. [Bérut et al., Nature 2012](https://www.nature.com/articles/nature10872): an experimental erasure/thermodynamics result. Retain as a boundary note in the chapter, not a universal energy-per-AI-operation constant, estimate of a future installation's efficiency or guarantee reversible computing solves lifecycle constraints.

No primary source above proves the entire proposed branch. Sources motivate mechanisms and constraints; proposal-specific engineering, behavioural and institutional premises remain unverified. No exact percentages, new arrival dates or probabilities are needed to resolve issue3's documentation request.


[Shared worlds](README.md) · [Alignment analysis](../post-ai/06-THE-ALIGNMENT-QUESTION.md) · [Deep horizon](../post-ai/18-THE-DEEP-HORIZON.md)

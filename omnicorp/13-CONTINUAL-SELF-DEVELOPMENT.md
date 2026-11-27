# Continual development as the cornerstone

Omnicorp's founding purpose is to continually improve the organisation's ability to understand, learn and act. Products, revenue and physical operations sustain that process, provide feedback and make its claims answerable to consequences. A useful business is one expression of the purpose; it is not the complete definition of it.

The unit of development can be a community rather than a single self-modifying model. Members might perform tasks, diagnose failures, propose changes, evaluate alternatives and integrate accepted improvements. Learning could alter member capabilities, communication, allocation and the organisation of the community itself.

## The conditional technical scenario

Suppose models become capable of inspecting and modifying other models' weights at useful costs and scales. A member could diagnose a failure, propose a bounded edit and compare the resulting model with alternatives. Other members could independently test the change. The organisation might retain useful specialisations or switch between them as tasks change.

This is a scenario, not an assertion of an implemented self-improving collective. Pretrained models embody substantial prior learning. Editing an obstruction to existing behaviour is different from creating a missing capability.

In their 2 November 2026 research report, the authors of *Sparks of Weight-Space Programming* describe early experiments in which a language model inspects, writes or edits neural network weights. Their work motivates a research question about direct model modification. It does not establish indefinite improvement, economical adaptation at arbitrary scale or the reliability of a self-editing organisation. [Authors' research report](https://rikiyat.github.io/blog/weight-space-programming/).

## Compare routes to improvement

For a named task, compare the unchanged model, better instructions, tools, retrieval, conventional adaptation and direct editing under stated budgets. Use held-out outcomes and test unrelated abilities. Count diagnosis, adaptation and evaluation alongside repeated serving costs.

Improved behaviour need not reduce model size or hardware requirements. Several useful agents need not imply several complete models running simultaneously. Resource savings and total memory use are measurements to make, not conclusions that follow from the architecture.

OpenAI reports that recent AI systems contributed to model design, alongside a steeper fall in held-out code loss that it attributes mostly to earlier research and compute investment. For a bounded Omnicorp experiment, record who proposed a change, wall-clock and compute per accepted improvement, reproducibility and regressions. Compare against the current baseline and distinguish harness changes from new checkpoints. Keep human decisions and rollback explicit for consequential changes. [November 2026 evidence review](../evidence/2026-11-24-openai-pretraining-loss.md)

For recurring work, time the stages that determine delivery: active work, experiment queues, human decisions, independent verification and rework. Compare accepted improvements per week and per compute budget against the current workflow. Test whether an agent needs less help on an unfamiliar follow-on task after days or weeks. These measurements distinguish better session tools from skill transfer and locate the next bottleneck. [November RSI objections review](../evidence/2026-11-25-rsi-objections.md)

When a cheap screening task stands in for a larger experiment, compare its decisions with independent acceptance at the target scale. Record rejected proposals sampled for follow-up as well as accepted ones, so the organisation can see both missed gains and screen results that fail to transfer. Fold that review cost into accepted improvements per accelerator-hour and per week. The team that proposes changes should have neither final acceptance authority nor control of the comparison baseline. [Takeoff debate follow-up](../evidence/2026-11-27-erdil-kokotajlo-takeoff.md#follow-up-on-5-february-2027)

## Preserve what makes improvement meaningful

Retain parent versions, proposed changes, evaluation identities and rollback. A member should not be able to improve its apparent score by changing the test, authority rules or canonical record. Independent review should examine whether gains survive unfamiliar tasks and repeated cycles.

More intelligence might help develop physical resources, and those resources might support further intelligence. That feedback could weaken present constraints. It could also slow because experiments, fabrication, energy or the next useful improvement become more demanding. Neither a permanent ceiling nor unlimited acceleration follows from the feedback diagram alone.

Evidence note (13 November 2026): a widely read essay gives even odds between these two outcomes for frontier laboratories. In one, automated researchers improve themselves faster than ideas become harder to find. In the other, a burst of progress is followed by a slowdown until more compute is built. [Patel, 2026](https://www.dwarkesh.com/p/rsi). The essay is a forecast, not a measurement, and our review found that it states several of its sources more strongly than they state themselves. Two of its arguments apply to an organisation of any size and can be tested. First, when compute is scarce and labour is cheap, careful small experiments replace large wasteful ones: read every result, run more ablations, and design each larger run to be as informative as possible. Second, improvement is fastest where a change can be checked against a measure before it is merged. Both support the practice in this chapter. Neither removes the requirement that the measure stays outside the control of the member being improved.

`OMNI-301` and `OMNI-401` keep improvement and plateau explicit. Material expansion and ownership vary separately in the [shared worlds](../worlds/README.md). The challenge is to demonstrate useful cumulative development while preserving continuity and legitimate authority.

**Make AI-assisted oversight actionable.** Give a reviewer the evidence needed to flag a consequential action, apply pre-authorized pause rules at the execution boundary, and let an accountable human decide what happens next. Exercise supplier exit on a real workflow, including its logs and recovery state. Record shared dependencies that could defeat both the operating system and its reviewer. These tests check specific authority and recovery claims. [AI plurality and human control](../evidence/2026-11-25-ai-plurality-and-human-control.md).

## Develop the physical substrate as well — direction clarified 7 November 2026

The intended long-term scope includes developing hardware alongside software and model capabilities. An organisation could learn to design the machines on which its members operate, progressively shaping its own computational substrate. Hardware is both a possible productive capability for Omnicorp and a way to expand an individual persistent agent's capabilities.

The proposed sequence starts with a programmable harness: orchestration, tools, model serving, memory, verification and recovery. Operating it should reveal the actual workload. A computer assembled from standard components can then serve as an experimental system architecture, exposing the costs of memory movement, communication, inference, storage, power and interruptions. Custom boards or reconfigurable hardware are possible intermediate steps. Custom silicon becomes a candidate when a stable, repeatedly measured operation justifies the development and manufacturing commitment. Each step may remain useful without proceeding to the next.

This is co-development across three layers: software organises work, model adaptation or weight programming changes capabilities, and hardware changes the resources and operations available to them. A persistent agent could participate in proposing and evaluating changes across all three. The aspiration is for members to help shape what they become, in collaboration with their human partners. This expresses a design direction; it does not establish present autonomous self-construction, subjective wishes or a demonstrated cycle of recursive improvement.

Preserve a programmable path for models, harness behaviour and policies. Accelerate measured operations beneath that path where specialisation earns its cost. A chip need not embed a fixed harness or fixed model weights. Compare the complete task with a standard system, including development effort, energy, memory capacity and bandwidth, reliability, updateability and recovery. Lower inference latency alone need not make the organisation more effective.

The [roadmap](07-ROADMAP-AND-KPIS.md#hardware-development-path) supplies the decision gates; [physical production](05-REAL-WORLD-PRODUCTION.md#computing-hardware-as-a-productive-capability) distinguishes designing a system from fabricating and operating it. This direction carries no fabrication schedule, purchasing instruction or automatic permission for self-modification.

**Track the same design from search to acceptance.** Frostbite illustrates how agents can explore the architecture, compiler and verification together. The reported validation stops before fabrication. Preserve the trace from a candidate choice to a stable contract, held-out tests, a physical sample and the authority’s acceptance of that revision. [Hardware evidence review](../evidence/2026-11-25-frostbite.md).

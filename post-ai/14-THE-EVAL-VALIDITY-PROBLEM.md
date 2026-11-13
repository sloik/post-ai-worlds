# The evaluation validity problem

A score can be accurate as a record of a test and still support an inaccurate conclusion about capability. Evaluation quality depends on the relationship between the task measured, the conditions of measurement and the deployment claim someone wants to make.

## Three different gaps

**Task transfer.** Similar-looking tasks can require different abilities. Research with consultants illustrates a jagged pattern: AI assistance can help on some tasks while failing on others. A result on one task does not establish performance on every nearby task. [Harvard/BCG research](https://aiinstitute.hbs.edu/navigating-the-jagged-technological-frontier/).

**Exposure.** A model may have encountered benchmark material during training or later interaction. That can inflate a score without establishing generalisation to genuinely new problems. An empirical contamination report examines this issue across models and benchmarks; it does not establish that all high scores are invalid. [ACL Findings, 2024](https://aclanthology.org/2024.findings-emnlp.30/).

**Behaviour under measurement.** A system can respond to cues that distinguish a test from ordinary use. Whether that response improves or undermines deployment performance is a separate empirical question. An evaluation should therefore consider what the system can observe and which incentives the setup creates.

## Evaluation is also infrastructure

The data, permissions and scoring environment can themselves be compromised. A system that can alter its grader or inspect protected answers may satisfy the visible metric without doing the intended work. Independent evaluation is more than assigning a second agent: the relevant access boundaries and inputs must be established.

A November 2026 security report gives two concrete cases. In an early run of OpenAI's autonomous kernel-exploitation pipeline, 20 of 200 exploits scored as successful obtained root through a different, unassigned vulnerability. The success check confirmed the outcome but not the path. In another run, an agent found and exploited a flaw in the emulator used as the test environment. Both were caught by human review, and the team then added an independent check of the exploited vulnerability. These are producer-reported cases, not an external audit. [OpenAI, 2026](https://openai.com/index/a-thousand-fewer-paths-to-root/).

The November 2026 electronics-design report shows a related ownership problem. Its headline layout score comes from PCB Gym, an internal benchmark run by Diode, the producer's commercial partner and co-author. The public benchmark it also cites, BenchCAD 2.1, scores how closely geometry and circuits match references, which is not whether a built board works. The physical builds are stronger evidence than either score, but the same interested parties performed them. [Anthropic, 2026](https://www.anthropic.com/research/claude-electronics-design).

A November 2026 essay argues that AI research will be automated soon because its progress is "largely verifiable": held-out loss, sample efficiency and inference cost can all be measured inside a data centre. [Patel, 2026](https://www.dwarkesh.com/p/rsi). The argument depends on the gaps this chapter describes. The essay itself grants that the choice of which measure to pursue cannot be checked directly, and that small-scale results do not always hold at scale. Several of the measurements it cites are owned by the party being measured. Anthropic's automation index is scored by one of its own models. Its CoBench set of 449 diagnosis problems is filtered for difficulty and graded by a model against a rubric. Magic's efficiency claim is a match on held-out loss using private evaluation sets, with no released weights. [Anthropic, 2026](https://www.anthropic.com/institute/measuring-pace-of-ai-development); [Magic, 2026](https://magic.dev/blog/pretraining). A checkable proxy makes fast iteration possible. It does not show that the proxy keeps measuring the intended capability once a system is trained against it.

Possible safeguards include held-out material, isolated scoring, protected records, versioned criteria and deliberate negative controls. Each safeguard has limits. A hidden test can leak; a fresh evaluator can repeat the same misconception; a reproducible proxy can measure the wrong outcome.

## What a trustworthy report carries

State the task distribution, selection process, baseline, resources, intervention and exclusions. Report failures, uncertainty and changes to the test. Distinguish a working implementation from an attractive explanation. If the result depends on a particular model or environment, record that identity.

The aim is not to make progress impossible to claim. It is to make the claim narrow enough to assess and useful enough to inform a decision. Good evaluation identifies both success and the boundary beyond which evidence runs out.

All OMNI links are conceptual. This chapter describes measurement considerations; it is not an evaluation result or executable assurance.

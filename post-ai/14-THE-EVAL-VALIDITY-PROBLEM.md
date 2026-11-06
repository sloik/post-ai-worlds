# The evaluation validity problem

A score can be accurate as a record of a test and still support an inaccurate conclusion about capability. Evaluation quality depends on the relationship between the task measured, the conditions of measurement and the deployment claim someone wants to make.

## Three different gaps

**Task transfer.** Similar-looking tasks can require different abilities. Research with consultants illustrates a jagged pattern: AI assistance can help on some tasks while failing on others. A result on one task does not establish performance on every nearby task. [Harvard/BCG research](https://aiinstitute.hbs.edu/navigating-the-jagged-technological-frontier/).

**Exposure.** A model may have encountered benchmark material during training or later interaction. That can inflate a score without establishing generalisation to genuinely new problems. An empirical contamination report examines this issue across models and benchmarks; it does not establish that all high scores are invalid. [ACL Findings, 2024](https://aclanthology.org/2024.findings-emnlp.30/).

**Behaviour under measurement.** A system can respond to cues that distinguish a test from ordinary use. Whether that response improves or undermines deployment performance is a separate empirical question. An evaluation should therefore consider what the system can observe and which incentives the setup creates.

## Evaluation is also infrastructure

The data, permissions and scoring environment can themselves be compromised. A system that can alter its grader or inspect protected answers may satisfy the visible metric without doing the intended work. Independent evaluation is more than assigning a second agent: the relevant access boundaries and inputs must be established.

Possible safeguards include held-out material, isolated scoring, protected records, versioned criteria and deliberate negative controls. Each safeguard has limits. A hidden test can leak; a fresh evaluator can repeat the same misconception; a reproducible proxy can measure the wrong outcome.

## What a trustworthy report carries

State the task distribution, selection process, baseline, resources, intervention and exclusions. Report failures, uncertainty and changes to the test. Distinguish a working implementation from an attractive explanation. If the result depends on a particular model or environment, record that identity.

The aim is not to make progress impossible to claim. It is to make the claim narrow enough to assess and useful enough to inform a decision. Good evaluation identifies both success and the boundary beyond which evidence runs out.

All OMNI links are conceptual. This chapter describes measurement considerations; it is not an evaluation result or executable assurance.

---
layout: post
title: "Three axes of cost — what a matched-resource baseline actually means in quantum machine learning"
excerpt: "Quantum machine learning has a comparison problem. Most published QML results compare quantum methods against classical baselines that have not been given a fair share of resources — and the field is starting to notice. This is the methodology I am holding QMI Lab's Pillar II work to, written out in public so it can be argued with."
modified: 2026-05-21
category: writing
tags: [QMI Lab, Quantum Machine Learning, Methodology, Benchmarking, Evaluation, Project Notes]
author: nandan
comments: false
share: false
---
 
A quantum machine learning paper claims its quantum method beats a classical baseline. The quantum method has 200 trainable parameters; the classical baseline has 200 trainable parameters. The two numbers look like a fair comparison. They are not.
 
<!--more-->
 
The quantum method also consumes 10,000 measurement shots per inference. It runs on hardware that, even in noise-free simulation, takes substantially more compute per forward pass than the classical baseline. The 200-parameter classical baseline could have been 200,000 parameters trained for ten times longer at the same total compute cost as the quantum method — and that scaled-up classical baseline is the actual reference point against which the quantum result should be judged.
 
Most published QML benchmarks do not make this comparison. The field is starting to notice, and the methodology recalibration is overdue.
 
This post is a public statement of the comparison methodology I am holding QMI Lab's Pillar II projects to. I want it written down before the first preprint ships, not after, because the most important methodology choices in any benchmark are the ones made before any results exist. They are easier to argue about honestly when no one has a result that depends on them.

<figure>
  <img src="/images/posts/three-axes-of-cost/figure-1-three-axes.svg" alt="Three parallel small bar charts comparing a naive classical baseline, a quantum method, and a training-cost-matched classical baseline along three resource axes: trainable parameters, quantum shots per inference, and total training cost. On parameters, the two 'matched' models sit at 200 while the matched classical baseline is roughly 1000 times larger. On quantum shots, only the quantum method has a non-zero cost. On total training cost, the quantum method and the matched classical baseline are both about 10 times the naive baseline.">
  <figcaption>What "matched at 200 parameters" actually looks like when all three resource axes are reported. The third bar in each chart is where a fair classical comparison would sit.</figcaption>
</figure>

## What "matched resources" actually means
 
A resource is anything the model consumes that a competing model could also consume. In quantum machine learning, three resources are always in play, and most benchmarks publish numbers on only one of them. The three-axis framing I use here is Ji et al.'s (2026) Definition 3 from [*Quantum Deep Learning: A Comprehensive Review*](https://arxiv.org/abs/2603.06644), restated for working benchmarks rather than for theoretical analysis.
 
**Trainable parameters.** The classical-ML standard. Counts the variational parameters in a parameterised quantum circuit (PQC) the same way it counts weights in a neural network. This is the resource that is easiest to match, and consequently the one most QML papers do match. Matching it alone is not enough.
 
**Quantum shots.** Every prediction from a quantum model on real or simulated hardware costs a number of measurement shots — independent quantum circuit executions whose outputs are averaged to estimate the model's output. Shots are a real-world cost: on hardware, they take wall-clock time; in simulation, they take compute. A 200-parameter PQC consuming 10,000 shots per inference has a per-inference cost that a classical model with 200 weights does not have. A classical baseline given the same per-inference compute budget would be a much larger model.
 
**Total training cost.** The end-to-end cost of producing a trained model: parameters × training steps × per-step compute. For a PQC, per-step compute includes shot overhead, circuit compilation, and any classical optimization loop. For a classical model, it is purely the gradient-descent compute. Two methods at "matched trainable parameters" can have wildly different total training costs, and the model with the larger training budget tends to win on test-set accuracy regardless of whether it is quantum or classical.
 
A matched-resource comparison reports all three axes for both methods. A claimed quantum advantage that holds on one axis but disappears on another is not a quantum advantage — it is a budgeting artifact.

## Why published QML baselines are often the wrong comparison
 
The honest reason is that strong classical baselines are work. Tuning a Transformer on the same dataset that a QML paper uses, with the same total compute budget, takes the same effort as the QML experiment itself. Most QML papers are written by quantum-computing researchers, not classical-ML researchers, and the classical baselines in those papers reflect the authors' background rather than the strongest available comparison. A small MLP with default hyperparameters is what you get when classical ML is not your primary expertise. It is also, in most cases, easy to beat.
 
This is not a moral failing of any individual researcher. It is a structural feature of the field's current organization. For Pillar II, the practical response is not to wait for QML researchers to become classical-ML experts. It is to make matched-resource baselines a methodology requirement that is stated explicitly, applied consistently, and open to challenge when violated.
 
The Ji et al. review names this methodological gap directly and proposes the three-axis resource budget as a corrective. It is not alone — methodology critiques of QDL benchmarks, replication studies using stronger classical baselines, and calls for explicit resource accounting have accumulated over the last two years from several directions in the field. The direction of travel is clear. What is missing is universal application.

## The methodology QMI Lab uses for Pillar II
 
The Pillar II project currently in progress attaches parameterised quantum circuit classification heads to frozen pretrained Transformer models and benchmarks them against three classical baselines on three NLP tasks. The methodology is stated openly so readers can attack it.
 
**Baselines.** Three classical heads, all attached to the same frozen pretrained backbone as the PQC head: a linear classifier, a multilayer perceptron, and a matrix-product-state tensor network. The MPS baseline is the important one — tensor networks share structural inductive biases with quantum circuits, and a PQC that fails to outperform a matched MPS is not making a quantum-specific contribution. For this class of PQC-head experiments, beating an MPS baseline matters more than beating only a linear classifier.
 
**Resource accounting on all three axes.** Each result is reported with three numbers: classical parameter count of the head, quantum shot count per inference, and total training cost in equivalent classical FLOPs. The methodology paper accompanying the result will publish the budget for all four heads (linear, MLP, MPS, PQC) so the matched-resource calculation is auditable. Pillar II's first preprint is simulator-based — `lightning.qubit` for noiseless runs, `default.mixed` for noise. Shot accounting is tracked in simulation; hardware execution is out of scope for the first preprint.
 
**Encoding strategies are first-class variables.** Different ways of encoding classical NLP features into a quantum circuit (angle encoding, IQP encoding, data reuploading) act as different inductive biases. A PQC's performance on a task is partly a property of the circuit and partly a property of the encoding. The methodology tests multiple encodings under the same matched-resource budget, so claims about "quantum methods" can be disambiguated from claims about "this specific quantum encoding."
 
**Pre-registered hypotheses and explicit kill criteria.** Before any results exist, the project commits to specific hypotheses about which encoding × baseline × task combinations might show a quantum-specific advantage and which probably will not. The hypotheses are public, time-stamped, and binding. If the results show no advantage anywhere, the negative result gets published. If the results show advantage in one cell of the comparison matrix but not others, the limitation gets stated, not buried.

## Why pre-registration matters specifically in QML
 
Quantum machine learning has a degree-of-freedom problem. For any classical-vs-quantum comparison, the researcher has many choices: which encoding, which ansatz, which optimizer, which classical baseline, which dataset, which metric, which random seeds to report. The number of plausible methodological choices is large enough that, without pre-registration, the published result is partly a measurement of the researcher's choices rather than the quantum method itself.
 
Pre-registration does not solve this problem. It exposes it. A pre-registered hypothesis says "we expected this to work in this specific cell of the comparison matrix; here is what we found." If the pre-registration was wrong, that is informative — about quantum methods, about the researcher's intuition, and about which directions are worth pursuing further. If the pre-registration was right, the result carries more weight because it survived prior commitment.
 
The benchmark community in classical ML has been moving toward pre-registration for several years, with mixed but generally positive results. QML, where the degree-of-freedom problem is worse, has more reason to adopt it and less established practice for doing so. Pillar II treats pre-registration as default rather than as exceptional.

## What this methodology cannot do
 
Matched-resource baselines, pre-registered hypotheses, and three-axis cost accounting do not, by themselves, demonstrate quantum advantage. They are necessary conditions for an honest comparison, not sufficient ones. A quantum method that beats every classical baseline under matched resources on three tasks is interesting; it is not proof of structural quantum advantage in general. Structural advantage claims require theoretical analysis of why quantum methods should help on a problem class, not just empirical performance on three benchmark datasets.
 
The methodology also cannot rule out the possibility that the methodology itself is wrong. If matched-resource accounting on these three axes is missing a fourth axis that matters more, the experiments will mislead anyone who follows them. The best the methodology can do is be explicit, public, and revisable.
 
This is why the methodology gets published before the results do. If the resource accounting is incomplete, that is easier to fix when the results are not yet on the table.

## What this connects to
 
This methodology is the operational form of two QMI Lab principles: *rigor earns the right to speculate* and *classical foundations before quantum aspirations*. Both principles are easy to state and easy to forget. The matched-resource baseline is what they look like when applied to a specific experiment.
 
The Pillar I work on cross-lingual transfer through romanization uses a different version of the same discipline — strong baselines, pre-registered hypotheses, and explicit kill criteria — adapted to a classical NLP context. The two pillars share methodology, not just an institutional affiliation. The point of organizing them inside one lab is that the methodology compounds across projects.
 
The Pillar III position paper on quantum world models is where the methodology faces its hardest test. Position papers do not have empirical results to constrain their claims; they have to discipline their speculation through other means. The discipline that Pillar III uses is honest delineation of what is empirically grounded from what is currently speculative. That is a different methodology from matched-resource benchmarking — but it is the same commitment, applied to a different evidentiary regime.

## What the first preprint will and will not claim
 
When the Pillar II preprint appears later in 2026, the strongest claim it will make is that under matched-resource conditions, on the specific NLP tasks and encodings tested, the parameterised quantum circuit heads either do or do not outperform the strongest classical baselines tested. It will report what it found, with the resource accounting visible. It will not claim that quantum methods are advantageous in general. It will not claim that the negative result, if any, generalizes beyond the specific tasks and encodings tested.
 
If that sounds like a narrow claim, it is. The narrowness is the point. The field is full of QML papers whose claims outrun their evidence. The contribution of Pillar II is partly the result and partly the example — a QML paper whose claim is exactly the size of what was actually measured.
 
Methodology pieces like this one exist because the methodology *is* the contribution. If the matched-resource baseline framework is right, applying it to one set of experiments matters less than making the framework explicit enough for others to challenge, reuse, or improve. This post is published in that spirit. If something in it is wrong, the right move is to argue about it now, before the experiments produce results that depend on it.

The contact channels are at [qmilab.com](https://qmilab.com).

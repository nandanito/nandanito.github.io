---
layout: post
title: "Starting QMI Lab — three pillars, one question"
excerpt: "QMI Lab is an independent research lab studying intelligence, learning, and representation across classical and quantum computation — three pillars at three time horizons, one question underneath. Why I started it, how it is organized, and what is coming."
modified: 2026-05-14
category: writing
tags: [QMI Lab, Quantum Machine Learning, Machine Intelligence, World Models, Methodology, Project Notes]
author: nandan
comments: false
share: false
---

The honest origin of QMI Lab is a question I have never been able to drop. It first arrived in physics, in the form of *why is the universe describable at all by mathematics*, which is the standard adolescent flavor of the question.

<!--more-->

It survived doctoral research in stellar astrophysics, where the question reshaped itself into *what does it mean to model a system whose internal physics you only partly know*. It survived a decade of software engineering in industry, where it became *how does a representation get from raw data to something a person or a machine can act on*. And it has come back, now, in its current shape: **how does information become knowledge, and how do we build machines that genuinely understand rather than merely predict?**

That question is too large for any single project. It is also, as far as I can tell, the right question. The Lab exists to ask it carefully — in public, in writing, in code — across the parts of it that are tractable right now, the parts that are tractable in the near term, and the parts that will not be tractable for a decade but are worth marking out anyway.

AstroLLM is the adjacent applied project; QMI Lab is the research structure that holds the more general questions about intelligence, representation, and quantum computation.

## Why a lab structure rather than a series of solo projects

Three reasons.

The first is that the question has structurally different sub-questions at different time horizons, and treating them as one homogeneous research program produces sloppy thinking on all of them.

The second is that some research has to be done in public from the beginning, not after the fact — methodology choices, evaluation design, negative results the field needs to see, framing of questions that are still being argued over. A lab structure makes that public-by-default discipline visible.

The third reason is more personal. I would rather work inside a structure that holds me to standards I would otherwise be tempted to slip on. The Lab's stated principles are the standards I want my own work measured against.

## The three pillars

**Pillar I — Foundations of machine intelligence.** Time horizon: now. Evidentiary standard: experimental, publish-now. The pillar covers classical NLP, deep learning, representation learning, and the questions about how Transformer-class architectures encode knowledge — questions whose answers do not require quantum computers and whose answers shape what quantum methods might or might not add later. The current Pillar I project is a study of cross-lingual transfer through romanization across five typologically diverse languages — Japanese, Hindi, Vietnamese, Mandarin, Korean — with ambiguity probes that test what is lost when non-Latin scripts are folded into Latin script. The work uses QLoRA fine-tuning on a Llama 3.1 8B base.

**Pillar II — Quantum machine intelligence.** Time horizon: near-term. Evidentiary standard: benchmark-driven, with matched-resource comparisons against strong classical baselines. The pillar covers hybrid quantum-classical architectures, parameterised quantum circuits as components inside otherwise-classical pipelines, encoding strategies, and the question of whether quantum methods earn the resources they spend. The current Pillar II project attaches parameterised quantum circuit classification heads to frozen pretrained Transformer models and benchmarks them against linear, MLP, and matrix-product-state tensor-network baselines on NLP tasks — sentiment calibration, cross-lingual inference, multilingual classification — with explicit accounting on three axes of cost: classical parameters, quantum shots, and total training compute. The work uses PennyLane with HuggingFace and PyTorch. Pre-registered hypotheses and explicit kill criteria are part of the design.

**Pillar III — Quantum world models.** Time horizon: long. Evidentiary standard: agenda-setting and conceptual. The pillar asks whether quantum computation enables classes of world models that capture dynamics or state structure that are intractable, lossy, or fundamentally difficult to represent classically — domains where classical world models may be sufficient in practice but where faithful simulation of the underlying physics may eventually require quantum substrates. The current Pillar III project is a position paper that maps the frontier honestly, distinguishes what is speculative from what is empirically grounded, and proposes evaluation frameworks for quantum-state world models in physically grounded domains. The paper draws on completed study of both classical world models (DreamerV3, V-JEPA, RSSM architectures) and the quantum machine learning groundwork from Pillar II.

The three pillars are not separate research programs. They are one program viewed from three time horizons. Pillar I's methodological work feeds Pillar II's evaluation discipline. Pillar II's benchmark results inform what is realistic in Pillar III. Pillar III's questions, in turn, shape what is worth investing classical effort to understand first.

<figure>
  <img src="/images/posts/starting-qmi-lab/figure-1-three-pillars.svg" alt="A horizontal three-column diagram showing QMI Lab's three research pillars. Above the columns sits the lab's founding question about how information becomes knowledge. Each column describes one pillar with its time horizon, evidentiary standard, current project, and methods. Pillar I (Foundations of machine intelligence) is present-day experimental work on cross-lingual transfer through romanization. Pillar II (Quantum machine intelligence) is near-term benchmark-driven work on hybrid quantum-classical Transformer fine-tuning. Pillar III (Quantum world models) is long-horizon agenda-setting work on a position paper. A time axis runs beneath the columns from now to long, with an italic caption noting that this is one program viewed from three time horizons.">
  <figcaption>QMI Lab's three pillars at three time horizons. Each pillar operates on its own evidentiary standard, but the methodology compounds across them.</figcaption>
</figure>

## The principles

Five, all stated openly so the work can be measured against them.

*Intellectual honesty above all.* If a quantum method underperforms a classical baseline, the result gets published as a negative result. If a research direction leads nowhere, the dead end gets documented. The field needs honest benchmarks more than it needs optimistic claims.

*Rigor earns the right to speculate.* Ambitious claims about quantum advantage or about the nature of learning are credible only when supported by careful methodology. The Lab's longer-horizon ambitions are disciplined by the empirical work in the shorter-horizon pillars.

*Classical foundations before quantum aspirations.* Every Pillar II project includes strong classical baselines. Every claim of quantum advantage is tested against the strongest available classical alternative under explicitly stated comparison conditions and matched resource assumptions. This is not caution. It is the only way to know whether quantum methods help.

*Questions over answers.* The Lab is organized around questions, not around technologies or techniques. A good question outlasts any single approach to answering it.

*Breadth through depth.* The Lab's scope is deliberately broad — classical and quantum, NLP and physical AI, present and long-horizon. But breadth without depth is superficiality. Each project is pursued with the depth required for publication-quality results.

## Why open by default

Code, data, methodology decisions, negative results — all public. The Lab's credibility comes from the quality of the work, not from proprietary advantage. Openness is also a strategy: it is how the Lab can attract collaborators, build trust, and make its work useful beyond one person's notebook. The first round of preprints is targeted for 2026, starting with the Pillar II hybrid-Transformer work, followed by the Pillar I romanization paper, followed by the Pillar III position paper after the Pillar II preprint has been reviewed.

## The long view

QMI Lab exists because the most interesting questions about intelligence cannot be answered by any single field, any single architecture, or any single computational paradigm. The questions I want QMI Lab to hold together are these: how information becomes knowledge, where classical computation is sufficient, where quantum computation may become necessary, and what it means to model dynamics rather than only predict next tokens.

The Lab is one person right now. It might stay small. It might grow. Its value is not measured in headcount or funding, but in the quality of the questions it asks and the rigor of the answers it produces.

If you are working on any part of this and want to talk — academic collaboration, co-authorship, visiting affiliate arrangements — the contact channels are at the bottom of [qmilab.com](https://qmilab.com), and I read everything that comes in. The Lab is designed for collaboration from the start. Nothing about a one-person research operation is the right shape for the questions worth asking.

> *Nature isn't classical, dammit, and if you want to make a simulation of nature, you'd better make it quantum mechanical, and by golly it's a wonderful problem, because it doesn't look so easy.*
>
> — Richard Feynman, 1981

It doesn't look so easy. That is exactly why it is worth doing.

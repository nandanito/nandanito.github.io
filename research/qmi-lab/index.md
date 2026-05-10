---
layout: page
title: QMI Lab
excerpt: "Quantum & Machine Intelligence Laboratory — independent research on intelligence, learning, and representation across classical and quantum computation."
modified: 2026-05-10
---

<p class="status status--in-prep">In preparation. Pillar I publishes first (Q3 2026); Pillars II and III publish across 2026–2027. Phasing is deliberate — see operating principles below.</p>

QMI Lab — Quantum & Machine Intelligence Laboratory — is an independent research lab studying intelligence, learning, and representation across classical and quantum computation. Single-researcher operation as of 2025–2026, organized around three research pillars and a small set of explicit operating principles. Web presence: [qmilab.com](https://qmilab.com).

## Why it exists

There is a methodological vacuum where machine intelligence research and quantum computing overlap. Quantum machine learning has accumulated a literature with weak classical baselines, undisclosed shot budgets, and overclaimed advantages — well-documented now in recent QML methodology reviews. Classical world-models research has its own evaluation crisis: most metrics measure prediction accuracy or reconstruction loss, not whether a model has learned transferable, physically meaningful structure. And the broader question — what are the right scientific questions at the quantum-AI frontier — is largely undertheorized.

QMI Lab's stance is that these gaps don't get fixed by faster compute or larger models. They get fixed by better questions, stronger baselines, honest reporting, and patient agenda-setting work.

## Operating principles

- **Intellectual honesty above all** — including reporting negative results.
- **Rigor earns the right to speculate.** Pillar III work is grounded in Pillars I and II, not the other way around.
- **Classical foundations before quantum aspirations.**
- **Questions over answers** — agenda-setting work matters as much as benchmark wins.
- **Breadth through depth** — one researcher can credibly span quantum, classical ML, and world models only by going deep on each, not by skimming.

## Pillar I — Foundations of Machine Intelligence

*Classical, publish-now. Strong methodological work that doesn't depend on quantum hardware. The skeptic's pillar — if you can't beat strong classical baselines, you can't make claims about quantum advantage.*

**Active project — Cross-Lingual Transfer Through Romanization.** *In preparation; arXiv preprint Q3 2026, EMNLP 2026 workshop submission planned.*

Five typologically diverse languages — Japanese (logographic + syllabary, hardest case), Hindi (best case but model-prior confound), Vietnamese (Latin-script control), Mandarin (tonal + logographic), Korean (alphabetic non-Latin). Each tested across three training conditions (native script, romanized, mixed) using QLoRA fine-tuning on Llama 3.1 8B. Signature contribution: ambiguity probes — targeted evaluations of homophone collisions introduced by romanization. Three-factor design: language typology × tokenizer prior × base-model prior.

**Planned project — World Model Evaluation Methodology.** *Planned; arXiv preprint Q1 2027, EACL/EMNLP 2027 venue submission planned.*

Evaluation frameworks that test for structured competence: counterfactual robustness, compositional generalization, causal abstraction, domain transfer. The framework should apply whether the world model is a classical RSSM or a quantum-enhanced encoder — natural connector between Pillars I and III.

## Pillar II — Quantum Machine Intelligence

*Near-term, benchmark-driven. Hybrid quantum-classical systems on NISQ hardware, with explicit resource accounting and matched comparisons across all three cost axes (classical parameters, quantum shots, total training cost).*

**Active project — Hybrid Quantum-Classical Transformer Fine-Tuning for NLP.** *In progress; arXiv preprint mid-2026, EMNLP or NeurIPS workshop submission late 2026.*

Compares parameterized quantum circuit (PQC) classification heads to classical baselines (linear, MLP, MPS tensor networks) on three NLP tasks: SST-2 (sentiment), XNLI (cross-lingual inference), and a multilingual classification setup. PQC heads attach to frozen pretrained language models. Multiple data encoding strategies tested as inductive biases: angle, amplitude, IQP. Three-axis resource contract reported per experiment. Pre-registered hypotheses about when and why PQC heads might offer parameter efficiency given matched resources. Honest reporting of negative results is a stated commitment — if classical heads win on every task, the paper says so and asks why anyone expected otherwise.

**Current state:** experimental harness in development; baseline classical heads benchmarked; encoding-strategy ablations being designed.

## Pillar III — Quantum World Models

*Long-horizon, agenda-setting. Position-paper-and-evaluation-framework work mapping where quantum representation might genuinely matter for world models, without claiming premature experimental results.*

**Planned project — Toward Quantum World Models: A Research Agenda.** *Planned; arXiv preprint Q4 2026, NeurIPS 2026 or ICLR 2027 workshop submission.*

Position paper. Provides a taxonomy of domains where quantum world models might offer genuine advantages over classical approaches (molecular dynamics, many-body systems, quantum materials), proposes evaluation frameworks for quantum-state world models, and offers concrete benchmark proposals for physically grounded domains.

**Current state:** background reading on classical world models complete. Pillar II hybrid quantum work continues building the empirical grounding the position paper relies on. Drafting begins once the Pillar II preprint is in workshop review.

## Outputs

- `qmilab/romanization` — Pillar I active project repo (in preparation)
- `qmilab/world-models` — Pillar I planned project repo
- `qmilab/quantum-nlp-hybrid` — Pillar II active project repo (in progress)
- `qmilab/quantum-world-models` — Pillar III planned project repo
- arXiv preprints: Q3 2026 (romanization), mid-2026 (hybrid quantum NLP), Q4 2026 (quantum world models position paper), Q1 2027 (world model evaluation methodology)

All research artifacts host on [QubitHub](/research/qubithub/) by deliberate commitment.

## Related work

Pillar-anchored references:

- **Bowles, Ahmed, Schuld** (2024) — *[Better than classical? The subtle art of benchmarking quantum machine learning models](https://arxiv.org/abs/2403.07059)*. The methodology critique Pillar II is built to answer.
- **Schuld, Sweke, Meyer** (2021) — *[Effect of data encoding on the expressive power of variational quantum-machine-learning models](https://arxiv.org/abs/2008.08605)*. Foundational work on encoding-as-inductive-bias.
- **DreamerV3** — Hafner et al., 2024, [arXiv:2301.04104](https://arxiv.org/abs/2301.04104). Reference for generative world model architecture.
- **V-JEPA / V-JEPA 2** — Bardes et al., Meta AI, 2024. Non-generative world model paradigm.
- **PennyLane** — Bergholm et al., 2022, [arXiv:1811.04968](https://arxiv.org/abs/1811.04968). Hybrid framework underlying the Pillar II experiments.
- **QLoRA** — Dettmers et al., 2023, [arXiv:2305.14314](https://arxiv.org/abs/2305.14314).
- **Llama 3.1** — Meta AI, 2024. Base model for Pillar I romanization fine-tuning.
- **World Models** — Ha & Schmidhuber, 2018, [arXiv:1803.10122](https://arxiv.org/abs/1803.10122). Foundational reference; RSSM lineage starts here.
- **Quantum simulation surveys** — Daley et al., 2022 (*Nature*); Georgescu et al., 2014 (*Reviews of Modern Physics*).
- **IQP and re-uploading encodings** — Havlíček et al., 2019, [arXiv:1804.11326](https://arxiv.org/abs/1804.11326); Pérez-Salinas et al., 2020.

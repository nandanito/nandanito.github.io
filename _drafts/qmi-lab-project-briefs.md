# QMI Lab — Project Brief for nandan.me

*Raw research material for site copy. Voice not finalized — substance and structure only.*

**Pillar count answer:** the lab is organized into **three pillars**, with **four research projects** distributed across them. Earlier home-page copy that referenced "four pillar sub-pages" conflated pillars with active projects — likely because the *World Model Evaluation Methodology* project bridges Pillars I and III. The brief below treats pillars as three, and notes the bridging project explicitly inside Pillar I.

---

## Section 1 — QMI Lab overview

### What the lab is

QMI Lab — Quantum & Machine Intelligence Laboratory — is an independent research lab studying intelligence, learning, and representation across classical and quantum computation. Single-researcher operation as of 2025–2026, organized around three research pillars and a small set of explicit operating principles. Web presence: qmilab.com.

### Why it exists

There is a methodological vacuum where machine intelligence research and quantum computing overlap. Quantum machine learning has accumulated a literature with weak classical baselines, undisclosed shot budgets, and overclaimed advantages — well-documented now in recent QML methodology reviews. Classical world models research has its own evaluation crisis: most metrics measure prediction accuracy or reconstruction loss, not whether a model has learned transferable, physically meaningful structure. And the broader question — what are the right scientific questions at the quantum-AI frontier — is largely undertheorized. QMI Lab's stance is that these gaps don't get fixed by faster compute or larger models. They get fixed by better questions, stronger baselines, honest reporting, and patient agenda-setting work.

### Who it's for

Graduate students and early-career researchers entering the quantum machine learning, world models, or scientific foundation model space. Teams considering whether quantum machine learning is worth investing in and looking for benchmark-driven prior art. Reviewers and program committees looking for methodologically careful work to cite. Hiring teams at scientific AI and quantum-AI labs evaluating researcher signal beyond CV proxies.

### The pillars at a glance

- **Pillar I — Foundations of Machine Intelligence.** Classical, publish-now. Strong methodological work that doesn't depend on quantum hardware. The skeptic's pillar — if you can't beat strong classical baselines, you can't make claims about quantum advantage.
- **Pillar II — Quantum Machine Intelligence.** Near-term, benchmark-driven. Hybrid quantum-classical systems on NISQ hardware, with explicit resource accounting and matched comparisons across all three cost axes (classical parameters, quantum shots, total training cost).
- **Pillar III — Quantum World Models.** Long-horizon, agenda-setting. Position-paper-and-evaluation-framework work mapping where quantum representation might genuinely matter for world models, without claiming premature experimental results.

### Operating principles

- **Intellectual honesty above all** — including reporting negative results.
- **Rigor earns the right to speculate.** Pillar III work is grounded in Pillars I and II, not the other way around.
- **Classical foundations before quantum aspirations.**
- **Questions over answers** — agenda-setting work matters as much as benchmark wins.
- **Breadth through depth** — one researcher can credibly span quantum, classical ML, and world models only by going deep on each, not by skimming.

### Position relative to AstroLLM

QMI Lab is the research lab; AstroLLM is the engineering project. The two share methodological commitments — staged design, explicit decision gates, adversarial review, honest evaluation — and a broader interest in scientific foundation models. They are linked from each other and from nandan.me, but the lab is the framing under which the research projects sit.

---

## Section 2 — Pillar I: Foundations of Machine Intelligence

### TL;DR

Classical ML research that doesn't wait on quantum hardware. Two projects: *Cross-Lingual Transfer Through Romanization* (in preparation, Q3 2026) and *World Model Evaluation Methodology* (planned, Q1 2027). The pillar earns the right to make Pillar II's quantum claims by establishing strong classical baselines and clean experimental designs. The world model evaluation project bridges into Pillar III.

### Why this matters

Most quantum machine learning papers fail at the classical-baseline step. A reviewer reading "PQC head outperforms MLP head" should ask: what was the MLP? Was it tuned with the same effort? Were resources matched across all cost axes? Pillar I answers those questions before Pillar II asks them. The classical baseline work is the credibility infrastructure for everything else QMI Lab does.

Separately, world models research has a parallel problem. Proxy metrics like next-token loss and reconstruction error don't measure whether a model has learned transferable structure. A model can ace prediction loss while failing every test of compositional generalization, counterfactual robustness, or causal abstraction. World model evaluation is one of the field's most under-explored and highest-leverage methodological challenges, and it sits naturally with Pillar I's publish-now stance.

### Methodology

Pre-registered hypotheses where applicable. Staged experimental design with explicit decision gates and kill criteria. Three-factor designs that name confounders rather than ignoring them. Honest reporting of negative or null results. The romanization project is structured as a "boundary conditions" question — when does the approach work, when doesn't it, and what's the cost ledger? The evaluation methodology project is structured around testing for structured competence, not surface metrics.

### Active project — Cross-Lingual Transfer Through Romanization

*Status: in preparation; arXiv preprint Q3 2026 target; EMNLP 2026 workshop submission planned.*

Five typologically diverse languages — Japanese (logographic + syllabary, hardest case), Hindi (best case but model-prior confound), Vietnamese (Latin-script control), Mandarin (tonal + logographic), Korean (alphabetic non-Latin). Each tested across three training conditions (native script, romanized, mixed) using QLoRA fine-tuning on Llama 3.1 8B. The signature contribution: ambiguity probes — targeted evaluations of homophone collisions introduced by romanization. Three-factor design: language typology × tokenizer prior × base-model prior. Explicit decision gates and kill criteria.

### Planned project — World Model Evaluation Methodology

*Status: planned; arXiv preprint Q1 2027 target; full venue submission (EACL/EMNLP 2027) planned.*

Develops evaluation frameworks that test for structured competence: counterfactual robustness, compositional generalization, causal abstraction, domain transfer. Bridging — the same framework should apply whether the world model is a classical RSSM or a quantum-enhanced encoder. Natural connector between Pillars I and III.

### Outputs

- `qmilab/romanization` repo. *In preparation.*
- `qmilab/world-models` repo. *Planned.*
- arXiv preprint, romanization. *Q3 2026.*
- arXiv preprint, world model evaluation. *Q1 2027.*
- EMNLP 2026 workshop submission, romanization. *Planned.*
- EACL or EMNLP 2027 venue submission, world model evaluation. *Planned.*

### Related work

- **Llama 3.1** — Meta AI, 2024. Base model for romanization fine-tuning experiments.
- **QLoRA** — Dettmers et al., 2023, [arXiv:2305.14314](https://arxiv.org/abs/2305.14314).
- **Tokenizer fairness and inequality** — Petrov et al., 2023; Rust et al., 2021. Core motivation for the romanization-as-cross-lingual-transfer question.
- **Romanization for low-resource NLP** — recent transliteration-based transfer literature.
- **DreamerV3** — Hafner et al., 2024, [arXiv:2301.04104](https://arxiv.org/abs/2301.04104). Reference architecture for the world model evaluation work.
- **V-JEPA / V-JEPA 2** — Bardes et al., Meta AI, 2024. Non-generative world model paradigm; central to the evaluation taxonomy.

---

## Section 3 — Pillar II: Quantum Machine Intelligence

### TL;DR

Near-term hybrid quantum-classical systems studied with strict comparative methodology. Active project: parameterized quantum circuit (PQC) classification heads for Transformer fine-tuning, benchmarked against classical heads (linear, MLP, MPS tensor networks) under matched resource budgets across three NLP tasks. Built with PennyLane, HuggingFace Transformers, PyTorch.

### Why this matters

The quantum machine learning literature has a credibility problem. Recent QML methodology reviews — Bowles et al., Schuld and Killoran, and others — have documented systematic failures: weak classical baselines, undisclosed shot budgets, missing resource accounting, and overclaimed quantum advantages on synthetic tasks. The field doesn't need more "quantum X works on toy problem Y." It needs honest comparisons under matched resources, explicit treatment of all three cost axes (classical parameters, quantum shots, total training cost), and pre-registered hypotheses about when and why a quantum component might help.

This is also where the data encoding question lives. Multiple QML papers have shown that data encoding acts as inductive bias — angle, amplitude, IQP encodings are not equivalent and the choice changes what the model can express. Pillar II treats encoding strategy as a first-class experimental variable, not a hyperparameter footnote.

### Methodology

PQC heads attach to frozen pretrained language models. The classical comparison set includes linear, MLP, and Matrix Product State (MPS) tensor-network heads — the last is critical, because tensor networks are the strongest classical baseline that captures the kind of structure quantum systems trade in. Multiple data encoding strategies tested as inductive biases: angle, amplitude, IQP. Tasks: SST-2 (sentiment), XNLI (cross-lingual inference), and a multilingual classification setup. Three-axis resource contract reported per experiment. Pre-registered hypotheses about when and why PQC heads might offer parameter efficiency given matched resources. Honest reporting of negative results is a stated commitment — if classical heads win on every task, the paper says so and asks why anyone expected otherwise.

### Active project — Hybrid Quantum-Classical Transformer Fine-Tuning for NLP

*Status: in progress; arXiv preprint mid-2026 target; EMNLP or NeurIPS workshop submission late 2026.*

Compares four head architectures across three NLP tasks. Three-axis resource accounting. Multiple encoding strategies tested. Designed to meet the methodological standards set by recent QDL reviews: strong classical baselines, explicit resource contracts, honest reporting of negative results.

**Current state:** experimental harness in development; baseline classical heads benchmarked; encoding-strategy ablations being designed.

### Outputs

- `qmilab/quantum-nlp-hybrid` repo. *In progress.*
- arXiv preprint. *Target mid-2026.*
- Workshop paper submission to EMNLP or NeurIPS workshop. *Target late 2026.*
- Pre-registration document alongside arXiv. *Planned.*

### Related work

- **"Better than classical? The subtle art of benchmarking quantum machine learning models"** — Bowles, Ahmed, Schuld, 2024, [arXiv:2403.07059](https://arxiv.org/abs/2403.07059). The methodology critique Pillar II is built to answer.
- **"Effect of data encoding on the expressive power of variational quantum-machine-learning models"** — Schuld, Sweke, Meyer, 2021, [arXiv:2008.08605](https://arxiv.org/abs/2008.08605). Foundational work on encoding-as-inductive-bias.
- **Tensor networks for NLP / DisCoCat** — Coecke et al., and the broader categorical-quantum NLP program. MPS baselines come from this lineage.
- **IQP and re-uploading encodings** — Havlíček et al., 2019, [arXiv:1804.11326](https://arxiv.org/abs/1804.11326); Pérez-Salinas et al., 2020.
- **PennyLane** — Bergholm et al., 2022, [arXiv:1811.04968](https://arxiv.org/abs/1811.04968). Hybrid framework underlying the experiments.
- **Quantum-classical hybrid Transformer literature** — Cherrat et al., 2024 and follow-up work on quantum-augmented attention and classification heads.

---

## Section 4 — Pillar III: Quantum World Models

### TL;DR

Long-horizon, agenda-setting work mapping where quantum representation might offer genuine advantages for world models. The deliverable is a position paper, not benchmark wins. The point is to identify the right questions before the field commits to the wrong ones. Builds on the Pillar I world model evaluation methodology and the Pillar II hybrid quantum work.

### Why this matters

World models research and quantum machine learning have grown up next to each other without much intersection. Classical world models — DreamerV3, V-JEPA, RSSM, Genie — have transformed model-based reinforcement learning and embodied AI. Quantum simulation has transformed how the physics community studies many-body systems. The question of where the two should meet — what classical world models miss that quantum-state representations might capture — is barely articulated, let alone studied empirically.

Premature benchmarking would do more harm than good here. Unlike Pillar II, where the methodology question is "how do we honestly compare?", in Pillar III the prior question is "what would even count as a meaningful comparison?" A research agenda paper that maps the territory — taxonomies of plausible domains, evaluation framework proposals, concrete benchmark seeds for physically grounded problems — is the high-leverage move. The honest delineation of what's currently speculative versus what's empirically grounded is itself the contribution.

### Methodology

Research synthesis bridging two literatures (classical world models and quantum simulation/QML). Concrete benchmark proposals where the physical domain admits them — molecular dynamics, many-body systems, quantum materials. No premature experimental results — this is agenda-setting, and pretending otherwise would be dishonest. Builds on completed study of both classical world models (DreamerV3, V-JEPA, RSSM, Genie architectures) and quantum machine learning (carrying through from the Pillar II project). Pillar I's world model evaluation methodology project is the natural empirical companion.

### Planned project — Toward Quantum World Models: A Research Agenda

*Status: planned; arXiv preprint Q4 2026 target; NeurIPS 2026 or ICLR 2027 workshop submission.*

Position paper. Provides a taxonomy of domains where quantum world models might offer genuine advantages over classical approaches (molecular dynamics, many-body systems, quantum materials), proposes evaluation frameworks for quantum-state world models, and offers concrete benchmark proposals for physically grounded domains.

**Current state:** planned. Background reading on classical world models complete. Pillar II hybrid quantum work continues building the empirical grounding the position paper relies on. Drafting begins once the Pillar II preprint is in workshop review.

### Outputs

- `qmilab/quantum-world-models` repo. *Planned.*
- arXiv preprint. *Target Q4 2026.*
- Workshop submission to NeurIPS 2026 or ICLR 2027. *Planned.*

### Related work

- **DreamerV3** — Hafner et al., 2024, [arXiv:2301.04104](https://arxiv.org/abs/2301.04104). Reference for generative world model architecture.
- **V-JEPA / V-JEPA 2** — Bardes et al., Meta AI, 2024. Non-generative world model paradigm.
- **World Models** — Ha & Schmidhuber, 2018, [arXiv:1803.10122](https://arxiv.org/abs/1803.10122). Foundational reference. RSSM lineage starts here.
- **Genie** — Bruce et al., DeepMind, 2024. Generative interactive environment work; widens the world model definition.
- **Quantum simulation surveys** — Daley et al., 2022 (*Nature*); Georgescu et al., 2014 (*Reviews of Modern Physics*). Anchors the "what are quantum simulators good at" side of the synthesis.
- **Quantum reinforcement learning** — Saggio et al., 2021 and follow-ups. Adjacent literature; world model framing is distinct from RL but shares some technical vocabulary.

---

## Notes for site copy

- Three pillars. The four-projects-distributed-across-three-pillars structure is the right framing; let pillar pages list the projects rather than promoting projects to pillar status.
- Pillar I publishes first; Pillars II and III publish in 2026–2027. The phasing is deliberate, not accidental — say so on the lab page.
- The lab name is `QMI Lab` or `Quantum & Machine Intelligence Laboratory`. Avoid "QMIL" as an acronym; it reads badly.
- Cross-link with AstroLLM. Both are independent research projects under the same researcher; the lab framing makes the relationship legible.
- The publication anchor for credibility is Reiners et al. 2012, *AJ* 143, 93 (doctoral-research period output). Surface in any longer-form site copy that establishes research background.

---
layout: page
title: AstroLLM
excerpt: "Domain-specialized retrieval-grounded language model for astronomy and astrophysics."
modified: 2026-05-10
---

<p class="status status--active">Active development — pre-training phase. Public beta target Q3 2026.</p>

AstroLLM is an independent research and engineering project building a domain-specialized, retrieval-grounded, tool-integrated language model family for astronomy and astrophysics. Differentiated from existing astronomy LLMs not by training scale but by deep integration with the databases astronomers actually use — NASA ADS, SIMBAD, and the NASA Exoplanet Archive — and by an evaluation suite designed to test research workflow competence, not knowledge recall.

## Why this matters

The astronomy LLM landscape has a gap. Frontier general-purpose models hallucinate paper citations and conflate astronomical objects — a SIMBAD alias collision is enough to confuse them. Domain-specialized models like AstroSage 8B and 70B (AstroMLab) have demonstrated that targeted training can match or exceed frontier models on knowledge benchmarks, but they operate as isolated Q&A systems with no live connection to the databases astronomers query in daily research.

NASA ADS holds 15M+ publications. SIMBAD catalogs 20.5M astronomical objects with a deep alias graph. The NASA Exoplanet Archive tracks 5,700+ confirmed planets and tens of thousands of candidates. None of this is in any LLM's training data with the freshness or completeness research demands, and none of it is queried correctly by general-purpose retrieval. The opportunity is to build a system where the LLM is the interface, not the source — every factual claim traces back to a specific paper via ADS bibcode, every object reference resolves through SIMBAD's alias graph, every workflow uses Astropy and astroquery the way researchers do.

The harder problem is evaluation. Existing astronomy LLM benchmarks (AstroMLab-1, Astro-QA) measure recall of astronomy knowledge. They don't measure whether a model can find a relevant paper in ADS, route a query through the right tool, or abstain when retrieval comes back weak. That last point — calibrated abstention — is where most retrieval-augmented systems fail and where evaluation is hardest. Building the evaluation suite alongside the model is part of the project, not a downstream concern.

The audience is graduate students and early-career researchers, with audience-adaptive explanation depth. Not a frontier-lab demo; not a benchmark-chasing exercise. A useful tool for the people doing the work.

## Methodology

**Base models.** Qwen3-4B and Qwen3-8B, chosen for permissive licensing, strong baseline reasoning, and efficient long-context handling. Adaptation via QLoRA fine-tuning with HuggingFace PEFT and TRL, on a curated SFT dataset of 5,000–8,000 examples. Composition: literature Q&A (30%), object/property retrieval (25%), citation-grounded summarization (20%), pedagogy (15%), tool-call formatting (10%).

**Retrieval.** Three-stage pipeline. Stage 1: hybrid sparse–dense recall — BM25 over abstract bodies combined with dense embeddings from SPECTER2. Stage 2: cross-encoder reranking. Stage 3: astronomy-aware filtering using SIMBAD's alias graph for object disambiguation. Index sits in PostgreSQL with pgvector. Tool integration covers astroquery, Astropy, and the broader Virtual Observatory ecosystem.

**Evaluation.** Custom four-track suite. Track 1: grounding and citation accuracy — does every factual claim resolve to a real ADS bibcode, and does the cited paper actually support the claim? Track 2: tool routing correctness. Track 3: abstention under weak retrieval — when the index returns nothing useful, does the model say so, or hallucinate? Track 4: pedagogical quality and audience-adaptive explanation depth.

**Process.** The plan went through adversarial peer review by two independent AI systems before scope was committed. The v1 is a scope-narrowed Core-only build with explicit decision gates and kill criteria.

## Current state

- Base model selection complete (Qwen3-4B and 8B). *Shipped.*
- Data engineering pipeline for ADS bulk ingestion and LaTeX processing. *In progress.*
- Synthetic SFT data generation with provenance tracking and schema validation. *In progress.*
- Custom evaluation suite design committed; benchmark fixtures being built. *In progress.*
- Retrieval index design complete; pgvector implementation underway. *In progress.*
- astrollm.org public site (Astro framework). *Planned, Q3 2026.*
- Adversarial peer review of v1 plan. *Shipped.*

The four-tier model family (Nano 1–3B through Ultra 70B+), AION-1 multimodal bridging (spectra, images, light curves), continuous arXiv ingestion, and community API sit on the long-term roadmap and are explicitly out of scope for v1.

## Outputs

- **astrollm.org** — public beta site (planned, Q3 2026).
- **astrollm GitHub organization** — training pipeline, evaluation suite, retrieval infrastructure (in progress; public release Q3 2026).
- **astrollm HuggingFace organization** — fine-tuned model weights, SFT dataset, evaluation benchmarks (in progress; public release Q3 2026).
- **Workshop paper** — ML4Astro at ICML, or AAS meeting (planned, Q4 2026 / Q1 2027).
- **Building a retrieval-grounded astronomy copilot on a budget** — blog series on this site (in progress through 2026).

## Related work

- **AstroSage 8B and 70B** — AstroMLab (de Haan et al., 2024+). State-of-the-art on AstroMLab-1 knowledge benchmark. AstroLLM differentiates on retrieval grounding and tool integration — AstroSage operates as isolated Q&A; AstroLLM is built around live database access.
- **AstroLLaMA** — Nguyen et al., 2023, [arXiv:2309.06126](https://arxiv.org/abs/2309.06126). Early astronomy LLM fine-tune on arXiv abstracts; demonstrated feasibility of domain adaptation but limited to abstract-level training and Q&A surface.
- **AION-1 / Multimodal Universe / Polymathic AI** — broader scientific foundation model program (2024+). Future bridging target for AstroLLM's multimodal track; AstroLLM positions as the language interface to that ecosystem.
- **AstroMLab-1 / Astro-QA** — measure knowledge recall but not retrieval competence, tool routing, abstention, or pedagogy. AstroLLM's four-track evaluation suite is designed to address these gaps.
- **QLoRA** — Dettmers et al., 2023, [arXiv:2305.14314](https://arxiv.org/abs/2305.14314). Efficient fine-tuning method underlying the training pipeline.
- **SPECTER2** — Singh et al., 2022. Scientific document embedding model used in the retrieval pipeline's dense recall stage.

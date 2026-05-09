# AstroLLM — Project Brief for nandan.me

*Raw research material for site copy. Voice not finalized — substance and structure only.*

---

## TL;DR

AstroLLM is an independent research and engineering project building a domain-specialized, retrieval-grounded, tool-integrated language model family for astronomy and astrophysics. Differentiated from existing astronomy LLMs not by training scale but by deep integration with the databases and tools astronomers actually use — NASA ADS, SIMBAD, and the NASA Exoplanet Archive — and by an evaluation suite designed to test research workflow competence, not knowledge recall. QLoRA fine-tuning on Qwen3-4B and 8B base models. Open-source models, datasets, training pipeline, and benchmarks. Active — pre-training phase. Public beta target Q3 2026 at astrollm.org.

**Status:** active, pre-training phase. Sole creator and researcher.

---

## Why this matters

The astronomy LLM landscape has a gap. Frontier general-purpose models hallucinate paper citations and conflate astronomical objects — a SIMBAD alias collision is enough to confuse them. Domain-specialized models like AstroSage 8B and 70B (AstroMLab) have demonstrated that targeted training can match or exceed frontier models on knowledge benchmarks. But these models operate as isolated Q&A systems, with no live connection to the databases astronomers query in daily research.

NASA ADS holds 15M+ publications. SIMBAD catalogs 20.5M astronomical objects with a deep alias graph. The NASA Exoplanet Archive tracks 5,700+ confirmed planets and tens of thousands of candidates. None of this is in any LLM's training data with the freshness or completeness research demands, and none of it is queried correctly by general-purpose retrieval. The opportunity is to build a system where the LLM is the interface, not the source — every factual claim traces back to a specific paper via ADS bibcode, every object reference resolves through SIMBAD's alias graph, every workflow uses Astropy and astroquery the way researchers do.

The harder problem is evaluation. Existing astronomy LLM benchmarks (AstroMLab-1, Astro-QA) measure recall of astronomy knowledge. They don't measure whether a model can find a relevant paper in ADS, route a query through the right tool, or abstain when retrieval comes back weak. That last point — calibrated abstention — is where most retrieval-augmented systems fail and where evaluation is hardest. Building the evaluation suite alongside the model is part of the project, not a downstream concern.

The audience is graduate students and early-career researchers, with audience-adaptive explanation depth. Not a frontier-lab demo, not a benchmark-chasing exercise. A useful tool for the people doing the work.

---

## Methodology

**Base models.** Qwen3-4B and Qwen3-8B, chosen for permissive licensing, strong baseline reasoning, and efficient long-context handling. Adaptation via QLoRA fine-tuning with HuggingFace PEFT and TRL, on a curated SFT dataset of 5,000–8,000 examples. Composition: literature Q&A (30%), object/property retrieval (25%), citation-grounded summarization (20%), pedagogy (15%), tool-call formatting (10%).

**Retrieval.** Three-stage pipeline. Stage 1: hybrid sparse–dense recall — BM25 over abstract bodies combined with dense embeddings from SPECTER2, a scientific document embedding model. Stage 2: cross-encoder reranking for relevance refinement. Stage 3: astronomy-aware filtering using SIMBAD's alias graph for object disambiguation. Index sits in PostgreSQL with pgvector. Tool integration covers astroquery, Astropy, and the broader Virtual Observatory ecosystem.

**Evaluation.** Custom four-track suite. Track 1: grounding and citation accuracy — does every factual claim resolve to a real ADS bibcode, and does the cited paper actually support the claim? Track 2: tool routing correctness. Track 3: abstention under weak retrieval — when the index returns nothing useful, does the model say so, or hallucinate? Track 4: pedagogical quality and audience-adaptive explanation depth.

**Process.** The plan went through adversarial peer review by two independent AI systems before scope was committed. The v1 is a scope-narrowed Core-only build with explicit decision gates and kill criteria. The project runs as a dual-mandate: a usable product for astronomers and a learning vehicle. Both mandates have explicit success criteria; the product mandate dominates near-term decisions, the learning mandate dominates retrospectives and method choices.

---

## Current state

**Active — pre-training phase.**

- Base model selection complete (Qwen3-4B and 8B). *Shipped.*
- Data engineering pipeline for ADS bulk ingestion and LaTeX processing. *In progress.*
- Synthetic SFT data generation with provenance tracking and schema validation. *In progress.*
- Custom evaluation suite design committed; benchmark fixtures being built. *In progress.*
- Retrieval index design complete; pgvector implementation underway. *In progress.*
- Astrollm.org public site (Astro framework). *Planned, Q3 2026.*
- Adversarial peer review of v1 plan. *Shipped.*

The four-tier model family (Nano 1–3B through Ultra 70B+), AION-1 multimodal bridging (spectra, images, light curves), continuous arXiv ingestion, and community API sit on the long-term roadmap and are explicitly out of scope for v1.

---

## Outputs

- **astrollm.org** — public beta site. *Planned, Q3 2026.*
- **astrollm GitHub organization** — training pipeline, evaluation suite, retrieval infrastructure. *In progress; public release Q3 2026.*
- **astrollm HuggingFace organization** — fine-tuned model weights, SFT dataset, evaluation benchmarks. *In progress; public release Q3 2026.*
- **"Building a retrieval-grounded astronomy copilot on a budget"** — blog series on nandan.me. *In progress; ongoing through 2026.*
- **Workshop paper** — ML4Astro at ICML, or AAS meeting. *Planned, Q4 2026 / Q1 2027.*
- **Long-term roadmap items (post-v1):** Nano-through-Ultra model family, AION-1 multimodal bridging, continuous arXiv ingestion, community API. *Planned.*

---

## Related work

Three to six anchor references; not exhaustive.

- **AstroSage 8B and 70B** — AstroMLab (de Haan et al., 2024+). Domain-specialized astronomy LLMs trained on curated astronomy corpora. State-of-the-art on AstroMLab-1 knowledge benchmark. AstroLLM differentiates on retrieval grounding and tool integration — AstroSage operates as isolated Q&A, AstroLLM is built around live database access.
- **AstroLLaMA** — Nguyen et al., 2023, [arXiv:2309.06126](https://arxiv.org/abs/2309.06126). Early astronomy LLM fine-tune on arXiv abstracts. Demonstrated feasibility of domain adaptation but limited to abstract-level training and Q&A surface.
- **AION-1 / Multimodal Universe / Polymathic AI** — broader scientific foundation model program (2024+). Multimodal astronomy foundation model handling spectra, images, light curves. Future bridging target for AstroLLM's multimodal track; AstroLLM positions as the language interface to that ecosystem.
- **AstroMLab-1 / Astro-QA** — existing astronomy benchmarks (AstroMLab, 2024). Measure knowledge recall but not retrieval competence, tool routing, abstention, or pedagogy. AstroLLM's four-track evaluation suite is designed to address these recognized gaps.
- **QLoRA** — Dettmers et al., 2023, [arXiv:2305.14314](https://arxiv.org/abs/2305.14314). Efficient fine-tuning method underlying the training pipeline.
- **SPECTER2** — Singh et al., 2022. Scientific document embedding model used in the retrieval pipeline's dense recall stage.

---

## Notes for site copy

- The publication anchor for related domain credibility is Reiners et al. 2012, *AJ* 143, 93 (doctoral-research period output). Worth name-checking in any longer site copy that establishes astronomy domain background.
- AstroLLM and QMI Lab are the two named independent research projects; both are public-OK across all surfaces. Cross-link between project pages on the site.
- "Cited, evidence-grounded" is the differentiator. Lead with it.

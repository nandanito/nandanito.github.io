---
layout: page
title: QubitHub
excerpt: "The developer platform for quantum computing — multi-framework, reproducibility-first, Git-backed."
modified: 2026-05-10
---

<p class="status status--in-prep">In beta. Open access launches late May 2026 at <a href="https://qubithub.co">qubithub.co</a>.</p>

QubitHub is a developer platform for quantum computing — multi-framework, reproducibility-first, with Git-backed collaboration and sandboxed execution.

## Why this is needed

Quantum hardware investment hit $4.2B in 2025. The developer layer hasn't kept up:

- **Framework fragmentation.** A handful of incompatible SDKs — Qiskit, PennyLane, Cirq, Braket, pyQuil, tket. A circuit in one rarely runs in another without a rewrite.
- **Reproducibility crisis.** Reproducing a published quantum result takes weeks. Papers share equations, not executable code. Hardware calibration drifts daily.
- **No discovery.** No "npm for quantum." Circuits live in paper appendices, GitHub repos without metadata, and personal file servers.
- **No collaboration infrastructure.** Software has GitHub. ML has Hugging Face. Quantum has nothing — no fork, star, version, benchmark, or attribution mechanics built for circuits.

Hardware companies historically don't capture the developer layer. IBM didn't build GitHub. Google didn't build Hugging Face. The quantum hardware boom creates the demand; a dedicated developer-platform company captures the community.

## Who it is for

- **Quantum developers** — building, sharing, and executing circuits across frameworks and hardware backends without rewrites.
- **Researchers** — publishing reproducible quantum-computing artifacts with proper metadata and attribution.
- **Educators** — running interactive quantum experiments in the browser without installing SDKs.
- **Organizations** — onboarding teams onto quantum without vendor lock-in.

## What it offers

- **Multi-framework circuit library.** Curated circuits across Qiskit, PennyLane, and Cirq, with version control and discovery built in.
- **Git-backed.** Every circuit is a real Git repository. The Git ecosystem — CI/CD, code review, IDE integrations, AI coding assistants — works natively.
- **In-browser execution.** Run circuits without installing SDKs or configuring credentials; emulation and real-hardware backends on the roadmap.
- **Interactive visualizations.** Bloch sphere, state vector, measurement histograms, circuit diagrams.
- **Sandboxed runtime.** Fail-closed security model for running shared circuits safely.
- **CLI and Python SDK.** First-class developer experience from terminal or notebook.
- **`qubithub.toml` manifest standard** — single source of truth for circuit metadata, dependencies, and execution. The Cargo.toml of quantum.

## QubitHub for Research

A research-platform extension is under active development for late 2026: reproducibility bundles, hybrid quantum-classical execution, datasets and benchmarks as first-class artifacts, FAIR-compliant metadata, and hybrid PyTorch + PennyLane pipelines. The capability fills a gap the quantum-research community has needed for years — Hugging Face is general-ML, Papers with Code is paper↔code mapping, Zenodo and OSF are archival.

## Roadmap

| Now | Next |
|---|---|
| Closed beta cohort onboarding | Open self-registration, late May 2026 |
| Multi-framework execution + visualization layer | First QPU integration (Q3 2026) |
| Git-backed circuit repository + manifest standard | *QubitHub for Research* (mid–late 2026) |
| CLI and Python SDK | GPU simulation + AI-agent interface (Q4 2026) |

## Bigger picture

QubitHub is the first product of **Quantputation** — the working thesis being that a complete world model, one that captures reality at the quantum level, requires quantum computers. Classical AI builds world models in words and pixels; quantum computes in the language nature actually speaks. The scientific foundation is [QMI Lab](/research/qmi-lab/), where peer-reviewed work validates the thesis and where research artifacts host on QubitHub by deliberate commitment.

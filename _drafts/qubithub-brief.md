# QubitHub — Brief

*The Developer Platform for Quantum Computing.*

**v1.0 — May 2026** | **Stage:** Pre-Seed | **Status:** Live at [qubithub.co](https://qubithub.co), Stage 3 (open self-registration) launching week of May 24–30, 2026 | **Audience:** Investor / advisor / partner

---

## One-Line

QubitHub is the developer platform for quantum computing — multi-framework, reproducibility-first, with research-grade FAIR compliance and hybrid quantum-classical execution as a layered capability. Live at [qubithub.co](https://qubithub.co).

**Reference exits in the developer-platform-for-X pattern:** GitHub $7.5B (developer platform for code, acquired by Microsoft 2018), Hugging Face $4.5B (developer platform for ML, current valuation). Quantum is the next category; the layer is unoccupied.

## The Gap

[$4.2B](https://w.tracxn.com/report-releases/quantum-computing-report-2025) flowed into quantum startups in 2025. Yet:

- **Framework fragmentation.** Six incompatible SDKs (Qiskit, PennyLane, Cirq, Braket, pyQuil, tket). A circuit in one rarely runs in another without a rewrite.
- **Reproducibility crisis.** Reproducing a published quantum result takes weeks. Papers share equations, not executable code. Hardware calibration drifts daily.
- **No discovery.** No "npm for quantum." Circuits are scattered across paper appendices, GitHub repos with no metadata, and personal file servers.
- **No collaboration infrastructure.** Software has GitHub. ML has Hugging Face. Quantum has nothing — no fork, star, version, benchmark, or attribution mechanics built for circuits.

Hardware companies historically don't capture the developer layer. **IBM didn't build GitHub. Google didn't build Hugging Face.** The quantum hardware boom creates the demand. A dedicated developer-platform company captures the community.

## The Product (Live, Not a Deck)

Deployed at [qubithub.co](https://qubithub.co) on $12/month of infrastructure (Hetzner CPX32 + free-tier services). Built solo over three months using AI-assisted development (Claude Code).

**What ships today:**

- **Multi-framework circuit repository** — 50 curated circuits across Qiskit, PennyLane, and Cirq, all audited to production quality.
- **Git-backed.** Every circuit is a real Git repo (`git clone https://qubithub.co/{user}/{circuit}` works). The entire Git ecosystem — CI/CD, code review, IDE integrations, AI coding assistants — works natively.
- **Three-tier execution model** — simulation live (Qiskit Aer), emulation and hardware planned (cloud QPU partners + IBM Quantum Q3 2026).
- **Five interactive visualizations** — Bloch sphere (3D), state vector, measurement histogram, circuit diagram, density matrix.
- **Two-layer security sandbox** — AST denylist + Docker container, fail-closed; hardened across multiple review rounds.
- **Enterprise stack** — JWT auth, RBAC, organization workspaces, Stripe billing (FREE / PRO / ENTERPRISE), audit logging (30+ action types), API keys with scoped permissions.
- **CLI & Python SDK** — `qubithub-sdk` with 12 commands and 20+ API methods.
- **`qubithub.toml` manifest standard** — single source of truth, 3-tier progressive complexity. The Cargo.toml of quantum.
- **950+ tests** passing (663 backend + 290 SDK), production monitoring (PostHog EU, Sentry, BetterStack).
- **MVP technical skeleton complete** (13/13 phases). **Sprint 15 closed 2026-05-10**; **Sprint 16 active**; **Stage 3 launches week of May 24–30**.

This is not a prototype. It is a deployed product with enterprise features, capital-efficient by design.

## The Expansion: QubitHub for Research

Decided + scoped + ADR-ratified 2026-05-09. Engineering delivery sequenced over Sprints 18–23.

The same Git-backed repository, collaboration, and execution substrate that serves quantum developers is being extended additively to serve serious quantum-research workflows. The forcing function: a 2026-05-09 design-partner gap analysis with the founder's parallel research project (`quantum-nlp-hybrid`) found that QubitHub today can host ~30% of what a serious quantum-ML research project wants to publish. The remaining 70% — reproducibility bundles, hybrid execution, datasets and benchmarks as first-class artifacts, cross-circuit comparison, FAIR primitives, hybrid PyTorch + PennyLane pipelines — does not exist end-to-end on any platform. Hugging Face is general-ML. Papers with Code is paper↔code mapping. Zenodo and OSF are archival.

**Two anchoring decisions:**
1. **Design Partner Program** — founder-led research projects engage QubitHub as design partners; their phase milestones drive the engineering sequence.
2. **QubitHub-First Artifact Hosting** — all founder-led research artifacts host on QubitHub, never on Hugging Face. A missed gap is a slipped artifact, never an HF fallback. The platform pays the visible cost of any miss — the only mechanism that turns a roadmap into a delivery commitment on real research timelines.

**Why this matters commercially:** the research-platform capability extends TAM (researcher tier of the developer market) and adds a defensibility layer (FAIR-compliant artifact hosting + citation infrastructure + persistent identifiers create switching costs that no competitor is building). It is additive, not a pivot — circuits remain the core primitive; "GitHub for quantum" remains the structural parallel.

## Market

| Layer | Size | Basis |
|---|---|---|
| **TAM** — Quantum software market (2033) | $4.75B | [Coherent MI](https://www.coherentmi.com/industry-reports/quantum-computing-software-market) |
| **SAM** — Quantum developer tools + collaboration + research-artifact hosting | ~$1.15B | Bottom-up: 250K developers × $2K avg + 5K enterprise teams × $50K + hardware marketplace fees |
| **SOM Year 1** — 1,000 registered, 500 MAU | ~$70K rev / $178K exiting ARR | 50 PRO + 3 Enterprise (9 months from beta) |
| **CAGR** | 34.6% | [BCC Research](https://www.bccresearch.com/pressroom/ift/global-quantum-computing-market-to-grow-346) |

Q1 2025 saw $1.25B in quantum funding, a [128% YoY surge](https://news.crunchbase.com/ai/quantum-startup-venture-highmark-february-2025-quera-softbank/). Classiq raised [$200M+](https://siliconangle.com/2025/11/13/quantum-software-startup-classiq-raises-new-funding-amd-qualcomm/) from AMD, Qualcomm, and IonQ. The software layer is the fastest-growing segment.

## Business Model

| Tier | Price | Driver |
|---|---|---|
| **FREE** | $0 | Researchers, students; build community + content flywheel |
| **PRO** | $19–49 / mo | Power users, small teams; private circuits, unlimited runs |
| **ENTERPRISE** | $20–50K / yr | Organizations; SSO, audit logs, SLA, dedicated support |
| **Hardware Marketplace** | 10–20% take-rate | Revenue share on real QPU execution (post-Q3 2026) |

**ARR Path** (bottom-up):
- **Year 1** (9 months from Stage-3 launch): 50 PRO + 3 Enterprise → ≈ $70K rev, $178K exiting ARR
- **Year 2** (full year, hardware live): 300 PRO + 15 Enterprise + hardware → ≈ $700K ARR
- **Year 3** (marketplace at scale): 1K PRO + 40 Enterprise + marketplace → ≈ $2.3M ARR

Target gross margin 75%+. Free-to-paid conversion ~2%. PRO ARPU ~$420/yr; Enterprise ARPU ~$25K/yr. LTV/CAC (PRO) > 5×.

**Year-1 ARR is gated by enterprise wins.** 3 enterprise contracts in 9 months is ambitious; first enterprise inbound conversation is the leading indicator. In a no-enterprise scenario, Year 1 lands at PRO-only ≈ $16K rev / $42K exiting ARR — still credible for pre-seed validation, but with the inflection point pushed into Year 2.

## Competitive Moat (4 Layers)

1. **Platform & Execution** — Multi-framework Docker-sandboxed execution + `qubithub.toml` standard + content-addressable storage. 6–12 months to replicate.
2. **Community Network Effects** — More circuits → better discovery → more users → more circuits. Critical mass ~500–1K active users + 2–5K circuits. Compounding.
3. **Data & Content Moat** — Accumulated circuits + datasets + benchmarks + execution metadata + reproducibility bundles. Cannot be replicated, must be accumulated.
4. **AI Distribution Moat** — External MCP server makes QubitHub the quantum platform that AI agents (Claude, ChatGPT, Gemini) reach for when a developer asks to "run a quantum circuit." No competitor is building this for external use.

**Direct competitors** (none own the developer-platform + research-platform intersection):
- **Strangeworks** ($28M, enterprise orchestration) — no community, no researcher focus.
- **Classiq** ($200M+, circuit synthesis) — proprietary, $30–50K/seat wall, not multi-framework.
- **qBraid** (~$5M, cloud IDE) — broadest QPU access but no registry, no collaboration, no benchmarks, no datasets.
- **BlueQubit** ($10M, GPU simulator) — no community, company-authored benchmarks only.
- **IBM Quantum / AWS Braket** — Qiskit-only / cloud execution; neither owns collaboration or discovery.

Hugging Face adding quantum is the most-asked risk. Answer: HF's infrastructure is built for large binary model weights; quantum circuits need purpose-built sandboxed multi-framework runtimes, quantum-specific visualization, and hardware integration. It would be a new product, not a feature — same reason GitHub didn't build HF.

## Why Now

1. **Record capital inflow** ($4.2B in 2025) creates a wave of new quantum developers who need tools.
2. **Quantum utility proven** — Quantinuum $5B valuation, IBM 127+ qubits, McKinsey's "year of quantum."
3. **Developer-platform layer is unoccupied** — Strangeworks = enterprise; Classiq = synthesis; qBraid = cloud IDE. None are building open community + discovery + research-platform capability.
4. **Hardware companies don't capture developer layers** — historical pattern. The quantum hardware boom creates demand for a dedicated platform company.
5. **AI agents are the next distribution channel** — building the MCP interface now, before any quantum competitor, locks in the AI-agent-first quantum platform position.

## Founder

**Nandan** — physicist (Master in Physics, University of Göttingen — the birthplace of quantum mechanics, where Heisenberg, Born, and Jordan formulated matrix mechanics in 1925), turned senior software engineer with deep enterprise infrastructure experience including blockchain / web3, turned founder.

**Builder before expert.** Nandan shipped QubitHub solo in 3 months — backend (FastAPI, SQLAlchemy), frontend (TanStack Start, React, TypeScript), infrastructure (Docker, Caddy, Hetzner), and multi-framework quantum execution (Qiskit, PennyLane, Cirq) — *before* deeply re-engaging quantum computing as a practitioner. Then started a structured 26-week quantum learning path; every week of learning feeds back into platform improvements (circuit quality, README depth, framework accuracy, research-platform primitives).

This is the pattern behind some of the most successful developer infrastructure: Drew Houston (Dropbox), DHH (Rails), Patrick Collison (Stripe) all shipped before having domain mastery. The "builder before expert" arc demonstrates execution speed, self-awareness, growth trajectory, and product-market intuition that precedes domain expertise. The vulnerability is the strength: the product improves visibly each week *because* the founder is learning, and every gap discovered as a learner is a gap the platform fills for users.

**First hires (with funding):** quantum-computing engineer (hardware integration: IBM Quantum, IonQ, Rigetti), DevRel / community lead, backend engineer.

## Company Status (Cap Table, Entity, IP)

- **Founder equity:** 100%. Solo founder, no co-founders, no convertibles outstanding, no SAFEs, no prior investor commitments. ESOP pool reserved at first round.
- **Entity structure:** under review with counsel. Three options on the table — German UG / GmbH (proximity to EU quantum ecosystem and German tax credits), Singapore Pte. Ltd. (fastest, APAC gateway, lowest setup friction), Delaware C-Corp + EU subsidiary (US-VC-friendly, YC-compatible). Decision will be lead-investor-aligned.
- **IP ownership:** all QubitHub code is authored by the founder on personal time, on personal hardware, with documented separation from any prior or current employer IP. Written declaration available on request as part of the data room.
- **Solo-founder risk:** acknowledged. The MVP is deployed and functional, and the agentic-architecture multiplier (16+ AI personas, 13+ slash-command skills) extends solo execution capacity meaningfully — but team build-out is the highest-priority use of funds, and the first three hires are explicit in the ask below.
- **Founder residency:** Germany (Indian passport). Founding-related employment-permit interaction is being evaluated with immigration counsel before round close.

## Traction

| Done | Next |
|---|---|
| ✅ Full MVP deployed (13/13 phases) | **May 24–30, 2026:** Stage 3 launch (open self-registration) |
| ✅ 50 curated circuits, 5 visualizations, Git-backed repos | Q2 2026: Beta cohort onboarding (50–100 users from waitlist) |
| ✅ Enterprise stack (billing, RBAC, audit, API keys) | Sprints 18–23: *QubitHub for Research* program (research-platform capability) |
| ✅ Two-layer security sandbox, hardened multi-round | Q3 2026: First QPU integration (IBM Quantum or Scaleway QaaS) |
| ✅ CLI & Python SDK (12 commands, 290 SDK tests) | Q3 2026: First paying customer |
| ✅ `qubithub.toml` manifest standard, content-addressable storage | Q4 2026: MCP Server live; second design partner; cuQuantum GPU simulation |
| ✅ 950+ tests, production monitoring (PostHog/Sentry/BetterStack) | |
| ✅ Sprint 15 closed (2026-05-10) | |
| ✅ Design Partner Program ratified (2026-05-09) | |

Total infrastructure cost to date: **$12 / month**.

## The Ask

**Raising €500K–€800K pre-seed for 12–18 months runway.** Implied dilution: 10–18% at a €3M–€5M post-money valuation (within the persona-benchmarked pre-seed band for a deployed deep-tech MVP). Lead investor sought; follower commitments welcomed thereafter. Instrument: SAFE or convertible note acceptable; priced round preferred at the higher end of the band.

**Use of funds:**

| Allocation | % | What it pays for |
|---|---|---|
| Founding-team hires | 60% | Quantum-computing engineer (hardware integration), DevRel / community lead, backend engineer |
| Hardware-integration partnerships | 15% | IBM Quantum API credits, Scaleway QaaS / OVHCloud QPU credits, integration engineering |
| Infrastructure scaling + GTM | 15% | Move from $12/month VPS to production-grade; conference presence, content, design-partner cohort |
| Legal + ops + buffer | 10% | Entity setup, IP / data-room counsel, immigration, runway buffer |

**Round milestones (what funding unlocks):**
1. Founding team hired (3 full-time inside 6 months); solo-founder risk eliminated.
2. Customer discovery complete — 20+ structured researcher interviews; willingness-to-pay validated.
3. Beta cohort onboarded — 50–100 users from waitlist; activation / retention / NPS benchmarked.
4. First QPU integration shipped — IBM Quantum or Scaleway QaaS; hardware-marketplace revenue model unlocked.
5. *QubitHub for Research* program delivered — six thematic epics across mid- and late-2026; first design-partner artifacts published on QubitHub on partner-project timelines.
6. First paying customer (PRO and / or enterprise); revenue validation.

**Bigger picture.** QubitHub is the first product of **Quantputation**, whose founding conviction is that a complete world model — one that captures reality at the quantum level — requires quantum computers. Classical AI builds world models in words and pixels; quantum computes in the language nature actually speaks. The scientific foundation is **QMI Lab** (independent research laboratory) — peer-reviewed science validates the thesis, and all founder-led research artifacts host on QubitHub by deliberate commitment.

**What's at stake:** the quantum developer-platform layer will be captured in the next 18–24 months. QubitHub has a deployed product, a clear market gap, an additive research-platform capability that no competitor is building, and the execution speed to win it.

---

*Sources: [BCC Research](https://www.bccresearch.com/pressroom/ift/global-quantum-computing-market-to-grow-346), [Tracxn](https://w.tracxn.com/report-releases/quantum-computing-report-2025), [Crunchbase](https://news.crunchbase.com/ai/quantum-startup-venture-highmark-february-2025-quera-softbank/), [McKinsey](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-year-of-quantum-from-concept-to-reality-in-2025), [Coherent MI](https://www.coherentmi.com/industry-reports/quantum-computing-software-market), [SiliconANGLE](https://siliconangle.com/2025/11/13/quantum-software-startup-classiq-raises-new-funding-amd-qualcomm/).*

*Companion docs (publicly shareable): [QUBITHUB.md](QUBITHUB.md) (full product document), [QUANTPUTATION.md](../company/QUANTPUTATION.md) (parent company), [Founder profile](../founder/PROFILE.md). Long-form investor narrative + pitch story available on request as part of the data room.*

---
layout: page
title: "PQ Readiness"
excerpt: "What post-quantum readiness means for a zkSDK deployment, which threats actually apply, and what the compliance kit ships today."
permalink: /pq-readiness/
order: 1
toc: true
---
<!-- GENERATED FILE — DO NOT EDIT.
     Source: docs/pq-readiness/index.md in the pq-zksdk-compliance-kit repo.
     Regenerate with: bun run scripts/render-jekyll.ts --out <jekyll-site-root>
     Edits made here will be silently overwritten. -->

> **Interim mirror.** These pages document the PQ-zkSDK Compliance Kit and are staged
> here while the canonical home is prepared under `zksdk.com/docs/`. They are a
> contributor's working copy, not an official zkSDK publication. Where this mirror and
> the zkSDK documentation ever disagree, the zkSDK documentation is authoritative.

> Compliance posture today. Quantum-safe primitives tomorrow.

This section answers one question with evidence: **is our privacy infrastructure ready for the post-quantum transition?**

Readiness is not the same as being post-quantum. Readiness means you can say, with dated artifacts rather than assurances, which cryptography you depend on, which parts a cryptographically-relevant quantum computer (CRQC) would break, what the migration path is, and which risks have no fix in the current version. That is a thing you can demonstrate today, before any mandate forces the issue.

## Two threats, not one

The most common framing error in this space is treating everything as "harvest now, decrypt later." Keep these separate — they have different victims, different timelines, and different fixes.

| | **Confidentiality break (HNDL)** | **Soundness / forgery break** |
|---|---|---|
| What happens | Ciphertext captured today is decrypted once a CRQC exists | A CRQC forges proofs or signatures, or breaks the binding of long-lived on-chain authorization state |
| Applies to | Encryption primitives — note envelopes, backups, stealth announcements | ZK proofs and signatures |
| Data already exposed? | **Yes** — anything already published must be assumed harvested | No — but permanent on-chain state becomes forgeable once the assumption falls |
| Fixing it later helps? | Not for data already published | Yes, for state created after the fix |

Encryption work is HNDL-relevant. **ZK-proof work is not** — it is forgery- and soundness-relevant. Anything that blurs the two is describing the wrong risk.

## Why hybrid, not post-quantum

Every primitive this kit ships is **hybrid by default**: a classical component and a post-quantum component, where *both* must verify.

That is deliberate. Module-lattice schemes (ML-KEM, ML-DSA) are believed post-quantum-secure, but lattice cryptanalysis is still maturing. Pure-PQ trades a well-understood assumption for a younger one. Given a sound combiner — one that binds both shared secrets *and* the transcripts that produced them into the KDF — a hybrid is at least as strong as the stronger of its two components, and it survives either assumption family falling.

Pure-classical and pure-PQ are explicit opt-outs, each with its own descriptor. Neither is the default, and the descriptor's `mode` field always carries the precision.

> **Note — Naming**
>
> A package named `-pq` is post-quantum-**ready**: its default mode is hybrid. It is not pure post-quantum. NIST names are used throughout — ML-KEM-768, not Kyber768; ML-DSA-44, not Dilithium2 — always with the parameter set stated.

## What ships today

| Package | What it does | Status |
|---|---|---|
| [`@zksdk/pq-audit`](/pq-readiness/audit-quickstart/) | Statically inventories a project's Shor/Grover exposure and maps it to regulatory frameworks. JSON, Markdown, PDF. | Available |
| [`@zksdk/security-descriptor`](/pq-readiness/security-descriptor/) | The machine-readable cryptographic provenance record every primitive must emit, plus the validator that enforces its honesty rules. | Available |
| Hybrid E2E encryption, hybrid ZK proofs, hybrid selective disclosure | Quantum-resistant variants of the live cryptographic surface | Planned — see the [migration timeline](/pq-readiness/migration-timeline/) |

The audit tool ships value with **zero post-quantum implementation**. You can inventory your exposure and produce audit-facing evidence today, without changing a line of cryptographic code.

Note that no kit primitive instantiates ML-KEM, ML-DSA or SLH-DSA yet — those land in Phases 2 and 4. Until then no descriptor claims FIPS conformance, and the [FIPS rows of the crosswalk](/pq-readiness/compliance-crosswalk/#nist-fips) are explicitly forward-looking.

## What this does not do

Read these as hard limits, not disclaimers:

- **It characterises compliance readiness; it does not certify compliance.** Throughout this section and every generated report, the kit *supports* or *provides evidence for* a control. It never satisfies, complies with, or certifies one. Those obligations bind regulated entities, not libraries.
- **FIPS conformance here is algorithm-level only.** Passing NIST test vectors in CI is not FIPS 140-3 / CMVP module validation and not a CAVP algorithm certificate. No package in this kit is a validated cryptographic module. An entity with a validated-module obligation cannot discharge it here.
- **No framework mandates post-quantum cryptography for DeFi today.** CNSA 2.0 has real deadlines, but they bind National Security Systems and their suppliers. Every other framework in the [crosswalk](/pq-readiness/compliance-crosswalk/) is algorithm-agnostic. This section is about readiness, never a claimed requirement.
- **Some exposure has no replacement in v1.** Transaction authorization (EIP-712 / ECDSA) is inherited from Ethereum's account model, and stealth-address recipient linkability has no post-quantum drop-in. Both are surfaced as [residual risks](/pq-readiness/threat-exposure/#residual-risks-no-v1-replacement) in every report — disclosed, never omitted.

## Where to go next

- **[Cryptographic exposure](/pq-readiness/threat-exposure/)** — which primitives Shor breaks, which Grover merely weakens, and the hybrid target for each.
- **[Audit quickstart](/pq-readiness/audit-quickstart/)** — run `bunx @zksdk/pq-audit ./your-project` and read the report.
- **[Security descriptor](/pq-readiness/security-descriptor/)** — the provenance record and the honesty rules the schema enforces.
- **[Compliance crosswalk](/pq-readiness/compliance-crosswalk/)** — CNSA 2.0, FIPS 203/204/205, DORA, NIS2, ISO/IEC 27001, SOC 2.
- **[Migration timeline](/pq-readiness/migration-timeline/)** — what exists now, what is planned, and what it will cost you in bytes.

---
layout: page
title: "Cryptographic exposure"
excerpt: "Which primitives in a zkSDK-style privacy stack are broken by Shor, which are only weakened by Grover, and the hybrid target for each."
order: 2
toc: true
---
<!-- GENERATED FILE — DO NOT EDIT.
     Source: docs/pq-readiness/threat-exposure.md in the pq-zksdk-compliance-kit repo.
     Regenerate with: bun run scripts/render-jekyll.ts --out <jekyll-site-root>
     Edits made here will be silently overwritten. -->

> **Interim mirror.** These pages document the PQ-zkSDK Compliance Kit and are staged
> here while the canonical home is prepared under `zksdk.com/docs/`. They are a
> contributor's working copy, not an official zkSDK publication. Where this mirror and
> the zkSDK documentation ever disagree, the zkSDK documentation is authoritative.

This page inventories the cryptographic primitive classes a zk-UTXO shielded-pool deployment typically depends on, and states — per primitive — what a cryptographically-relevant quantum computer (CRQC) does to it.

Two rules govern every claim here:

- **Broken is broken.** Shor does not weaken ECDLP, DLP, or pairings; it breaks them. Anything in that family is reported as `quantum_security_bits: 0`, never a small number.
- **Grover-reduced is not broken.** Hash-based constructions lose margin and survive with adequate parameters. Halving is the conservative planning bound and applies to *preimage* search; realistic collision-resistance loss is smaller, since the known quantum collision attacks need infeasible memory. Conflating "reduced" with "broken" overstates the damage and burns credibility.

## Exposure by primitive

| Primitive class | Assumption family | Shor-broken? | Grover-only | HNDL-relevant | Forgery-relevant |
|---|---|---|---|---|---|
| **Key-derivation root** — deterministic wallet ECDSA signature → hash → HKDF key tree | dlog (secp256k1) *at the root* | **Yes** | downstream HKDF | **Yes — critical** | **Yes** |
| **Note / memo encryption** — per-recipient secp256k1-ECDH envelope + HKDF wrap keys + AES-256-GCM | dlog + symmetric | **Yes** (ECDH wrap) | AES-GCM, HKDF | **Yes** | — |
| **Viewing-key tree** — HKDF sub-keys for user / pool / app / auditor scopes | hash, rooted in the key root | via root | Yes | **Yes** | — |
| **Note backup at rest** — AES-256-GCM under a non-extractable key | symmetric, rooted in the key root | via root | Yes | **Yes** | — |
| **Stealth addresses** — EIP-5564 / ERC-6538, secp256k1 ECDH + view tags | dlog (secp256k1) | **Yes** | — | **Yes** | **Yes** |
| **zk-UTXO proofs** — Groth16 over BN254 | pairing (BN254) | **Yes** | — | — | **Yes** |
| **Poseidon in-circuit** — commitments, nullifiers, Merkle paths | hash | — | Yes | — | Yes |
| **Sanctions / allowlist non-membership** — indexed Merkle tree, Poseidon | hash inside a Groth16 wrapper | wrapper broken | Yes | — | Yes |
| **Transaction authorization** — EIP-712 / ECDSA signing | dlog (secp256k1) | **Yes** | — | — | **Yes** |
| **Audit grants** — HMAC-SHA-256 wire format with embedded scoped key | hash / symmetric | — | Yes | grant blobs carry key material | minor |

> **Important — The key root dominates everything below it**
>
> Where a client key hierarchy is derived from a **single deterministic wallet signature** over a fixed message, that one signature is the whole tree's root of trust — and it is ECDSA, so Shor breaks it.
>
> A CRQC recovers the wallet key, re-signs the fixed derivation message, and re-derives every downstream key: viewing keys, backup keys, spending keys. Primitives that look hash-based in isolation (the viewing-key tree, note backups at rest) inherit full Shor exposure through that root. The audit tool surfaces this as a dependency cascade rather than letting those primitives report as merely Grover-reduced.
>
> The practical consequence: hybridizing note envelopes is not sufficient on its own. Post-quantum readiness has to reach key **derivation**, not just the encryption sitting on top of it.

### What is already harvestable

For HNDL, the question is not whether an attacker *will* capture the data — it is whether they already have.

| Data type | Where it lives | Harvestable today? |
|---|---|---|
| Memo envelopes (notes, disclosures) | on-chain, permanent and public | **Trivially** |
| Stealth announcements | on-chain, permanent | **Trivially** — a future view-key break makes every past announcement retroactively linkable |
| Encrypted note backups | application database | on database compromise or insider access |
| Proofs, commitments, nullifiers | on-chain | not confidentiality — forgery/soundness only |
| Transaction authorizations | on-chain / mempool | not confidentiality — forgery only |

Deprecating a code path does not un-publish its ciphertexts. Data written under a legacy scheme stays exposed regardless of what replaces the scheme.

## Hybrid targets

| Classical (live) | Hybrid target | PQ component | FIPS |
|---|---|---|---|
| Key-derivation root | classical wallet secret ⊕ ML-KEM-768-derived secret, both feeding HKDF | ML-KEM-768 | FIPS 203 |
| Per-recipient ECDH envelope wrap | ECDH(secp256k1) ⊕ ML-KEM-768 per-recipient wrap | ML-KEM-768 | FIPS 203 |
| Viewing-key authentication | Ed25519 ⊕ ML-DSA-44 | ML-DSA-44 / -65 | FIPS 204 |
| Groth16/BN254 proofs | Groth16 ⊕ hash-based STARK over the same statements | hash-based STARK | — (no FIPS standard covers STARKs) |
| Stealth addresses | **open problem** — no drop-in PQ scheme | — | — |
| EIP-712 / ECDSA authorization | **none in v1** — inherited from Ethereum's account model | — | — |

The key-derivation row carries a design constraint worth stating early: wallets cannot perform post-quantum operations natively today, so a hybrid key root needs a post-quantum key-custody story before it is deployable.

### ML-DSA parameter choice follows key lifecycle {#ml-dsa-parameter-choice}

Not a blanket default — the parameter set tracks how long a key lives and whether it can be rotated:

- **Rotatable, revocable, scope-bounded keys (viewing keys): ML-DSA-44** (NIST Category 2). Matches the ~128-bit classical target of the rest of the stack, and the 2,420-byte signature is already the UX pressure point at viewing-key frequency. Rotation bounds the exposure window; the Ed25519 half covers near-term risk.
- **Non-rotatable issuer / credential root keys: ML-DSA-65** (Category 3) recommended. The extra ~900 bytes is irrelevant at issuer-key frequency, and the higher category is cheap insurance on exactly the keys that *cannot* be rotated while lattice cryptanalysis matures.

A blanket ML-DSA-65 punishes the high-frequency path for no operational gain; a blanket ML-DSA-44 leaves the least-rotatable keys on the family floor. Each descriptor records which profile applies and why.

Note that neither choice buys CNSA 2.0 alignment — CNSA specifies ML-DSA-87. See the [crosswalk](/pq-readiness/compliance-crosswalk/#cnsa-20) for that gap.

## Residual risks (no v1 replacement) {#residual-risks-no-v1-replacement}

These are reported in every audit run. They are not oversights, and they are never silently omitted:

- **EIP-712 / ECDSA transaction authorization stays Shor-exposed.** Authorization is inherited from Ethereum's account model and is not replaceable at the SDK layer. Post-quantum account abstraction is upstream ecosystem work, out of kit scope.
- **Stealth addresses have no post-quantum successor.** Announcements harvested today become retroactively linkable once secp256k1 falls. There is no drop-in scheme to migrate to.
- **Already-harvested legacy data stays exposed.** Ciphertexts and content identifiers already written to a database or a public network remain harvestable after the path that produced them is deprecated.
- **Post-quantum cryptanalysis evolves.** This is the reason the kit is hybrid rather than pure-PQ — a hybrid survives its post-quantum half being weakened.
- **Post-quantum library hardening.** Side-channel and timing review of the underlying PQ implementation is a maturity concern; primitives carry an `experimental` status until third-party review lands.
- **On-chain soundness stays classical where only the classical proof is verified on-chain.** Declared as `onchain_soundness: classical_only`, never implied to be hybrid. Swapping a cryptographic assumption for a trusted-party attestation while still calling it hybrid would be worse than the honest claim.
- **Off-chain verification with a signed attestation is a trust assumption, not a cryptographic one.** Where a worker verifies a proof off-chain and signs the result, the security of that path rests on the operator, and the audit reports it in the same honesty class as `classical_only` soundness.

## How this maps to the audit tool

Everything above is encoded in the knowledge base that [`@zksdk/pq-audit`](/pq-readiness/audit-quickstart/) evaluates against. Findings are grouped into three categories, all of which appear in a report:

- **Primitives** — a quantum-exposed cryptographic primitive was detected.
- **Residual** — a known exposure with no v1 replacement, surfaced whether or not it was detected.
- **Operational** — a non-quantum finding that nonetheless invalidates the security story (a development-grade trusted setup, for example, makes proof soundness moot long before a CRQC is relevant).

Detection is static and heuristic — it reads manifests and matches known primitive signatures in source. **Absence of a finding is not proof of absence of exposure.**

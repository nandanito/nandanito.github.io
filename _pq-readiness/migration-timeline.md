---
layout: page
title: "Migration timeline"
excerpt: "What ships now, what is planned, what hybrid mode costs in bytes, and what an adopter can do today."
order: 6
toc: true
---
<!-- GENERATED FILE — DO NOT EDIT.
     Source: docs/pq-readiness/migration-timeline.md in the pq-zksdk-compliance-kit repo.
     Regenerate with: bun run scripts/render-jekyll.ts --out <jekyll-site-root>
     Edits made here will be silently overwritten. -->

> **Interim mirror.** These pages document the PQ-zkSDK Compliance Kit and are staged
> here while the canonical home is prepared under `zksdk.com/docs/`. They are a
> contributor's working copy, not an official zkSDK publication. Where this mirror and
> the zkSDK documentation ever disagree, the zkSDK documentation is authoritative.

This page is deliberately blunt about what exists. Nothing below is described as available unless it is.

> **Info — Cadence**
>
> The kit ships on its own cadence and is **not** pinned to a zkSDK release train. Phase durations are planning estimates, not commitments, and no calendar dates are given for unshipped work — a dated promise for cryptography that has not been reviewed is exactly the kind of claim this kit exists to prevent.

## Phases

| Phase | What it delivers | Status |
|---|---|---|
| **0** — Scoping | Threat model, primitive inventory, per-primitive Shor/Grover exposure | ✅ Complete |
| **1** — Compliance assessment surface | `@zksdk/pq-audit`, `@zksdk/security-descriptor`, descriptor + crosswalk schemas | ✅ Available |
| **2** — Hybrid E2E encryption | ECDH(secp256k1) ⊕ ML-KEM-768 and X25519 ⊕ ML-KEM-768 note encryption; FIPS 203 vectors in CI | Planned (~4 wk) |
| **3** — Hybrid ZK proofs | Groth16 ⊕ hash-based STARK over the same statements | Planned (~6 wk, benchmark spike first) |
| **4** — Hybrid selective disclosure | Ed25519 ⊕ ML-DSA-44/65 viewing keys and issuer signatures | Planned (~4 wk) |
| **5** — Reference deployment | End-to-end shielded-payment demo, PQ posture dashboard, audit-package PDF export | Planned (~3 wk) |

Phase 1 exists first on purpose: **it produces value without committing to any specific post-quantum implementation choice.** If the hard ZK work in Phase 3 runs long, adopters still have a credible inventory-and-evidence tool. It is also the artifact that lets an institution justify engaging with the stack in the first place.

## Available now

**Inventory your exposure.** [`@zksdk/pq-audit`](/pq-readiness/audit-quickstart/) produces JSON, Markdown, and an audit-support PDF suitable for a DORA / SOC 2 / ISO 27001 evidence package. No code changes, no post-quantum dependency.

**Emit provenance.** [`@zksdk/security-descriptor`](/pq-readiness/security-descriptor/) gives you the descriptor contract and a validator whose honesty rules make overclaiming structurally impossible. Third-party primitives become auditable the moment they emit a conformant descriptor.

**Both schemas.** [`security-descriptor.schema.json`](/schemas/security-descriptor.schema.json) and [`compliance-crosswalk.schema.json`](/schemas/compliance-crosswalk.schema.json) — draft 2020-12, consumable by any validator.

## Planned

### Phase 2 — Hybrid E2E encryption

The lowest-risk wedge: a clean KEM substitution with no ZK redesign. Two packages, `-pq` suffixed, hybrid by default.

The combiner is the security-critical part. The symmetric key derives from a KDF whose input binds both shared secrets **and the transcripts that produced them**:

```
HKDF(classical_secret ∥ pq_secret ∥ ct_classical ∥ pk_classical ∥ ct_pq ∥ label)
```

(`∥` is concatenation; `ct` a ciphertext, `pk` a public key, and `label` a domain-separation string that keeps this derivation distinct from any other use of the same inputs.)

Binding the ciphertexts and public keys — not just the bare secrets — is what gives the combined KEM its robustness. Bare-secret concatenation is not sufficient. This is necessary hygiene, not a proof: IND-CCA security of the combined KEM requires a written combiner analysis covering invalid-key handling, contributory behaviour, domain separation, downgrade resistance, KDF choice and the exact KEM transform. That analysis is a release gate.

The design is **modeled on the X-Wing hybrid KEM, not an instance of it** — X-Wing's security argument is specific to X25519 + ML-KEM-768, so the secp256k1 variant ships with its own written deviation analysis.

**Mode is deployment policy, not a per-message option.** Ciphertexts commit to their mode and suite identifier through the AEAD associated data and the domain-separation label; decryptors pin an expected mode at configuration time; there is no silent fallback. A classical-mode artifact presented to a hybrid-pinned decryptor is rejected outright.

### Phase 3 — Hybrid ZK proofs

The proving system is chosen **by benchmark, not by prior commitment**. A week-one spike compares candidate STARK paths on prove time, proof size, bundle size, gas cost and verifier complexity, with a security-semantics gate applied first: what statement is bound, and what is actually verified where.

"Both proofs must verify" is only a security claim if both proofs are provably about the *same* statement. The preferred approach is a single commitment whose membership path is verified in both systems; the fallback — dual trees with an application-enforced consistency invariant — becomes an explicit, descriptor-disclosed trust assumption.

**On-chain honesty comes first.** In the initial version the classical proof is verified on-chain and the STARK off-chain, so the descriptor says `onchain_soundness: classical_only` and reports say it plainly: off-chain verification gets full hybrid soundness today; on-chain settlement keeps classical soundness with a documented upgrade path. There are no attestation-of-off-chain-verification schemes — trading a cryptographic assumption for a trusted-party assumption while still calling it hybrid is worse than the honest claim.

### Phase 4 — Hybrid selective disclosure

Hybrid issuer and viewing-key signatures, where **both** signatures must verify. Anti-stripping is structural: the suite identifier, mode and both public keys are signed under both signatures, and verifiers pin the expected mode at key-registration time. Parameter choice follows [key lifecycle](/pq-readiness/threat-exposure/#ml-dsa-parameter-choice) — ML-DSA-44 for rotatable viewing keys, ML-DSA-65 for non-rotatable issuer roots.

## What hybrid costs

Post-quantum is not free, and the sizes are the honest reason migrations get deferred. Plan for them.

| Primitive | Size | Versus classical |
|---|---|---|
| ML-KEM-768 ciphertext | 1,088 B | +1,088 B per encapsulation |
| ML-KEM-768 encapsulation key | 1,184 B | vs. 32–65 B classical (decapsulation key 2,400 B) |
| ML-DSA-44 signature | 2,420 B | ~38× Ed25519 (64 B) |
| ML-DSA-44 public key | 1,312 B | vs. 32 B Ed25519 |
| SLH-DSA-SHA2-128f signature | 17,088 B | hash-only, and very large (same size in the SHAKE family); listed for comparison — no kit path uses it |
| Hash-based STARK proof | ~50–200 KB | 200–800× Groth16 (256 B) — placeholder pending the Phase 3 benchmark |

In hybrid mode you pay these **in addition to** the classical sizes, since both components ship. For a per-recipient note envelope that is roughly a kilobyte per recipient; for on-chain proof data it is the difference between a constant-size Groth16 proof and something that does not belong on L1 today. That last row is why Phase 3 leads with a benchmark instead of a commitment.

## What you can do today

Four steps, none of which require any planned phase to land:

1. **Run the audit** and keep the JSON. `bunx @zksdk/pq-audit ./your-project --format json --out audit.json`. The first report is your baseline; subsequent diffs are your migration evidence.
2. **Gate CI on descriptor validity.** `--fail-on` also fails the run when any emitted descriptor is invalid, at whichever severity you set. This is the cheapest control to add and it catches false safety claims before they reach a report.
3. **Classify your data by HNDL exposure.** Anything already published — on-chain envelopes, stealth announcements — must be assumed harvested. That is what determines migration urgency, not the primitive count. See [cryptographic exposure](/pq-readiness/threat-exposure/).
4. **Record the residual risks you are accepting.** Transaction authorization and stealth-address linkability have no v1 replacement. Documenting an accepted risk is a legitimate compliance posture; discovering it during an audit is not.

## What none of this changes

The frameworks in the [crosswalk](/pq-readiness/compliance-crosswalk/) impose **no post-quantum mandate** on DeFi or commercial entities today. CNSA 2.0's deadlines bind National Security Systems and their suppliers.

That is precisely the window. The institutions choosing privacy infrastructure now are the ones who will re-migrate mid-cycle unless what they choose is already post-quantum ready. Readiness is worth demonstrating before a mandate exists — not because one is coming on a known date, but because the data published today is the data decrypted later.

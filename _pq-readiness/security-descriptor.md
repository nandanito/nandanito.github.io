---
layout: page
title: "Security descriptor"
excerpt: "The machine-readable cryptographic provenance record every primitive emits, and the honesty rules its schema mechanically enforces."
order: 4
toc: true
---
<!-- GENERATED FILE — DO NOT EDIT.
     Source: docs/pq-readiness/security-descriptor.md in the pq-zksdk-compliance-kit repo.
     Regenerate with: bun run scripts/render-jekyll.ts --out <jekyll-site-root>
     Edits made here will be silently overwritten. -->

> **Interim mirror.** These pages document the PQ-zkSDK Compliance Kit and are staged
> here while the canonical home is prepared under `zksdk.com/docs/`. They are a
> contributor's working copy, not an official zkSDK publication. Where this mirror and
> the zkSDK documentation ever disagree, the zkSDK documentation is authoritative.

The security descriptor is the load-bearing artifact of the kit: a structured, machine-readable record of a primitive's cryptographic provenance — what it assumes, what it uses, and what it claims. The audit tool, compliance reports, and GRC integrations all read it.

**Every primitive exports `securityDescriptor()`. No descriptor, not shippable.**

The JSON Schema (draft 2020-12) is published at [`security-descriptor.schema.json`](/schemas/security-descriptor.schema.json).

## Why structured, not a boolean

A `quantum_safe: true / false` flag is actively dangerous. It hides the parameters that decide whether the claim is even true, and it invites the single worst failure mode in this space: **a primitive labelled post-quantum-safe that delivers less than it claims.** That is not a bug, it is a liability — it can hand a regulated institution a false compliance posture.

A descriptor forces every claim to be explicit and defensible, and it lets an auditor disagree with a *specific field* rather than with a vibe.

## Why two components, not one algorithm field

A hybrid primitive has two halves, and inventorying the **classical** (Shor-exposed) half is the entire job of an audit. So both halves are first-class machine-readable objects — `classical_component` and `pq_component` — never a single `kem` field with the other half buried in prose `notes`.

This matters more than it looks: the honesty rules below are enforced from the *components*, not from the `mode` label. A descriptor cannot call itself `hybrid` and then leave one side empty.

## Fields

Ten fields are required: `primitive`, `mode`, `assumption_family`, `classical_component`, `pq_component`, `classical_security_bits`, `quantum_security_bits`, `fips_conformance`, `status`, `last_reviewed`. Unknown properties are rejected.

| Field | Type | Meaning |
|---|---|---|
| `primitive` | string | package + primitive identifier |
| `mode` | enum | `hybrid` \| `classical` \| `pq-only` |
| `assumption_family` | enum | `pairing` \| `dlog` \| `hash` \| `lattice` \| `hybrid` \| `unknown` — the primitive as a whole |
| `classical_component` | object | `{ kem, signature, proof_system }` from `x25519` \| `ecdh_secp256k1` \| `ed25519` \| `ecdsa_secp256k1` \| `groth16` \| `plonk` \| `none` |
| `pq_component` | object | `{ kem, signature, proof_system }` from `ml_kem_512/768/1024` \| `ml_dsa_44/65/87` \| `slh_dsa_sha2_128s/128f` \| `slh_dsa_shake_128s/128f` \| `stark` \| `none` |
| `wrapper` | enum | `none` \| `groth16_bn254` \| `recursive_stark` \| `hybrid_classical_pq` |
| `fiat_shamir_hash` | string[] | e.g. `poseidon`, `keccak256`, `shake256` |
| `classical_security_bits` | integer | best classical attack cost — name the metric in `notes` |
| `quantum_security_bits` | integer | post-Grover for hash; `0` (broken) for ECDLP/pairing under Shor — name the metric in `notes` |
| `trusted_setup` | enum | `none` \| `universal_ptau` \| `per_circuit_phase2` \| `hybrid` |
| `onchain_verifier` | enum | `none` \| `ethereum_l1_groth16` \| `ethereum_l1_stark` \| `starknet` \| `l2_native` \| `offchain_only` |
| `onchain_soundness` | enum | `none` \| `classical_only` \| `hybrid_pq` — what the chain actually enforces |
| `fips_conformance` | string[] | `fips_203` \| `fips_204` \| `fips_205` \| `none` — algorithm-level test vectors only |
| `nist_security_category` | 1–5, optional | NIST category of the PQ parameter set — NIST assigns categories, not bit scalars |
| `cavp_validation` | string, optional | CAVP algorithm certificate ID or `none` — distinct from passing test vectors, and from CMVP |
| `cmvp_validation` | string, optional | FIPS 140-3 CMVP module certificate ID or `none` (no kit package has one) |
| `status` | enum | `production` \| `experimental` \| `research` \| `deprecated` |
| `last_reviewed` | date | when the claims were last checked against current cryptanalysis |
| `notes` | string | caveats, especially anything that downgrades confidence |

## Honesty rules

The schema carries **20 conditional rules** that make the dangerous claims structurally unrepresentable. These are not lint suggestions — a descriptor that violates one does not validate, and the audit tool reports an invalid descriptor as a finding in its own right.

**Broken is broken.**
- A Shor-broken assumption family (`pairing`, `dlog`) must declare `quantum_security_bits: 0`, in every mode.
- A *nonzero* quantum claim requires a genuine basis: a hash assumption family, or an active PQ component. The schema never *mandates* a nonzero claim — that would be a licence to lie.
- An active classical component with no PQ component is dlog/pairing cryptography and must say so, which in turn forces `quantum_security_bits: 0`.

**A hybrid must actually be hybrid.**
- `mode: hybrid` requires a real algorithm on **both** sides. A "hybrid" of one component is a mislabel.
- `mode: classical` carries no active PQ component; `mode: pq-only` carries no active classical component.

**On-chain soundness is what the chain enforces.**
- A Groth16 L1 verifier enforces classical soundness only — the descriptor must say `classical_only`.
- A `groth16_bn254` wrapper cannot claim `onchain_soundness: hybrid_pq`: the wrapped verification rests on BN254 pairing, which Shor breaks.
- `hybrid_pq` requires a PQ-sound proof **actually verified on-chain** — an active STARK proof system *and* an on-chain verifier that checks it. `offchain_only`, a Groth16 verifier, or `none` can never be `hybrid_pq`. A commitment to an off-chain result does not count.

**FIPS claims must be backed by the algorithm they name.**
- `fips_203` requires an ML-KEM in the PQ component; `fips_204` requires an ML-DSA; `fips_205` requires an SLH-DSA.
- `none` is exclusive — it cannot sit alongside a real conformance claim.

**Parameter sets cap what you may claim.** Seven rules bind each PQ parameter set to its NIST category and a conservative bit ceiling, so a real PQ primitive cannot be overclaimed:

| Parameter set | NIST category cap | `quantum_security_bits` cap |
|---|---|---|
| ML-KEM-512 | 1 | 128 |
| ML-KEM-768 | 3 | 192 |
| ML-KEM-1024 | 5 | 256 |
| ML-DSA-44 | 2 | 128 |
| ML-DSA-65 | 3 | 192 |
| ML-DSA-87 | 5 | 256 |
| SLH-DSA-128 (SHA2 or SHAKE, `s` or `f`) | 1 | 128 |

Beyond the schema, two conventions apply by policy:

- **Vector conformance is not module validation.** `fips_conformance` asserts *algorithm-level* conformance (NIST test vectors in CI). It does not assert FIPS 140-3 / CMVP module validation, and it is not a CAVP algorithm certificate. No package in this kit is a validated cryptographic module.
- **`last_reviewed` is load-bearing.** Lattice assumptions can shift. A stale review date is itself a signal, and every `*_security_bits` value should name its metric in `notes` — which component, which attack model, why the number is conservative.

## Example

A hybrid E2E encryption primitive:

```json
{
  "primitive": "@zksdk/e2e-encryption-secp256k1-pq",
  "mode": "hybrid",
  "assumption_family": "hybrid",
  "classical_component": { "kem": "ecdh_secp256k1", "signature": "none", "proof_system": "none" },
  "pq_component": { "kem": "ml_kem_768", "signature": "none", "proof_system": "none" },
  "wrapper": "hybrid_classical_pq",
  "fiat_shamir_hash": [],
  "classical_security_bits": 128,
  "quantum_security_bits": 128,
  "trusted_setup": "none",
  "onchain_verifier": "none",
  "fips_conformance": ["fips_203"],
  "status": "experimental",
  "last_reviewed": "2026-07-21",
  "notes": "Hybrid ECDH(secp256k1) ⊕ ML-KEM-768. KDF input binds both shared secrets plus ciphertexts, public keys, and a domain-separation label (X-Wing-style combiner; the secp256k1 deviation analysis is separate — X-Wing's proof is X25519-specific). classical_security_bits: floor across components (secp256k1 ≈ 128; ML-KEM-768 ≈ 192 classical). quantum_security_bits: deliberate conservative floor — ML-KEM-768 is NIST Category 3 (comparable to AES-192), but we claim only 128 while lattice cryptanalysis matures. fips_conformance is algorithm-level (FIPS 203 test vectors in CI), NOT FIPS 140-3/CMVP module validation. Experimental pending third-party side-channel review of the ML-KEM implementation."
}
```

Note what the `notes` field is doing: it names the metric behind each number, states why the quantum claim is *lower* than the parameter set would allow, and records exactly why the status is `experimental`. That is the intended use — the descriptor is where you write down what you cannot yet back.

## API

```ts
import {
  type SecurityDescriptor,
  type HasSecurityDescriptor,
  validate,                 // (x: unknown) => x is SecurityDescriptor
  validateDescriptor,       // (x: unknown) => { valid, errors: { path, rule, message }[] }
  assertValidDescriptor,    // throws a readable summary on failure
  securityDescriptorSchema, // the exact JSON Schema this package validates against
} from "@zksdk/security-descriptor";
```

Validation errors carry a stable `rule` id: `schema:<field>` for structural problems, `honesty:<name>` for the honesty rules — for example `honesty:shor-broken-zero-quantum`, `honesty:hybrid-both-active`, `honesty:param-set-bits-cap`. The audit tool surfaces these directly.

## How the guarantees hold

Two properties are worth trusting rather than assuming:

- **Type = schema.** The TypeScript types are *generated* from the JSON Schema. Hand-sync is impossible by construction: `bun run codegen:check` fails if the committed output drifts from the schema.
- **Validator = published schema, provably.** The validator is hand-rolled, zero-dependency and `eval`-free, so it survives compilation into the audit CLI's single binary. It is kept honest by a **differential test** that runs it and an `ajv` oracle — built against the literal published schema — over a fixture corpus, asserting they agree on every case. `ajv` is a development-only oracle and is never shipped.

The result: the shipped validator provably matches the published schema, without shipping a general-purpose schema engine or any `eval`.

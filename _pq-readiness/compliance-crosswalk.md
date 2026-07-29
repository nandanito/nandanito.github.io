---
layout: page
title: "Compliance crosswalk"
excerpt: "How the kit's artifacts map to CNSA 2.0, NIST FIPS 203/204/205, EU DORA, NIS2, ISO/IEC 27001 and SOC 2 — as readiness evidence, never as compliance."
order: 5
toc: true
---
<!-- GENERATED FILE — DO NOT EDIT.
     Source: docs/pq-readiness/compliance-crosswalk.md in the pq-zksdk-compliance-kit repo.
     Regenerate with: bun run scripts/render-jekyll.ts --out <jekyll-site-root>
     Edits made here will be silently overwritten. -->

> **Interim mirror.** These pages document the PQ-zkSDK Compliance Kit and are staged
> here while the canonical home is prepared under `zksdk.com/docs/`. They are a
> contributor's working copy, not an official zkSDK publication. Where this mirror and
> the zkSDK documentation ever disagree, the zkSDK documentation is authoritative.

Regulated adopters get asked about frameworks. This crosswalk states, control by control, exactly what the kit contributes and — more importantly — **what it does not**.

Every row is machine-readable and validates against [`compliance-crosswalk.schema.json`](/schemas/compliance-crosswalk.schema.json). There are no prose-only mappings: the schema is what makes the audit tool's mapping layer implementable, and it structurally prevents the two failure modes that make crosswalks worthless — scope inflation and empty-gap overclaiming.

## Ground rules

Four rules are applied to every row, and they are enforced rather than promised:

**Verb discipline.** Rows use *supports* and *provides evidence for*. The words *satisfies*, *complies*, and *certifies* appear only under negation. A negation-aware validator confirms no un-negated banned verb survives.

**Who is bound.** Every row names the entity the control binds — an NSS supplier, an EU financial entity, a certified organization, a service organization. Never the kit. A library cannot be bound by an obligation that runs to a regulated entity.

**Readiness, not requirement.** No row implies a post-quantum mandate. Where a PQ deadline genuinely exists (CNSA 2.0) it is scoped to National Security Systems only. Every other framework is explicitly marked as having no PQ mandate.

**Honest gap.** Every row names something the control needs that the kit does not produce — validated modules, organizational policy, key-management governance, data classification, auditor judgment, national-law scoping. **No row claims `gap: none`.** A mapping with no gap is a mapping that has stopped being honest.

## The single most important caveat

> Algorithm-level FIPS conformance (NIST test vectors in CI) is **not** FIPS 140-3 / CMVP module validation, and **not** a CAVP algorithm certificate. No package in this kit is a validated cryptographic module. **An entity with a validated-module obligation cannot discharge it with this kit.**

This is carried in every FIPS row's gap, in the CNSA 2.0 gap, and in every generated report.

## Rows

Each row records: framework, framework version, control id, applicability, requirement summary, what the kit provides, the evidence artifact, the gap, a readiness statement, and `last_reviewed`.

### CNSA 2.0 {#cnsa-20}

**Instrument:** CNSA 2.0 Cybersecurity Advisory (NSA, Sep 2022 Ver. 1.0) + CNSA 2.0 FAQ (U/OO/194427-22, PP-24-4014, December 2024 Ver. 2.1).

**Applicability:** National Security Systems and their vendors/suppliers only, per NSM-10. **Not** commercial, DeFi, or EU-regulated entities, which have no CNSA 2.0 deadline. An adopter outside the NSS supply chain is out of scope for this row entirely.

**Requirement:** ML-KEM-1024 for key establishment, ML-DSA-87 for signatures, AES-256, and SHA-384 or SHA-512.

Firmware and software signing uses the **stateful hash-based schemes LMS or XMSS** from NIST SP 800-208 — NSA's preferred parameter set is LMS with SHA-256/192, and HSS and XMSS^MT are not allowed.

> **Warning — SLH-DSA is not CNSA 2.0**
>
> It is easy to assume the third NIST PQC signature standard belongs here. It does not. FAQ v2.1 is explicit: *"While SLH-DSA is hash-based, it is not part of CNSA and is not approved for any use in NSS."* CNSA 2.0's hash-based signature path is LMS/XMSS under SP 800-208, not FIPS 205.

**Timeline** (FAQ v2.1, citing the updated CNSSP 15):

| By | What |
|---|---|
| 31 Dec 2025 | No transition enforced before this date |
| 1 Jan 2027 | All new NSS acquisitions must meet CNSA 2.0, unless otherwise noted |
| 31 Dec 2030 | Equipment and services that cannot support CNSA 2.0 must be phased out |
| 31 Dec 2031 | CNSA 2.0 algorithms are mandated for use; the vast majority of cryptography in an NSS should be quantum resistant |
| 2035 | All NSS quantum-resistant, per NSM-10 |

**Gap — and this one is load-bearing:** the kit's default parameter sets (ML-KEM-768 / ML-DSA-44) do **not** meet CNSA 2.0, which requires ML-KEM-1024 and ML-DSA-87 (NIST Category 5).

Note also that **NSA does not require hybrid** for NSS. FAQ v2.1 states NSA has confidence in the CNSA 2.0 algorithms and will not require developers to use hybrid certified products for security purposes, treating hybrid as an availability and interoperability accommodation that adds protocol complexity. The kit's hybrid-by-default posture is sound engineering for the threat model in [cryptographic exposure](/pq-readiness/threat-exposure/) — but it earns no CNSA credit, and this section does not present it as though it does. CNSA further presumes validated modules: SP 800-208 signers require CMVP-validated hardware and waivers are not granted, and no kit package is a validated module.

**This row is framed as a gap, never as alignment.** For NSS-facing adopters it is planning input. Commercial and EU-regulated adopters must not read it as a deadline that binds them — CNSA is tracked here as a benchmark that buyers sometimes borrow, not as an obligation.

### NIST FIPS 203 / 204 / 205 {#nist-fips}

**Instruments:** FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA) — all final, published 13 August 2024.

**Applicability:** any adopter asserting algorithm conformance. U.S. federal agencies are bound to FIPS via FISMA; others adopt voluntarily. Algorithm conformance is not, by itself, a module-validation obligation.

Conformance is demonstrated by passing NIST-published known-answer / ACVP test vectors for the claimed parameter set — **not by assertion, and not by using a library that describes itself as FIPS.** The gap between "uses an ML-KEM library" and "FIPS 203-conformant" is real, and the kit's commitment is to close it with test vectors rather than assertion.

> **Caution — These three rows are forward-looking**
>
> No kit primitive currently instantiates ML-KEM, ML-DSA or SLH-DSA — the cryptographic packages land in Phases 2 and 4 — so **no FIPS test vectors run today**, and no descriptor claims `fips_conformance` other than `["none"]`. The rows below record what the mapping *will* rest on, and the honesty rule that governs it: if conformance is not verified against NIST vectors in CI, `fips_conformance` stays `["none"]`, whichever library is used.

| Row | What the mapping will rest on | Status |
|---|---|---|
| **FIPS 203** (ML-KEM-768) | NIST ML-KEM-768 test vectors, to run in CI on every PR | Lands with the hybrid encryption primitive in **Phase 2** |
| **FIPS 204** (ML-DSA-44 default, ML-DSA-65 issuer-root profile) | NIST ML-DSA test vectors, to run in CI | Lands with the signature primitive in **Phase 4**; the descriptor carries `status: experimental` until third-party review |
| **FIPS 205** (e.g. SLH-DSA-SHA2-128f) | Test vectors where a primitive actually instantiates SLH-DSA | **Conditional** — no default kit primitive uses SLH-DSA, so this is exercised only if a hash-based signature is deliberately selected |

Every FIPS gap encodes the same three-way distinction: **test vectors in CI ≠ CAVP algorithm certificate ≠ CMVP module validation.**

### EU DORA — three rows

**Instruments:** Regulation (EU) 2022/2554 (in force Jan 2023, applicable from **17 January 2025**) and Commission Delegated Regulation (EU) **2024/1774** (RTS on ICT risk management).

**Applicability:** EU financial entities within DORA scope (Art. 2), **including MiCA-authorized crypto-asset service providers (CASPs)** — the strongest genuinely-applicable hook for this kit's audience. The obligation binds the financial entity, not a library.

**DORA imposes no post-quantum mandate.** The kit's genuine hook is narrower and more useful than a PQ deadline:

| Row | Control | What the kit contributes | The gap |
|---|---|---|---|
| **Art. 9(2)** (with Art. 9(4)) | ICT security policies, procedures, protocols and tools | A documented cryptographic inventory (Shor/Grover exposure) plus machine-readable per-primitive provenance the entity folds into its ICT security policy evidence | The article binds the entity and is discharged by organizational controls — governance, data classification, risk assessment, monitoring. A library cannot satisfy it |
| **CDR Art. 6(4)** | Encryption and cryptographic controls policy — Art. 6(1) requires the policy, Art. 6(2) grounds it in an approved data classification and ICT risk assessment (data at rest, in transit, and in use *where necessary*), Art. 6(4) is the kit's hook | Evidence for the **"developments in cryptanalysis"** limb at Art. 6(4): a quantum-exposure inventory and a dated hybrid migration path, giving the entity's crypto policy a concrete cryptographic-agility artifact | The entity owns the policy, the data classification, the risk assessment, in-use data handling and key management. The kit is an evidence input to the cryptanalysis-monitoring provision only |
| **CDR Art. 7** | Cryptographic key management across the full key lifecycle | Machine-readable documentation of key-derivation and hybrid KEM-wrap design, and an explicit flag on the Shor-exposed key-derivation root | A key-management-lifecycle governance obligation — generation, storage, rotation, revocation, destruction — owned and operated by the entity. The kit provides no HSM, KMS, key custody or lifecycle governance, and satisfies no part of Art. 7 |

The Art. 7 row carries a caveat the kit applies to itself: where a client key hierarchy roots in a single Shor-exposed wallet ECDSA signature, that is a residual risk the kit **reports, not resolves**. See [the key-root callout](/pq-readiness/threat-exposure/#exposure-by-primitive).

### EU NIS2

**Instrument:** Directive (EU) 2022/2555, **Art. 21(2)(h)** — "policies and procedures regarding the use of cryptography and, where appropriate, encryption." National transposition deadline 17 October 2024.

**Applicability:** essential and important entities in Annex I/II sectors, subject to size thresholds and each Member State's transposition. Implementing Regulation (EU) 2024/2690 adds technical detail for certain digital-infrastructure / ICT-service sectors.

**The scoping caveat is the point of this row.** NIS2 is a *directive*, so the operative obligation is whatever the relevant Member State's transposing law says. The kit cannot determine an adopter's in-scope status, and does not attempt to: the row's applicability and gap both state that scope must be confirmed against national law rather than read off the Directive, and the report asserts no scope of its own.

(A planned enhancement will take jurisdiction, sector and size as report inputs and output "not assessed" or "out-of-scope candidate" explicitly. Today the report simply makes no scope claim.)

The Directive is algorithm-agnostic and imposes no post-quantum mandate.

### ISO/IEC 27001:2022

**Instrument:** Annex A control **A.8.24 — Use of cryptography** (aligned with ISO/IEC 27002:2022): rules for the effective use of cryptography, including key management, defined and implemented.

**Applicability:** organizations seeking or holding ISO/IEC 27001:2022 certification. Annex A controls are subject to inclusion or exclusion with justification in the **Statement of Applicability**, so A.8.24 applies where the organization's risk assessment retains it.

**What the kit provides:** a machine-readable cryptographic inventory and per-primitive provenance — algorithm, assumption family, parameters, review date — that the organization can cite in its cryptography policy and SoA justification.

**Gap:** A.8.24 is an organizational governance control. The cryptography rules, the key-management process and their implementation are owned by the certified organization and assessed by a certification body. The kit is not an auditor and supplies no policy.

### SOC 2

**Instrument:** AICPA Trust Services Criteria 2017 (with Revised Points of Focus, 2022), common criterion **CC6.1** — logical access security software, infrastructure and architectures over protected information assets. Encryption of data at rest and in transit, and protection of encryption keys, are among its points of focus.

**Applicability:** service organizations undergoing a SOC 2 examination where the Security common criteria are in scope. **The service auditor — a licensed CPA firm — renders the opinion, not the kit.**

**Gap, stated precisely:** the kit provides evidence that a cryptographic control was *designed*. It does not provide proof that the control *operated effectively over the period*, and it renders no opinion. Key management, access provisioning and the broader CC6 series remain the entity's controls.

## Dating and re-verification

Every row carries `last_reviewed`. Frameworks evolve — instruments get amended, RTS get published, national transposition changes NIS2 scope. A crosswalk row with a stale review date is a signal in the same way a stale descriptor is.

**Rows are pinned to a named instrument version, not to a framework in the abstract.** Before relying on a row for an audit engagement, check it against the current text of the instrument named in `framework_version`. The kit re-verifies rows at each release and bumps the date.

`last_reviewed` tracks **when the row was checked against the instrument**, so it is bumped only for rows actually re-verified — never as a side effect of editing wording. Rows can therefore legitimately carry different dates, and a row whose date lags the others is telling you something real about how recently that instrument was read.

## Reading a crosswalk in an audit report

The crosswalk section of a [`@zksdk/pq-audit`](/pq-readiness/audit-quickstart/) report groups findings per control. What you get is an evidence inventory: which artifacts exist, what they show, and what the control still needs from you.

What you do not get — by design — is a score, a pass mark, or a compliance statement. Those are the auditor's judgment and the entity's obligation, and a tool that produced them would be producing a false posture.

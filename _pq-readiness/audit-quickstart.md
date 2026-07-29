---
layout: page
title: "Audit quickstart"
excerpt: "Run @zksdk/pq-audit against a project to produce a cryptographic exposure inventory and compliance-readiness evidence in JSON, Markdown, or PDF."
order: 3
toc: true
---
<!-- GENERATED FILE — DO NOT EDIT.
     Source: docs/pq-readiness/audit-quickstart.md in the pq-zksdk-compliance-kit repo.
     Regenerate with: bun run scripts/render-jekyll.ts --out <jekyll-site-root>
     Edits made here will be silently overwritten. -->

> **Interim mirror.** These pages document the PQ-zkSDK Compliance Kit and are staged
> here while the canonical home is prepared under `zksdk.com/docs/`. They are a
> contributor's working copy, not an official zkSDK publication. Where this mirror and
> the zkSDK documentation ever disagree, the zkSDK documentation is authoritative.

`@zksdk/pq-audit` inventories a project's cryptographic exposure to Shor and Grover and maps it to the frameworks regulated adopters get asked about. It requires **no post-quantum implementation** and **no code changes** — point it at a directory and read the report.

```bash
bunx @zksdk/pq-audit ./my-project
```

> **Note — Availability**
>
> Until the package is published to npm under the `@zksdk` scope, run it from a checkout of the kit:
>
> ```bash
> bun run packages/pq-audit/src/index.ts ./my-project
> ```

## What it does

Statically — **without executing any target code** — it:

1. **Scans** the project. Reads the package manifest for known cryptographic dependencies, and matches source against the import signatures of quantum-exposed primitives (Groth16/snarkjs, circomlib/Poseidon, EIP-5564/ERC-6538 stealth addresses, EIP-712/ECDSA, FHE paths). Every detection carries a confidence grade.
2. **Assesses exposure** against a built-in knowledge base: assumption family, Shor/Grover status, HNDL vs. forgery relevance, and the hybrid target per primitive.
3. **Validates emitted descriptors.** Any [`securityDescriptor()`](/pq-readiness/security-descriptor/) the project ships is validated. **A dishonest or malformed descriptor is itself a finding** — the audit will not let a Shor-broken primitive claim it is quantum-safe.
4. **Maps to frameworks** using the dated [compliance crosswalk](/pq-readiness/compliance-crosswalk/).
5. **Renders** JSON, Markdown, or PDF.

## Usage

```
pq-audit [target] [options]

ARGUMENTS
  target                Directory to audit (default: ".")

OPTIONS
  -f, --format <fmt>    json | markdown | pdf | all  (default: markdown)
  -o, --out <path>      Write output to a file/base path instead of stdout
                        (required for 'all'; recommended for 'pdf')
      --fail-on <sev>   Exit non-zero if any finding is at/above <sev>
                        (critical|high|medium|low) OR any emitted descriptor is invalid
      --ignore <list>   Comma-separated path substrings to exclude from the source
                        scan (e.g. generated code, vendored deps, fixtures)
      --profile <path>  Merge an additional detection-profile JSON on top of the
                        built-in generic knowledge base (org-specific detections)
  -v, --version         Print version
  -h, --help            Print this help
```

### Output formats

| Format | Use it for |
|---|---|
| `markdown` (default) | Reading in a terminal, pasting into a PR or an issue |
| `json` | Machine consumption — dashboards, GRC platform ingestion, diffing between runs |
| `pdf` | Inclusion in a DORA / SOC 2 / ISO 27001 evidence package |
| `all` | All three at once; requires `-o <base-path>` |

```bash
# Machine-readable, for a dashboard or a diff
bunx @zksdk/pq-audit ./my-project --format json --out audit.json

# Audit-support PDF
bunx @zksdk/pq-audit ./my-project --format pdf --out pq-audit-report.pdf

# Everything, written to pq-audit-report.{json,md,pdf}
bunx @zksdk/pq-audit ./my-project --format all --out pq-audit-report
```

### Confidence grades

Detection is heuristic text matching, **not** AST analysis. Read the grades accordingly:

| Grade | Means | Does **not** mean |
|---|---|---|
| `source` | A reference to the primitive was found in source | That the primitive is exercised at runtime |
| `dependency` | A library providing it is declared in the manifest | That the library is imported or used |
| `inherited` | Exposure arrives through a dependency on another exposed primitive | An independent detection |

Repositories that merely *reference* primitive names — security tooling, documentation, this kit's own knowledge base — will over-report. Exclude those paths:

```bash
bunx @zksdk/pq-audit . --ignore vendor/,generated/,test/fixtures
```

### Gating CI

`--fail-on` exits **2** when a finding is at or above the given severity, **or** when any descriptor the project emits fails validation. That second condition is the one worth wiring up early: it catches a primitive that starts claiming more than it delivers. (Exit `0` is a clean run; exit `1` is a tool error such as an unreadable target.)

Start at `critical` on an existing codebase and tighten as you migrate — an established stack will report `high` findings on day one, because Groth16 and secp256k1 are genuinely Shor-exposed, and a gate that always fails gets switched off.

```yaml
- name: PQ exposure audit
  run: bunx @zksdk/pq-audit . --fail-on critical --ignore test/fixtures
```

### Organization-specific detections

`--profile` merges an additional detection profile over the built-in knowledge base, so internal module paths and findings from private security review stay out of the published package:

```bash
bunx @zksdk/pq-audit ./my-project --profile ./audit-profiles/internal.profile.json
```

A profile is plain JSON and is never executed. Profile entry ids must be disjoint from the built-in entries — a profile may only **add** detections, never silently redefine a shipped one.

## Reading the report

A report opens with the posture summary and the disclaimers, then findings, then the framework crosswalk.

```markdown
# Post-Quantum Cryptographic Exposure & Compliance-Readiness Report

**Posture:** 9 cryptographic exposure findings detected; 4 Shor-broken by own
assumption — quantum_security_bits: 0 for these; 4 HNDL-relevant
(harvest-now-decrypt-later); 5 forgery/soundness-relevant.

## Posture summary

| Metric | Value |
| --- | --- |
| Total findings | 9 |
| Shor-broken by own assumption | **yes** (4) |
| Compromised via a Shor-broken dependency | 0 |
| Grover-reduced (hash) | 1 |
| Believed PQ-secure | 1 |
| HNDL-relevant surface | 4 |
| Forgery/soundness-relevant surface | 5 |
| Primitives / Residual / Operational | 4 / 3 / 2 |
| Emitted descriptors valid / invalid | 1 / 0 |

Severity: 🔴 Critical 1 · 🟠 High 4 · 🟡 Medium 1 · 🔵 Low 1 · ⚪ Info 2
```

The posture line is a **characterisation, not a verdict**. It does not grade you, and there is no passing score. Each finding then expands with its assumption family, quantum status, concrete impact, hybrid target, what triggered the detection, and the provenance of the claim.

Findings come in three categories — **primitives** (detected exposure), **residual** (known exposure with no v1 replacement, reported whether or not it was detected), and **operational** (non-quantum findings that invalidate the security story anyway, such as a development-grade trusted setup).

## Honesty guarantees

Every report carries these, and they are not removable:

- The report **characterises exposure and compliance readiness. It does not certify, attest, or establish compliance** with any framework.
- FIPS conformance claimed anywhere in this kit is **algorithm-level only** (NIST test vectors in CI). It is **not** FIPS 140-3 / CMVP module validation. No package in this kit is a validated cryptographic module.
- Detection is **static** — no project code is executed. **Absence of a finding is not proof of absence of exposure.**
- Quantum-status claims follow the assumption family: Shor-broken is reported as `quantum_security_bits: 0`, not a small number.
- Residual risks with no v1 replacement are disclosed, **never silently omitted**.

## Build

`bun run build` compiles a self-contained single binary (`bun build --compile`) — no runtime dependencies, no `eval`, with the crosswalk data and validators embedded. The only runtime dependency of the source is [`@zksdk/security-descriptor`](/pq-readiness/security-descriptor/).

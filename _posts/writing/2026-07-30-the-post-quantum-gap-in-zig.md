---
layout: post
title: "The post-quantum gap in Zig — shipping slh-dsa-zig"
excerpt: "slh-dsa-zig is a pure-Zig implementation of SLH-DSA (FIPS 205), all twelve parameter sets, KAT-validated against NIST ACVP. What hash-based signatures are for, what Zig was missing, what this library does and does not yet claim, and where it goes next."
modified: 2026-07-30
category: writing
tags: [Post-Quantum Cryptography, Zig, Open Source, SLH-DSA]
author: nandan
comments: false
share: false
---

This started with a smaller question. I have been maintaining [`tweetnacl-zig`](https://github.com/nandanito/tweetnacl-zig), a faithful port of Dan Bernstein's TweetNaCl to Zig, and someone asked whether it could be made post-quantum. The honest answer is no: TweetNaCl predates the post-quantum standards, `crypto_box` is X25519 and `crypto_sign` is Ed25519, and a sufficiently large quantum computer running Shor's algorithm breaks both of them outright. A post-quantum version of NaCl is not a port. It is a different library, with different primitives, different combiners, and a different threat-model posture.

So I built one, starting with the piece Zig was missing entirely. **[`slh-dsa-zig`](https://github.com/nandanito/slh-dsa-zig) v0.1.1 is tagged today**: a pure-Zig implementation of SLH-DSA — the stateless hash-based signature scheme standardised as [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) in August 2024, and known before that as SPHINCS+. All twelve parameter sets, validated against the NIST ACVP vectors.

For context on why post-quantum migration matters on this timescale rather than a later one, my earlier piece [Quantum-safe custody](/writing/quantum-safe-custody/) covers the urgency argument. This post picks up after it.

<!--more-->

**Status, before anything else: experimental. Not audited. Do not use in production.** Passing known-answer tests proves conformance to a specification. It does not prove resistance to an attacker. The banner stays on the README until that distinction closes.

## What shipped

[`v0.1.1`](https://github.com/nandanito/slh-dsa-zig/releases/tag/v0.1.1) is tagged as of 30 July 2026, marked as a pre-release so it does not occupy the "Latest release" slot while the experimental banner is up. It needs Zig 0.16.0.

There are two tags dated today. `v0.1.0` was tagged hours earlier and shipped two documentation defects: a stale example header claiming the library panics, and a benchmark attribution naming the wrong hash primitive. The library itself is behaviour-identical — `git diff v0.1.0..v0.1.1 -- src/` is comment-only. `v0.1.0` stays published and marked superseded, because that is the honest record of what was tagged.

```
zig fetch --save git+https://github.com/nandanito/slh-dsa-zig.git#v0.1.1
```

Pin the tag. Without the `#v0.1.1` suffix `zig fetch` resolves the default branch, which is a moving target — and since the manifest carries a release version either way, the resolved dependency ends up labelled with a version number that need not correspond to any tag.

The API is comptime-parameterised. You pick a parameter set and get back a namespace in which every buffer size is a compile-time constant:

```zig
const std = @import("std");
const slh_dsa = @import("slh_dsa");

pub fn main(init: std.process.Init) !void {
    const Scheme = slh_dsa.Slh_Dsa(.slh_dsa_shake_128s);

    const kp = try Scheme.KeyPair.generate(init.io);

    const message = "attack at dawn";
    var sig: [Scheme.signature_length]u8 = undefined;
    try Scheme.sign(&sig, message, &kp.secret_key, null);
    try Scheme.verify(&sig, message, &kp.public_key);
}
```

That covers key generation, signing, and verification for all twelve parameter sets across both hash families, with and without context strings. The pre-hash variants are not implemented. There is no shared library, no DLL, no FFI surface — it is a Zig library for Zig programs.

Code is 0BSD; the documentation is CC BY 4.0. 0BSD drops even the attribution clause MIT keeps, which is the right posture for cryptographic code that should be trivial to vendor and adapt. It is the wrong posture for prose: if the chapters help someone build their own implementation, saying so is the ask.

## The Zig PQ landscape

Zig is ahead of most systems-language standard libraries on the post-quantum question. `std.crypto` already ships:

- **ML-KEM** (FIPS 203) in the 512, 768, and 1024 parameter sets.
- **ML-DSA** (FIPS 204) in the 44, 65, and 87 parameter sets.
- **`MlKem768X25519`**, a hybrid KEM combining classical X25519 with ML-KEM-768 — the same construction TLS 1.3 deployments and age now use.
- **`kyber_d00`**, retained as a legacy draft for compatibility with older deployments.

The credit for that belongs to the contributors who landed those patches. The gaps, by my reading:

| Algorithm | Standard | Status in Zig | Where it matters |
|---|---|---|---|
| **SLH-DSA** (SPHINCS+) | FIPS 205 (Aug 2024) | Missing from `std.crypto` | Firmware and code signing; conservative PQ signature |
| **FN-DSA** (Falcon) | FIPS 206 — draft submitted for approval Aug 2025; final expected late 2026 / early 2027 | Not yet standardised | Smaller signatures than ML-DSA |
| **HQC** | Selected by NIST Mar 2025 as a backup KEM; draft pending, final expected 2027 | Missing everywhere except libOQS | Code-based KEM; ML-KEM backup |
| **XMSS / LMS / HSS** | RFC 8391 / 8554 / SP 800-208 | Missing for general use | Stateful hash-based for firmware updates |
| Hybrid signatures | IETF drafts | Not in `std.crypto` | TLS and PQXDH hybrid auth |
| Protocol-level constructs | PQXDH, X-Wing named export, Noise-PQ | All missing | Real-world deployment |

Note the correction on HQC against how it is often described: NIST *selected* it in March 2025 as a backup to ML-KEM. It is not standardised — the draft has not appeared yet, and a final standard is expected in 2027.

A note on what I did not start with. HQC is a genuinely important code-based backstop, but it has no final standard to implement against yet, and ML-KEM has the operational momentum. Stateful hash-based schemes — XMSS, LMS, HSS — solve a narrower problem, and their state-management semantics make them a different kind of project from a NaCl-philosophy library. Both are gaps worth filling. Neither was the gap to start with.

## A note on adjacent efforts

A few Zig PQC projects already exist. They are solving different problems, mostly well within their scope.

- [**`GhostKellz/zcrypto`**](https://github.com/GhostKellz/zcrypto) — a modular Zig crypto library, now at v1.0.6 with a stable core and feature-gated experimental modules. Its post-quantum signatures are ML-DSA-65; SLH-DSA was removed, and the roadmap says it returns only once a `std.crypto` backend exists, explicitly declining to hand-roll one.
- [**`OnlyF0uR/pqc-zig`**](https://github.com/OnlyF0uR/pqc-zig) — Zig bindings to PQClean. Useful, but not pure Zig, and the SPHINCS+ parameter sets are listed as supported-in-principle rather than wired up.
- [**`blockblaz/hash-zig`**](https://github.com/blockblaz/hash-zig) — pure Zig Generalized XMSS with verified Rust interop, scoped to Ethereum's leanSig rather than general use.

The space `slh-dsa-zig` occupies is the focused, pure-Zig, audit-track implementation of the FIPS 205 standard itself.

## What SLH-DSA is, briefly

SLH-DSA is the conservative choice among NIST's post-quantum signature standards. Where ML-DSA rests on lattice assumptions — well studied, but young by cryptographic standards — SLH-DSA rests on nothing but hash functions. If SHA-2 and SHAKE hold, SLH-DSA holds. No factoring, no discrete logarithms, no lattices.

The price is size and speed. An SLH-DSA-128s signature is 7,856 bytes against Ed25519's 64, and signing costs millions of hash invocations. The public key, though, is 32 bytes — the smallest of any NIST post-quantum signature standard. That shape is the whole reason it is positioned as a conservative hedge rather than a default: it is well suited to signing firmware once and verifying it many times on a device that must not be wrong.

The construction stacks WOTS+ one-time signatures under XMSS Merkle trees, stacks those trees into a hypertree, and uses FORS — a Forest Of Random Subsets — to sign the message digest itself.

<figure>
  <img src="/images/posts/pq-zig/slh-dsa-structure.svg" alt="SLH-DSA structure diagram: three stacked XMSS trees forming the hypertree, with WOTS+ one-time signatures at the leaves and a FORS tree branching off for message signing.">
  <figcaption>SLH-DSA structure: a hypertree of XMSS trees, with FORS for message signing.</figcaption>
</figure>

I am not going to walk through that here, because I wrote something better. The **[documentation site](https://nandan.me/slh-dsa-zig/)** is a 33-page learning-oriented guide to the scheme: why classical signatures are on a clock, why hash-based signatures — an idea from 1979 — turned out to be the conservative answer, and then eight chapters that build SLH-DSA from a one-time signature, each solving the problem the last one created. Beyond that there are per-module walkthroughs mapping every FIPS 205 algorithm to the function in `src/` that implements it, a glossary of 79 terms, and a [build-it-yourself study path](https://nandan.me/slh-dsa-zig/build-it-yourself/) with exercises and self-check questions for anyone who wants to derive the scheme from the standard themselves.

FIPS 205 is precise, complete, and almost entirely silent on motivation. It tells you what to compute and never why that computation is the right one. Read cold, WOTS+ chains and FORS forests look like arbitrary complexity. They are not — each is the cheapest available answer to a problem created by the previous design decision. Reconstructing that chain of reasoning is what the site is for.

One citation note that cost me time and may save you some: cite the **final** FIPS 205 of August 2024, never the initial public draft. The final standard inserted `gen_len2` as Algorithm 1 in §3.2, which shifted every subsequent algorithm number by one and renumbered the WOTS+ subsections. A section number recalled from a draft-era paper or blog post is very likely off by one.

## How it is tested, and what that does not prove

Every parameter set passes the NIST ACVP vectors for keyGen, sigGen, and sigVer. That is the primary correctness gate and the only one checked against external ground truth. One structural wrinkle worth knowing if you are testing an implementation of your own: ACVP publishes vectors only at scheme level. There are none for WOTS+, XMSS, the hypertree, or FORS individually. Those are covered by the scheme-level KATs that exercise them, by spec-derived property tests, and — where a component was not yet reachable from a passing scheme-level KAT — by intermediate fixtures lifted from the SPHINCS+ and PQClean references. Fixtures, never code.

Constant-time behaviour is checked in CI by running harnesses under Valgrind with `SK.seed` and `SK.prf` marked tainted, failing on any secret-dependent branch or memory access.

The interesting problem there is that almost every intermediate value in a signature descends from `SK.seed`, while almost none of them are secret. A whole-path taint audit drowns in false positives unless the public values are classified explicitly. `src/ct.zig` provides a `declassify` helper, called wherever FIPS 205 publishes a value — `R` (§9.2), `PK_FORS` (§9.3), and the XMSS roots (§7.2) — and compiling to nothing unless the module is built with Valgrind support. There is also a negative control: a harness that *should* be flagged, which fails the job if it ever passes. Without it, a clean run is indistinguishable from a run where the taint markers silently went inert.

Beyond that, property tests for round-trips, tamper detection and serialisation, and fuzz harnesses on the verifier and the ACVP parser — the two attacker-facing surfaces.

What none of this proves is that the library is safe to deploy. KATs establish that the implementation computes what the standard says to compute. They say nothing about whether an attacker with a timer, a power probe, or a fault injector can extract a key. That gap closes with a third-party audit, and only then.

## The benchmark gate, and the one number that fails it

The project targets performance within 2× of PQClean's portable `clean` C reference. Wording that gate correctly took longer than measuring it, and the reasoning generalises beyond this project.

The original wording was "within 2× on equivalent hardware". PQClean `clean` is portable C by definition — it cannot use SHA-NI or the ARMv8 crypto extensions. Comparing a hardware-accelerated Zig build against it measures the CPU's hash unit rather than the library, and it produces a gate that *cannot fail for the right reason*: the machinery around the hash could regress badly and the hardware speedup would hide it. So the gate is now **within 2× of PQClean's portable `clean` reference, both sides built without hardware hash acceleration** — on x86-64, `-Dcpu=x86_64_v3`, the same baseline the constant-time workflow pins. "Equivalent hardware" was unfalsifiable; a named target is reproducible.

Measured 2026-07-30 on an AMD EPYC 9V74, gcc 13.3, Linux:

| leg | SHA-2 | SHAKE | over 2× |
|---|---|---|---|
| portable (`x86_64_v3`) — **the gate** | 1.73×–2.06× (mean 1.85×) | 0.87×–0.98× | **1 of 36** |
| accelerated (`x86_64_v3+sha`) | 0.33×–0.63× | 0.87×–1.00× | 0 of 36 |
| PQClean `avx2` against its own `clean` | — | — | 2.3×–4.3× faster |

**35 of 36 pass.** That is better than forecast: [issue #40](https://github.com/nandanito/slh-dsa-zig/issues/40) had predicted nine of eighteen SHA-2 measurements over the gate, extrapolating from an arm64 rebuild with the crypto extensions disabled. The actual figure was one of eighteen, at a mean of 1.85× — a pessimistic extrapolation that did not survive measurement.

The exceedance is `SLH-DSA-SHA2-256s keygen`, at 2.06× against a 2.00× gate. It is reported rather than papered over, and it can be attributed rather than merely excused — though the attribution needs stating carefully, because the obvious version of it is too strong.

Every structural module — WOTS+ chains, XMSS tree hashing, the hypertree, FORS — takes its hash functions from a single adapter selected at comptime, and none of them knows which family it is running on. That code is shared between SHAKE and SHA-2 line for line. What differs is the adapter beneath: SHAKE feeds the expanded 32-byte address to Keccak throughout, while SHA-2 feeds a 22-byte compressed address, uses MGF1 for variable-length output, and moves from SHA-256 to SHA-512 above security category 1.

So this is not quite "same code, different hash". But the two extra differences push toward the conclusion rather than away from it: SHA-2 hashes ten fewer bytes of address per call and is still slower, and MGF1 runs once per operation against millions of F and H invocations. Meanwhile SHAKE sits at 0.96× — parity with PQClean's portable Keccak, on shared structural code. The shortfall therefore isolates to `std.crypto`'s portable SHA-2 implementations rather than to this library's SLH-DSA machinery — though not to SHA-256 specifically, since `SLH-DSA-SHA2-256s` runs at n=32, where keygen drives F through SHA-256 and H through SHA-512. Both are implicated, and both are upstream code this project does not control.

Which is a more useful claim than "36 of 36 passes", and it survives someone else re-measuring. What it deliberately does not claim is precision: 2.06× is one measurement on a shared CI runner, and noise could plausibly move it under the line. The run has not been repeated to find out, because re-rolling until a published number passes is not a methodology. Full tables and provenance are in [`bench/README.md`](https://github.com/nandanito/slh-dsa-zig/blob/main/bench/README.md).

## Known limitations

Explicitly, because "experimental" is easy to skim past:

- **Not audited.** No third party has reviewed this code.
- **The constant-time result is narrower than it sounds.** x86-64-v3 only, with AVX-512 paths excluded because Valgrind cannot decode them ([#6](https://github.com/nandanito/slh-dsa-zig/issues/6)), and run on four parameter sets chosen to cover every adapter code path rather than on all twelve. That is a reasoned coverage argument, not twelve measured runs.
- **The 24-hour cumulative fuzz target has not been reached.** Harnesses and the nightly workflow are merged and accruing.
- **One benchmark measurement exceeds its gate**, as above.
- **HashSLH-DSA (the pre-hash variants) is not implemented** ([#45](https://github.com/nandanito/slh-dsa-zig/issues/45)) — a deliberate deferral, and those ACVP groups are skipped explicitly rather than silently dropped.
- **A known performance gap.** `xmss_sign` recomputes shared subtrees when building authentication paths ([#38](https://github.com/nandanito/slh-dsa-zig/issues/38)).

## The two lanes

If you open the repository you will find an `upstream-candidate/` directory, and it needs a word of explanation.

Everything else is Lane A: the library, tests, benchmarks, examples, and the documentation site. AI assistance is permitted there, and I review and shape every line that ships. `upstream-candidate/` is Lane B — human-authored only, reserved for a from-scratch second reading of FIPS 205, with the rule enforced by a commit-trailer check in CI.

The reason is not provenance for its own sake. It is independence. Two implementations of one specification are worth more than one, and the second one's value depends entirely on having been derived separately. Where they disagree, one of them is wrong, and that disagreement is a far stronger signal than either implementation agreeing with itself. Having the same assistant draft both would produce two implementations that share their mistakes — duplication wearing a disguise.

Lane B was originally aimed at contributing SLH-DSA upstream to `std.crypto`. That is no longer on the roadmap, and the short version of why may be useful to anyone planning work around someone else's contribution rules.

I designed the arrangement in May, reserving a narrow set of AI roles on the Lane B side: spec interpretation, study support, review of code I had written. At the end of that month Ziglang published its [Code of Conduct](https://ziglang.org/code-of-conduct/) in its current form, prohibiting LLM use for code and prose, for editing, for finding bugs, and for brainstorming whose results are then shared. The roles I had reserved are named in that list. The discipline was aimed at a line that moved a week after I finished aiming.

Their reasoning is defensible, and I thought so before it affected me: a small core team, a large review backlog, and mentorship as a stated part of the mission. A policy that lets a reviewer assume a human thought about every line is a rational use of scarce attention, and it is entirely theirs to set. So upstreaming moved from a scheduled deliverable to a separate decision, to be taken later on its own merits. The directory stays with its rules in force, because the independence argument does not depend on where that second reading eventually goes.

The transferable part: a plan that depends on someone else's policy holding still has a dependency you cannot version-pin. This one survived because the library was worth building on its own terms. Had I scoped the project so that upstreaming was the deliverable, two months of work would have been aimed at a target that no longer existed.

## Where this goes next

The `pq-zig` GitHub organisation now exists but is empty. Two further libraries are *named intentions*, not tracked work, and I would rather say so than imply a roadmap I am not currently executing.

**`pq-nacl`** would be a NaCl-style minimal API for the post-quantum world: ML-KEM exposed as the X-Wing hybrid construction, hybrid signing combining Ed25519 with ML-DSA, and SLH-DSA as a conservative mode. A spiritual successor to `tweetnacl-zig`, kept separate so both stay intellectually clean.

The interesting design content there is the hybrid. A hybrid KEM combines a classical primitive with a post-quantum one such that the result stays secure as long as *either* component is unbroken — the threat model being that we are not yet certain lattices survive cryptanalysis, and we are certain X25519 does not survive a large quantum computer. [X-Wing](https://datatracker.ietf.org/doc/draft-connolly-cfrg-xwing-kem/) is the construction `MlKem768X25519` already implements in `std.crypto`.

X-Wing derives its shared secret with SHA3-256 over both shared secrets, both X25519 public keys, and a constant label — and it is worth being precise about what that buys. The authors prove classical IND-CCA security in the random oracle model under a strong Diffie–Hellman assumption, and post-quantum IND-CCA security in the standard model assuming ML-KEM-768 is IND-CCA and SHA3-256 is a secure PRF. Loosely: secure if either component is. They also stress that X-Wing is a concrete construction rather than a generic combiner. Generic combiners with proofs do exist; X-Wing's efficiency comes from shortcuts — not hashing the ML-KEM ciphertext, flattening DHKEM — that are only sound because of the specific primitives chosen, and do not transfer.

<figure>
  <img src="/images/posts/pq-zig/x-wing-combiner.svg" alt="X-Wing hybrid KEM: X25519 shared secret and ML-KEM-768 shared secret both feed into SHA3-256, along with both X25519 public keys and a domain-separation label, producing a single hybrid shared secret.">
  <figcaption>X-Wing: secure if either X25519 or ML-KEM-768 is unbroken.</figcaption>
</figure>

If `pq-nacl` happens, it exposes this directly rather than hiding it behind a `box`-style primitive that obscures the construction. If you are reaching for a hybrid KEM you should know which one, and why.

**`agez`** would be a pure-Zig implementation of the [age v1 format](https://age-encryption.org/v1) with first-class `mlkem768x25519` recipient support, interop-tested against [Go age](https://github.com/FiloSottile/age) and [Rust rage](https://github.com/str4d/rage).

But the direction I am actually most interested in is **post-quantum cryptography on embedded devices**, and it is why the from-scratch Lane B implementation is worth finishing regardless of where it is ever submitted. SLH-DSA is unusually well suited to that setting and unusually badly suited to it at the same time: a 32-byte public key and hash-only security assumptions are close to ideal for verifying firmware on a constrained device, while a 7,856-byte signature and millions of hash invocations per signature are not. The engineering questions that follow — stack budgets without an allocator, verification cost on a microcontroller, whether hardware hash acceleration changes the parameter-set calculus, what a fault-injection threat model does to the constant-time argument — are the ones I want to spend the next stretch on. A comptime-parameterised, allocation-free implementation with no FFI surface is a reasonable place to start asking them.

## Cryptographic discipline

The defaults every primitive is built against. These are gates, not aspirations:

- **Constant-time.** No secret-dependent branches or memory accesses. Verified empirically under Valgrind in CI, with the coverage caveats stated above.
- **No allocator in hot paths.** Stack allocation and comptime sizing throughout the crypto core.
- **Explicit secret zeroisation.** Sensitive buffers zeroed before scope exit, with compiler barriers where the optimiser might otherwise drop the stores.
- **KAT-validated.** NIST ACVP vectors pass before a component is declared functional.
- **Fuzzed.** Every attacker-facing parser and the verify path carries a harness. GitHub Actions caps a job at six hours, so the 24-hour target is *cumulative*: a nightly workflow fuzzes for a bounded window, persists the corpus, and accrues toward the total.
- **Benchmarked.** Within 2× of [PQClean's](https://github.com/PQClean/PQClean) portable `clean` C reference, both sides built without hardware hash acceleration. Accelerated and PQClean AVX2 numbers are published alongside, but never gated on.

## The trajectory

| Stage | What it means | Cost |
|---|---|---|
| Experimental | KATs pass, builds clean, banner prominent | Time only |
| Beta | Constant-time audit pass, fuzz harness, informal third-party review | Time + small bounties |
| Production-candidate | Formal third-party security audit by a recognised firm | Estimated $40K–$150K |
| Production | Audit recommendations addressed, reproducible builds, ongoing maintenance | Ongoing |

v0.1.1 is the first row. Reaching the third costs real money, and the funding paths worth looking at are NLnet Foundation (NGI0), the Open Tech Fund, OpenSSF Alpha-Omega, and the Sovereign Tech Fund. The "pure-Zig PQ primitives, public-good infrastructure" framing fits what those funders exist to support. I would rather make that path visible early than discover it late.

## Feedback

Contributors are welcome on the standalone library. Reviewers are more welcome still — particularly anyone with FIPS 205 implementation experience, constant-time discipline, or side-channel analysis expertise. Security issues should follow the responsible-disclosure procedure in [SECURITY.md](https://github.com/nandanito/slh-dsa-zig/blob/main/SECURITY.md) rather than a public issue.

The most valuable thing anyone can do with this code right now is find something wrong with it. Bug reports, harsh review, and pointed questions about specific cryptographic decisions are all better than stars.

Repository: [`nandanito/slh-dsa-zig`](https://github.com/nandanito/slh-dsa-zig). Documentation: [nandan.me/slh-dsa-zig](https://nandan.me/slh-dsa-zig/). Predecessor: [`tweetnacl-zig`](https://github.com/nandanito/tweetnacl-zig).

If something in this is wrong or naive, please tell me.

---

## References

**NIST standards**
- [FIPS 203 — ML-KEM](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [FIPS 204 — ML-DSA](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- [FIPS 205 — SLH-DSA](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (final, August 2024)
- [NIST PQC standardization](https://csrc.nist.gov/Projects/post-quantum-cryptography/post-quantum-cryptography-standardization) — HQC selection and round status

**IETF and protocol specs**
- [X-Wing hybrid KEM draft](https://datatracker.ietf.org/doc/draft-connolly-cfrg-xwing-kem/) · [the paper](https://eprint.iacr.org/2024/039)
- [age v1 spec](https://age-encryption.org/v1)
- [PQXDH spec](https://signal.org/docs/specifications/pqxdh/)

**Zig**
- [Zig on Codeberg](https://codeberg.org/ziglang/zig) — canonical since 26 November 2025; the GitHub mirror is read-only and issues and pull requests were not migrated
- [Zig Code of Conduct](https://ziglang.org/code-of-conduct/)
- [`std.crypto`](https://codeberg.org/ziglang/zig/src/branch/master/lib/std/crypto.zig)
- [ML-KEM in Zig](https://codeberg.org/ziglang/zig/src/branch/master/lib/std/crypto/ml_kem)
- [ML-DSA in Zig](https://codeberg.org/ziglang/zig/src/branch/master/lib/std/crypto/ml_dsa)

**Reference implementations**
- [PQClean](https://github.com/PQClean/PQClean)
- [SPHINCS+ reference](https://github.com/sphincs/sphincsplus)

**Adjacent Zig PQC efforts**
- [`GhostKellz/zcrypto`](https://github.com/GhostKellz/zcrypto)
- [`OnlyF0uR/pqc-zig`](https://github.com/OnlyF0uR/pqc-zig)
- [`blockblaz/hash-zig`](https://github.com/blockblaz/hash-zig)

**age ecosystem**
- [Go age](https://github.com/FiloSottile/age)
- [Rust rage](https://github.com/str4d/rage)

**This project**
- [`slh-dsa-zig` v0.1.1](https://github.com/nandanito/slh-dsa-zig/releases/tag/v0.1.1) · [repository](https://github.com/nandanito/slh-dsa-zig) · [documentation](https://nandan.me/slh-dsa-zig/) · [architecture](https://github.com/nandanito/slh-dsa-zig/blob/main/ARCHITECTURE.md) · [benchmarks](https://github.com/nandanito/slh-dsa-zig/blob/main/bench/README.md)
- [`tweetnacl-zig`](https://github.com/nandanito/tweetnacl-zig)
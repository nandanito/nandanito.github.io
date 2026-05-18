---
layout: post
title: "Quantum-safe custody — what changes for hardware-anchored and MPC signing when ECDSA falls"
excerpt: "The planning baseline for Q-Day compressed in March 2026, and the question for institutional digital-asset custody is no longer when, but whether the cryptography can be migrated fast enough. Hardware-anchored signing and MPC have different migration paths — and one will be substantially easier."
modified: 2026-05-17
category: writing
tags: [Quantum Cryptography, Post-Quantum Cryptography, Digital Assets, Custody, Crypto-Agility, IBM Quantum Safe, Methodology]
author: nandan
comments: false
share: false
---

For roughly a decade, the standard answer to *"when will quantum computers break ECDSA-256"* was *"in ten to fifteen years, give or take, and probably toward the back of that range."* That answer no longer survives contact with the March 2026 resource estimates.

The practical question for institutional digital-asset custody is therefore not only *when*. It is whether the cryptography can be replaced before the risk becomes operational.

<!--more-->

The older answer rested on Craig Gidney's 2019–2021 resource estimates, which put the qubit count for a Shor's-algorithm attack on a 256-bit elliptic-curve signature at around one million physical qubits. One million was a long way away. Everyone agreed it was. That agreement was the quiet basis on which institutional digital-asset custody, banking PKI, and most other public-key cryptography continued to use algorithms whose expiry date was assumed to be comfortably distant.

The agreement no longer holds.

In March 2026, a [Google Quantum AI whitepaper](https://quantumai.google/static/site-assets/downloads/cryptocurrency-whitepaper.pdf), co-authored with Justin Drake of the Ethereum Foundation and Dan Boneh of Stanford, brought the resource estimate down by more than an order of magnitude. The new estimate for attacking secp256k1 is fewer than 500,000 physical qubits, with runtime measured in minutes on fast-clock architectures under the paper's assumptions. The paper estimates roughly 9–12 minutes for an on-spend attack against secp256k1, with about 9 minutes attributable to the target key once precomputation is accounted for — meaningful because about half of the computation can be run before the target public key is even known.

Around the same time, a [Caltech and Oratomic preprint](https://arxiv.org/abs/2603.28627) showed that Shor's algorithm may be possible at cryptographically relevant scales with as few as 10,000 reconfigurable neutral-atom qubits. Under plausible assumptions, the authors estimate that a P-256 discrete-logarithm attack could take a few days on a 26,000-qubit neutral-atom system.

Neither result means Q-Day is in 2027. They are resource estimates, not deployed machines. They also remain whitepaper and preprint results rather than settled engineering fact. But they have been taken seriously enough by the cryptography and quantum-computing communities that the older planning posture now looks unsafe. Gidney's one-million-qubit baseline, the number behind the comfortable ten-year answer, is no longer the right anchor.

<figure>
  <img src="/images/posts/quantum-safe-custody/figure-3-timeline.svg" alt="Timeline showing post-quantum cryptography migration milestones between 2024 and 2035, including NIST standards in August 2024, the March 2026 inflection from the Google and Caltech papers, Ethereum's post-quantum security team in January 2026, Tron's mainnet PQC announcement in April 2026, CNSA 2.0 acquisition deadlines, Google and Cloudflare's 2029 targets, and the 2035 full-transition target.">
  <figcaption>Regulatory, corporate, and industry milestones on a single timeline. The March 2026 inflection sits at the centre.</figcaption>
</figure>

The policy and infrastructure timelines are also moving. NIST published the first three post-quantum cryptographic standards — ML-KEM, ML-DSA, and SLH-DSA — in August 2024. NSA's CNSA 2.0 transition, as interpreted by NIAP and NSA compliance guidance, sets January 1, 2027 for new CNSA-capable acquisitions, phase-out of non-CNSA-capable equipment by end-2030, and CNSA 2.0 mandatory across National Security Systems by end-2031 — with the full transition targeted for 2035 in line with NSM-10. NIST guidance continues to point toward broader deprecation of many quantum-vulnerable algorithms by 2030 and disallowance by 2035. [Both Google and Cloudflare have publicly set 2029 targets for being fully post-quantum secure, including authentication](https://blog.cloudflare.com/post-quantum-roadmap/) — which matters, because post-quantum signatures lag post-quantum key exchange in most production deployments, and a 2029 authentication deadline is the ambitious end of those commitments.

As [CNN reported](https://www.cnn.com/2026/05/17/science/quantum-computing-cybersecurity-q-day), Dustin Moody, a NIST mathematician working on the post-quantum cryptography standards, has observed that past cryptographic migrations have typically taken a decade or two, and the post-quantum transition is likely to be harder and more expensive than its predecessors. Institutional digital-asset custody is one of the more complicated cases.

Public blockchains are beginning to respond, unevenly. [Tron's Justin Sun said in April 2026](https://x.com/justinsuntron/status/2044179729067245837) that TRON would deploy NIST-standardized post-quantum signatures on mainnet, aiming to be the first major public blockchain to do so. Bitcoin is debating [BIP-361](https://github.com/bitcoin/bips/blob/master/bip-0361.mediawiki), which discusses freezing legacy signature outputs after a migration period and states that more than 34% of bitcoin had exposed public keys on-chain as of March 1, 2026 — coins that could be stolen by an attacker with a sufficiently powerful quantum computer, with no clean recovery path once a private key is derived. Ethereum has had a post-quantum security effort since January 2026, led by Thomas Coratger, with two million dollars committed across the Poseidon and Proximity Prizes for post-quantum cryptographic research.

Bitcoin's exposed keys are the most visible case of a broader pattern that custody operators have to plan around: *harvest now, decrypt later* attacks, in which adversaries — state-level or otherwise — are presumed to be collecting encrypted material today to decrypt once cryptographically relevant quantum computers exist. For institutional custody, the long-lived artifacts at risk are not only live signing keys. Key archives, encrypted wallet backups, settled-transaction records, and any cryptographic state that has to remain confidential for years rather than seconds all fall inside the harvest window. The migration timeline therefore cannot be paced to Q-Day. It has to be paced to the data whose confidentiality has to outlast Q-Day.

<figure>
  <img src="/images/posts/quantum-safe-custody/figure-1-architecture-comparison.svg" alt="Side-by-side comparison of hardware-anchored signing and MPC signing under post-quantum cryptographic migration across six dimensions: where signing happens, what bounds migration speed, upgrade path, attestation chain, PQC production status, and the dominant unknown for each architecture.">
  <figcaption>Hardware-anchored and MPC signing face different migration problems. The differentiator is crypto-agility built before the emergency.</figcaption>
</figure>

The quantum technology writer [Anastasia Marchenkova framed the better question](https://x.com/amarchenkova/status/2048545203510743298):

> *"When is Q-Day?" is the question that makes you feel like companies are trying to buy time. "Can you change your cryptography fast?" is the question that tells you whether you do.*

For institutional digital-asset custody, that question distinguishes a well-architected platform from one that will be expensive to migrate, regardless of when migration becomes mandatory. The architectural choices that determine the answer differ in two major directions: hardware-anchored signing and MPC. Both are in production. Both face post-quantum migration. They do not face the same migration problem.

## Hardware-anchored signing under post-quantum migration

Hardware-anchored signing protects private keys by binding them to Hardware Security Modules, secure enclaves, or related trusted hardware boundaries. Vendors and platforms in this category include Thales Luna, Utimaco, AWS CloudHSM, Microsoft Azure Key Vault Managed HSM, [IBM Cloud Hyper Protect Crypto Services](https://cloud.ibm.com/docs/overview?topic=overview-security#quantum), and institutional custody platforms such as Ripple Custody — formerly Metaco Harmonize — where HSM-backed key control is a core part of the security model. Intel SGX and similar enclave technologies sit in the adjacent secure-enclave category.

The model is straightforward in principle: the private key never leaves the hardware boundary, and the signing operation happens inside it. Post-quantum migration changes three things.

First, **firmware-level algorithm support**. Hardware-anchored signing under ML-DSA or SLH-DSA requires the HSM firmware to support those algorithms. Vendor roadmaps vary, and FIPS validation adds its own clock. IBM says Hyper Protect Crypto Services supports quantum-safe digital signing today using Dilithium (CRYSTALS-Dilithium, the algorithm now standardized as ML-DSA). Other major HSM vendors have public post-quantum roadmaps, but support differs by product line, algorithm, validation status, and deployment model. For a custody platform anchored to a specific HSM vendor, the effective post-quantum readiness date is the slower of the vendor's roadmap and the platform's own integration work.

Second, **key rotation under algorithm change**. ECDSA keys provisioned today cannot be migrated to ML-DSA by re-signing the same private key. The primitives are unrelated, the public-key formats differ, and the on-chain or off-chain addresses derived from those keys are not portable. A custody platform migrating from ECDSA to ML-DSA must generate new keys, transfer assets to addresses derived from those keys, and decommission old keys. That is not a patch. It is a managed asset migration.

Third, **attestation under post-quantum signatures**. HSM and TEE attestation — the cryptographic proof that a signing operation happened inside a particular trusted hardware boundary — currently relies on classical signatures from the hardware manufacturer's root of trust. Post-quantum attestation requires the manufacturer's root signing keys to become quantum-safe as well. That means re-issued device certificates, updated attestation flows, and audit-trail implications for any custody platform whose compliance posture relies on hardware attestation.

This is the hard boundary for hardware-anchored signing. The migration path is conceptually clear, and the standards are available. But the timeline is bounded by external dependencies that no custody operator controls on its own.

## MPC signing under post-quantum migration

MPC-based signing distributes signing authority across multiple parties so that no single party ever holds the full private key. Fireblocks, Curv — now part of PayPal — Copper, Dfns, and other institutional custody providers have used variations of this model. Threshold ECDSA, the dominant production pattern, is mature enough for institutional use. The performance is acceptable, and the operational model is familiar to many digital-asset teams.

Post-quantum migration changes three things here as well.

First, **threshold lattice-based signing is harder mathematics**. Threshold ECDSA works because elliptic-curve operations have algebraic structure that is relatively well suited to distributed signing. ML-DSA is different. It involves lattice-based operations, sampling, and rejection-sampling behavior that do not map as cleanly into the threshold protocols used for ECDSA. Research exists, but the distance between *works in a paper* and *meets institutional custody latency requirements under production controls* is not small. SLH-DSA has a different set of tradeoffs: conservative security assumptions, larger signatures, and slower signing performance.

Second, **performance and round complexity matter**. Threshold ECDSA in modern production deployments can complete signing in a small number of communication rounds, often with sub-second latency for common quorum sizes. Production-grade threshold ML-DSA or threshold SLH-DSA is not yet at the same level of maturity. If signing latency moves from sub-second to several seconds, the difference is not academic. It changes product behavior, operational risk, and service-level commitments.

Third, **the migration is mostly software-side**. This is the corresponding advantage. Where hardware-anchored signing is constrained by HSM firmware, validation cycles, and hardware attestation chains, MPC migration is constrained mainly by protocol design, implementation quality, and security review. Once production-grade threshold post-quantum signing is available, an MPC custody provider can in principle deploy it through software and infrastructure updates.

That does not make MPC automatically safer. It means the bottleneck is different. Hardware-anchored signing has clearer standards but slower external dependencies. MPC has more upgradeable infrastructure but less mature threshold post-quantum signing.

<figure>
  <img src="/images/posts/quantum-safe-custody/figure-2-resource-compression.svg" alt="Bar chart showing physical qubit estimates for attacking ECDSA — approximately 1,000,000 qubits in Gidney's 2019–2021 baseline, under 500,000 in the Google + Drake + Boneh March 2026 whitepaper, and 10,000 to 26,000 in the Caltech + Oratomic March 2026 preprint.">
  <figcaption>Resource estimates for breaking ECDSA, before and after March 2026. Both 2026 results remain whitepaper and preprint, not peer-reviewed engineering fact.</figcaption>
</figure>

## Hybrid migration and the crypto-agility frame

The realistic 2026–2028 path for institutional custody is neither a clean cutover to a single post-quantum algorithm nor indefinite continuation on classical algorithms. It is hybrid operation: classical and post-quantum signatures during a transition period, explicit algorithm agility in key schemas, and policy-driven retirement of vulnerable primitives.

This is the **crypto-agility** frame [IBM Quantum Safe](https://www.ibm.com/quantum/blog/crypto-agility) has been arguing for, and it is the right architectural lens here even if one does not use IBM products. IBM's crypto-agility framework emphasizes architecture, automation, and governance. Those three categories map directly onto custody.

*Architecturally*, crypto-agility means decoupling cryptographic primitives from the rest of the platform. A custody application should not have business logic that assumes the underlying signature is ECDSA. The signing operation should be accessed through an abstraction layer, with algorithm choice driven by configuration, policy, and client constraints.

*Operationally*, crypto-agility means key generation, rotation, algorithm updates, and certificate renewal are managed by tooling rather than manual procedures. A custody platform that requires manual per-client intervention to add a new signature algorithm will migrate slowly. A platform with automated key lifecycle management has a better chance of migrating in weeks rather than quarters.

*In governance terms*, crypto-agility means the platform can answer a simple question at any moment: what cryptography am I using, where, and at what version? The Cryptography Bill of Materials, now supported in CycloneDX 1.6 and generated by tools such as IBM Quantum Safe Explorer, is one practical format for that inventory. For a custody operator answering a bank RFP in 2027, a CBOM-style cryptographic inventory will not be a theoretical nicety. It will be a procurement question.

## What this means for buyers

Most institutional buyers and many custody operators are not yet organised for this migration. [CNN, citing McKinsey data](https://www.cnn.com/2026/05/17/science/quantum-computing-cybersecurity-q-day), reports that more than 90% of businesses still lack a quantum-security roadmap of any kind. The implication for procurement is direct: the majority of platforms a buyer evaluates in 2026 will not yet have credible answers to the questions below.

For institutional clients evaluating custody platforms in the 2026–2028 window, the useful questions are concrete.

**How long does it take this platform to add support for a new signature algorithm?** The relevant interval is not from vendor announcement to press release. It is from standardization to production use across relevant keys.

**What is the key-rotation architecture?** Can the platform generate keys under a different algorithm, migrate assets to addresses derived from those keys, and decommission old keys without manual intervention for each client?

**Does the platform support hybrid signing during transition periods?** Dual-signing is operationally heavier, but it is likely to be the safer transition posture for many institutional systems.

**What is the platform's cryptographic inventory?** Can it produce a CBOM or equivalent inventory showing algorithms, keys, certificates, dependencies, and vulnerable primitives?

**What external dependencies bound the migration timeline?** This is the question buyers should ask twice. A platform's quantum-readiness timeline cannot be faster than the slowest external component it relies on. If a custody provider's claimed migration timeline is faster than its HSM vendor's post-quantum firmware and validation roadmap, the claim needs evidence.

## The point

The planning baseline for Q-Day compressed in March 2026. Hardware-anchored signing and MPC signing now face different migration problems. Both can reach post-quantum custody, but not through the same path.

The platforms that migrate cleanly will be the ones designed for crypto-agility before the emergency. The platforms that did not will discover, around 2028 or 2029, that a deferred cryptography problem has become an operational one.

The question for custody architects, operators, and buyers is no longer only *when is Q-Day*. It is whether the platform can change its cryptography fast enough. That answer is being set now, in key schemas, signing abstractions, vendor dependencies, attestation models, and migration tooling.
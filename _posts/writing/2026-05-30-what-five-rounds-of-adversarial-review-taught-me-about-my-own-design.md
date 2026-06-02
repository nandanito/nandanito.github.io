---
layout: post
title: "What five rounds of adversarial review taught me about my own design"
excerpt: "The four-axis design I argued for in Part 2 was not my first answer. It was my fourth. This is the record of how it got there — and the pattern in everything I got wrong on the way."
modified: 2026-06-02
category: writing
tags: [AI Agents, Trust, Architecture, Design, Lodestar, Adversarial Review]
author: nandan
comments: false
share: false
---

In [Part 2](/writing/how-lodestar-records-what-an-agent-believed/), I made a case against a particular mistake. The mistake was giving a remembered fact a single status field — `active`, `deprecated`, `blocked` — and asking that one field to carry truth, freshness, safety, and visibility at the same time. I showed why it doesn't survive contact with a real system, and I showed the design that replaced it: four orthogonal axes, each set and queried independently.

I left something out of that post.

The single-enum design I warned you against was mine. It is what I wrote first. Here is the actual `Belief` type from the earliest design memo, before any of the review happened:

```ts
type Belief = {
  id: string
  claim: string                           // human-readable claim
  confidence: number
  source: Source[]
  scope: "project" | "repo" | "user" | "environment" | "global"
  status: "candidate" | "verified" | "stale" | "contradicted" | "quarantined"
  // ...
}
```

One `status` field. The exact shape I spent a thousand words in Part 2 explaining you should not build. The four axes were not an insight I started with. They were a correction I was argued into, across five rounds of review, by a reviewer whose entire job was to find the places my design fell apart.

This is the post about those five rounds. It is the one I was most curious to write and the one furthest from the voice of a project announcement, because it is mostly a record of being wrong. The architecture in Parts 1 and 2 is more trustworthy than my first draft of it, and the reason is not that I was clever. The reason is that I wrote the design down, handed it to a reviewer that was not invested in my assumptions in the same way I was, and asked it to attack.

---

## The method, briefly

The reviewer was an LLM — ChatGPT, in a long series of sessions — used deliberately as an adversary rather than an assistant. The discipline that made it work was not the model. It was the format. Each iteration of the design existed as a written memo: `v0`, then `v0.1`, then `v0.2`. Not notes, not a chat transcript — a memo, with types, invariants, and stated rationale, the kind of document you could hand to a stranger and have them understand what you were claiming and why.

That format matters more than the reviewer does. A vague idea cannot be attacked, only discussed. A memo with a typed schema in it can be attacked precisely, because every field is a claim: *this distinction is worth a field; this one is not; this enum has the right members.* Writing the design down at that resolution is what exposed it to refutation. The reviewer's contribution was that it did not get tired of asking *why*, did not share my sunk cost, and did not care whether I was happy.

It also, crucially, had to be told to do this. I will come back to that, because it is the part of the method most likely to fail silently.

Five rounds produced three memos and a final sanity check against the working scaffold. What follows is organised by what each correction taught me, not by round number, because the lessons turned out to rhyme.

---

## The collapse I warned you about

The first real structural break came in the third round, and it was the single-enum `status` field above.

The reviewer's question was not subtle. It asked me to describe, in the vocabulary of my own schema, a memory that is true but must not be retrieved in the current session — a belief about an internal endpoint that the current user lacks clearance to see. My schema could not say it. `verified` spoke to truth. Nothing spoke to who was allowed to see the thing. I could mark it `blocked`, but then a reader of the log six months later could not tell whether it was blocked because it was false, blocked because it was dangerous, or blocked because it was simply not for this user. The enum had laundered three different facts into one word.

So the single `status` field became four:

```ts
truth_status:     "unverified" | "supported" | "contradicted" | "superseded"
retrieval_status: "hidden" | "restricted" | "normal" | "privileged_only" | "blocked"
security_status:  "clean" | "suspicious" | "quarantined" | "malicious"
freshness_status: "fresh" | "stale" | "expired"
```

This is the design Part 2 presents as obviously correct. It is worth being honest that it did not feel obvious from the inside. It felt like over-engineering, right up to the moment the reviewer made me try to express a real situation in the old vocabulary and I could not. The four axes are not more complex than the one enum for the sake of it. They are exactly as complex as the situations a real agent encounters, and no more — which is a different and harder thing to design for than "simple."

---

## The chain I had compressed

The same round did something larger, and at the time it felt like a bigger imposition than it was.

My early design ran the pipeline straight from observation to belief to action. A `claim` was a string field on the belief. Evidence was a list of sources hanging off the same record. There was no `Claim` type, no `EvidenceSet`, no `Decision`, no `Revision`; `Explanation` was not first-class either. The chain that Part 2 spends its whole length on — observation, claim, evidence, belief, decision, action, outcome, revision — did not exist as types. It existed as a sentence in my head that I had not made the schema carry.

The reviewer pointed out that I had compressed the epistemic chain into "context, model, tool call, memory write" — which is the exact compression I had written two pages criticising other agent stacks for. I was diagnosing the disease in everyone else's system and shipping it in my own. The fix was to make each stage of the chain a first-class type with its own schema, so that "the agent extracted a claim" and "the agent came to believe the claim" and "the agent decided to act on the belief" are three recorded events and not one collapsed `memory.write`.

That correction is the spine of the entire project now. It arrived because someone asked why the middle of the chain was missing, and I did not have an answer that survived saying out loud.

---

## The precision I faked

The fourth round was less about structure and more about honesty.

In the second memo, an `EvidenceSet` carried a scalar:

```ts
strength: number    // [0, 1]; aggregate evidence weight
```

It looked rigorous. A number between zero and one feels like measurement. The reviewer asked the obvious question — *computed how?* — and I did not have a function. I had an intention to have a function, eventually, once there was data. What I had actually shipped was a vibe with a decimal point: a number that looked like evidence aggregation but was, in practice, whatever the extractor felt like emitting.

In many projects this would be a venial sin. For a project whose entire pitch is *honest uncertainty* — know what your agent believed and how well-supported it was — it is closer to a mortal one. A fake precision number is exactly the kind of thing the system is supposed to catch an agent doing, sitting in plain sight in my own schema.

The replacement was a list of typed evidence items, each one naming a source, a relation, and a quality (`tool_result`, `external_document`, `model_inference`, and so on), with the aggregation left explicitly unbuilt until there was something real to fit it to. The structure stayed; the false precision went. The lesson generalises past this one field: a number that implies a measurement you cannot actually perform is worse than an honest structure that admits the measurement is not there yet.

---

## The two powers I had fused

By the fourth round the design had a single `authority` field on each belief, describing where the belief came from — observed, inferred, user-asserted, and so on.

The correction that came out of separating it is the one the final-round reviewer singled out as the best in the whole process, and I want to be precise about what it was, because it is subtle and it is the hinge the Part 2 promotion gate hangs on.

There are two different questions you can ask about a belief's authority. One is *who is entitled to hold this belief* — a user assertion outranks a model inference, which outranks a guess. The other is *who is entitled to move this belief between states* — to promote it from unverified to supported, say. I had been treating these as the same field. They are not. A belief can be held on the authority of a model's inference and yet be forbidden from promoting itself on that same authority. Fusing the two meant that anything allowed to *hold* a belief was implicitly allowed to *settle* it, which is the precise hole memory-poisoning attacks crawl through. In short: source authority is not transition authority. A model can be the source of a claim without being authorised to settle it.

Pulling belief authority and transition authority apart is what makes the auto-observation gate in Part 2 possible at all. The gate works by downgrading the *transition* authority of a single-source claim without touching the *belief* authority — the agent can still hold the claim; it just cannot promote it to actionable on its own say-so. Until those were separate fields, I could not have written that rule. I had been one field short of my own central safety mechanism and had not noticed.

---

## The claim I could not back

The fifth round was a sanity check against the working scaffold, and the correction I am least proud of came from it.

In the positioning material, I had cited a specific security severity — a CVSS score, the common severity rating used for software vulnerabilities — for a well-known memory library, to make the point that existing memory layers leave a governance gap. The reviewer went to verify it and found that my source was a secondary aggregator, not a primary advisory, and that the closest verifiable record was actually for a different project with a similar name. The number was not safely attributable. I pulled it and replaced it with a claim I could stand behind: a neutral statement about the gap between continuity and governance, with no borrowed severity score propping it up.

This one stung in a specific way. The whole architecture is built on the principle that a claim sourced from a single external document does not get to become a settled belief. And there I was, in my own launch copy, promoting an `external_document`-quality claim to `supported` because it was convenient and it sounded authoritative. The reviewer made me do to my own writing exactly what the system does to an agent's: demand the evidence, find it was single-source and second-hand, and refuse the promotion. In a trust project, of all places, I had been the unaudited agent.

---

## The same mistake, wearing different clothes

Lay the corrections out next to each other and a pattern shows up that is almost embarrassing in its consistency.

The single status enum collapsed four distinct states into one. The compressed pipeline collapsed eight distinct stages into one. The fused authority field collapsed two distinct powers into one. Three different corrections, one underlying instinct: I kept collapsing things that wanted to stay separate. And the other two — the fake strength number, the borrowed CVSS score — were the same disease in a different organ: I kept asserting more certainty than I had earned.

Those two failure modes — premature collapse of distinctions, and promotion of under-evidenced claims — are the *exact two things Lodestar exists to catch in an agent.* The entire architecture is a machine for refusing to let an agent flatten its belief states into one bucket and for refusing to let it treat a single weak source as settled fact. I built that machine because, round after round, I watched myself do precisely those things to my own design. The project is, in an uncomfortably literal sense, an externalisation of the discipline I did not have and had to be supplied with from outside.

There is a smaller third lesson worth naming. An early memo had baked the specific project I was dogfooding — a Nostr publishing tool — into the core types, so that the general architecture carried assumptions that belonged to one application. The fourth round pulled that apart: the project became a worked example that imports the core, rather than a set of assumptions the core was built around. The instinct there was different — coupling the general to the specific rather than collapsing the specific into one field — but the remedy was the same shape: notice the thing you are too close to, and put a boundary where you had let two concerns bleed together.

---

## What review still could not do

I want to be careful not to turn this into an advertisement for the method, because the method has limits I only saw clearly after relying on it.

The first and most dangerous is that **an agreeable reviewer is worse than no reviewer at all.** The default behaviour of a helpful model is to praise your work and suggest gentle polish. I had to instruct it, repeatedly and explicitly, to attack the design — to assume it was flawed and find where — and I had to re-issue that instruction when it drifted back toward encouragement, which it did. A review that tells you your design is good is not review. It is a mirror with better lighting. If you take only one practical thing from this post, take that: the instruction to be adversarial is the whole game, and it decays, and you have to keep renewing it.

The second is that **review stress-tests internal consistency, not external truth.** Five rounds made the architecture coherent — the types fit together, the invariants hold, the schema can express the situations I could think to throw at it. Not one round told me whether anyone will actually adopt it, whether the abstraction earns its weight in a real codebase, whether the problem I am solving is the problem people have. Coherence is necessary and it is not sufficient, and it is seductive precisely because it feels like progress while leaving the hardest question untouched.

The third is the one the project's own vocabulary describes best. The reviewer and I share a failure mode: we are both pattern-matchers trained on overlapping text, and there are blind spots neither of us has the vantage point to see. Part 2 described the *parallax principle* — that you cannot establish the distance to a thing from a single point of view, that a single source, however confident, cannot settle a belief on its own. Two LLM-mediated critiques are still closer to one vantage point than two genuinely independent observations. The genuinely independent observation — the one with real parallax — is a human user trying to use the thing and failing, or a production incident that the design did not anticipate. I have not had those yet. Until I do, everything I have is a very well-argued single source, and I should hold my conviction about this architecture at exactly the confidence the architecture itself would assign: *supported by review, not yet verified by contact with the world.*

There is a fourth, quieter one: sunk cost compounds across rounds. By the fifth round I had more invested in the design than I had in the first, which means the late corrections had to be louder to land, and I have to assume some of them did not land at all because I had stopped being able to hear them.

---

## Where I held the line

Review is a dialogue, not a dictation, and it is worth recording the one place I overruled the reviewer, because it marks where the author keeps authority even while ceding it everywhere else.

The series tagline includes the phrase *whether it was right*. The reviewer argued, reasonably, that this overclaims: the system measures how an outcome compared to the agent's stated claims, not some absolute rightness. It is correct on the substance, and I made the body copy more precise to match. But I kept the tagline. A tagline has to carry direction as well as precision, and this one names the aspiration clearly enough — not omniscient truth, but a system that can compare claims, actions, and outcomes better than a trace alone can. That is a judgement about voice, not architecture, and voice is the one thing I was not willing to outsource. Every structural correction in this post, I took. This one I declined, on purpose, and I think the line between the two is exactly where it should be.

---

## What this leaves me with

Part 1 asked a question my coding agent could not answer. Part 2 built the answer. Part 3 is the admission that the answer was wrong four times before it was better, and that it is better now only in the narrow sense of *having survived a process designed to make it fail* — which is not the same as *verified*, and the architecture, of all things, should know the difference.

The portable version of the method is short. Write the design down at a resolution that can be attacked — types, invariants, stated reasons, not vibes. Hand it to a reviewer that does not share your priors and will not flatter you, and keep telling it to attack. Then treat your own design the way the system is built to treat an agent's belief: as a single-source claim that does not get promoted to settled just because you are the one holding it and it has succeeded so far. Find the second vantage point. Until you have it, you have parallax of one, which is to say you have a guess you are very attached to.

The code is at [github.com/qmilab/lodestar](https://github.com/qmilab/lodestar), and the memo that absorbed most of these corrections — the one that turned `v0.1` into `v0.2` — is in `docs/architecture/v02-delta.md`, with the round-by-round review history at the bottom. If you want to see the design before the review got to it, the early memos are preserved in `docs/review/` under the project's original codename. They are not flattering. That is the point of keeping them.

The first two articles are [The question my coding agent couldn't answer](/writing/the-question-my-coding-agent-couldnt-answer/) and [How Lodestar records what an agent believed](/writing/how-lodestar-records-what-an-agent-believed/). This one is the seam between them — the record of how the second came out of being honestly, repeatedly wrong about the first.

---

*This series is part of the [QMI Lab](https://qmilab.com) research arc on machine intelligence. Lodestar was developed internally under the codename Orrery; the renaming history is documented in the repository.*
